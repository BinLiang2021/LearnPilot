"""
Knowledge Graph Agent
构建论文间的知识依赖图谱
"""

from typing import Dict, List, Any, Tuple
import networkx as nx
import logging

logger = logging.getLogger(__name__)

class KnowledgeGraphAgent:
    """知识图谱构建器"""
    
    def __init__(self):
        self.logger = logger
        self.graph = nx.DiGraph()
    
    def build_dependency_graph(self, papers_concepts: Dict[str, Dict]) -> nx.DiGraph:
        """
        构建论文依赖图
        
        Args:
            papers_concepts: 论文概念字典 {paper_id: {concepts: [], prerequisites: []}}
            
        Returns:
            NetworkX 有向图
        """
        self.graph.clear()
        
        # 添加所有论文节点
        for paper_id, data in papers_concepts.items():
            self.graph.add_node(paper_id, 
                               concepts=data.get('concepts', []),
                               prerequisites=data.get('prerequisites', []),
                               difficulty=data.get('difficulty_level', 'intermediate'))
        
        # 构建依赖边：如果论文A的概念是论文B的前置知识，则B依赖A
        for paper_id_b, data_b in papers_concepts.items():
            prerequisites_b = set(data_b.get('prerequisites', []))
            
            for paper_id_a, data_a in papers_concepts.items():
                if paper_id_a != paper_id_b:
                    concepts_a = set(data_a.get('concepts', []))
                    
                    # 计算概念重叠
                    overlap = len(prerequisites_b.intersection(concepts_a))
                    if overlap > 0:
                        # 添加依赖边，权重为重叠概念数
                        self.graph.add_edge(paper_id_a, paper_id_b, weight=overlap)
                        self.logger.debug(f"添加依赖: {paper_id_a} -> {paper_id_b} (重叠概念: {overlap})")
        
        self.logger.info(f"构建依赖图完成: {len(self.graph.nodes())} 个节点, {len(self.graph.edges())} 条边")
        return self.graph
    
    def get_reading_order(self) -> List[str]:
        """
        根据依赖图获取推荐阅读顺序
        
        Returns:
            按依赖关系排序的论文ID列表
        """
        try:
            return list(nx.topological_sort(self.graph))
        except nx.NetworkXError as e:
            self.logger.error(f"图中存在环形依赖: {e}")
            return list(self.graph.nodes())
    
    def analyze_complexity(self, paper_id: str) -> Dict[str, Any]:
        """
        分析论文复杂度（基于依赖关系）
        
        Args:
            paper_id: 论文ID
            
        Returns:
            复杂度分析结果
        """
        if paper_id not in self.graph.nodes():
            return {"error": f"论文 {paper_id} 不在图中"}
            
        # 计算各种复杂度指标
        in_degree = self.graph.in_degree(paper_id)  # 依赖数量
        out_degree = self.graph.out_degree(paper_id)  # 被依赖数量
        
        # 获取节点属性
        node_data = self.graph.nodes[paper_id]
        concepts = node_data.get('concepts', [])
        prerequisites = node_data.get('prerequisites', [])
        difficulty = node_data.get('difficulty', 'intermediate')
        
        # 计算路径复杂度 (从根节点到当前节点的最长路径)
        path_complexity = 0
        try:
            # 找到所有没有前置依赖的节点作为根节点
            root_nodes = [n for n in self.graph.nodes() if self.graph.in_degree(n) == 0]
            if root_nodes:
                max_path = 0
                for root in root_nodes:
                    try:
                        if nx.has_path(self.graph, root, paper_id):
                            path_length = nx.shortest_path_length(self.graph, root, paper_id)
                            max_path = max(max_path, path_length)
                    except nx.NetworkXNoPath:
                        continue
                path_complexity = max_path
        except Exception as e:
            self.logger.warning(f"计算路径复杂度时出错: {e}")
        
        # 计算综合复杂度分数
        concept_score = len(concepts) * 0.3
        prerequisite_score = len(prerequisites) * 0.4
        dependency_score = in_degree * 0.2
        path_score = path_complexity * 0.1
        
        total_score = concept_score + prerequisite_score + dependency_score + path_score
        
        # 根据分数确定复杂度等级
        if total_score <= 5:
            complexity_level = "low"
        elif total_score <= 15:
            complexity_level = "medium"
        else:
            complexity_level = "high"
        
        return {
            "paper_id": paper_id,
            "dependency_count": in_degree,
            "dependent_count": out_degree,
            "concept_count": len(concepts),
            "prerequisite_count": len(prerequisites),
            "path_complexity": path_complexity,
            "complexity_score": round(total_score, 2),
            "complexity_level": complexity_level,
            "difficulty_level": difficulty,
            "recommended_reading_position": path_complexity + 1
        }

if __name__ == "__main__":
    agent = KnowledgeGraphAgent()
    print("KnowledgeGraphAgent 初始化完成")
