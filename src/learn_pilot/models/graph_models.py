"""
知识图谱相关数据模型
用于定义概念、关系、图谱结构等
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set, Tuple
from datetime import datetime
from enum import Enum
import networkx as nx

class RelationshipType(Enum):
    """关系类型枚举"""
    PREREQUISITE = "prerequisite"    # 前置要求
    EXTENDS = "extends"             # 扩展关系
    APPLIES = "applies"             # 应用关系
    COMPARES = "compares"           # 比较关系
    IMPLEMENTS = "implements"       # 实现关系
    SIMILAR_TO = "similar_to"       # 相似关系

class ConceptType(Enum):
    """概念类型枚举"""
    ALGORITHM = "algorithm"         # 算法
    MODEL = "model"                # 模型
    TECHNIQUE = "technique"         # 技术
    THEORY = "theory"              # 理论
    APPLICATION = "application"     # 应用
    DATASET = "dataset"            # 数据集
    METRIC = "metric"              # 评估指标

@dataclass
class Concept:
    """概念实体"""
    id: str
    name: str
    description: str
    concept_type: ConceptType
    
    # 层级和分类
    domain: str  # 所属领域，如 "machine_learning", "nlp", "computer_vision"
    complexity_level: str  # "basic", "intermediate", "advanced"
    
    # 关联信息
    aliases: List[str] = field(default_factory=list)  # 别名
    keywords: List[str] = field(default_factory=list)  # 关键词
    related_papers: List[str] = field(default_factory=list)  # 相关论文ID
    
    # 元信息
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_alias(self, alias: str):
        """添加别名"""
        if alias not in self.aliases:
            self.aliases.append(alias)
    
    def add_paper(self, paper_id: str):
        """关联论文"""
        if paper_id not in self.related_papers:
            self.related_papers.append(paper_id)

@dataclass
class ConceptRelationship:
    """概念间关系"""
    source_concept: str  # 源概念ID
    target_concept: str  # 目标概念ID
    relationship_type: RelationshipType
    strength: float  # 关系强度 0.0-1.0
    description: str = ""
    confidence: float = 1.0  # 置信度
    evidence_papers: List[str] = field(default_factory=list)  # 支撑证据论文
    
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class PaperConceptMap:
    """论文-概念映射"""
    paper_id: str
    concepts: List[str]  # 论文包含的概念ID列表
    concept_importance: Dict[str, float] = field(default_factory=dict)  # 概念重要性评分
    concept_sections: Dict[str, List[str]] = field(default_factory=dict)  # 概念出现的章节
    
    def add_concept(self, concept_id: str, importance: float = 1.0, sections: List[str] = None):
        """添加概念"""
        if concept_id not in self.concepts:
            self.concepts.append(concept_id)
        self.concept_importance[concept_id] = importance
        if sections:
            self.concept_sections[concept_id] = sections

@dataclass
class KnowledgeGraph:
    """知识图谱"""
    concepts: Dict[str, Concept] = field(default_factory=dict)
    relationships: List[ConceptRelationship] = field(default_factory=list)
    paper_concept_maps: Dict[str, PaperConceptMap] = field(default_factory=dict)
    
    # 图结构（使用NetworkX）
    _graph: Optional[nx.DiGraph] = field(default=None, init=False)
    
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """初始化时创建空的图结构"""
        self._graph = nx.DiGraph()
    
    def add_concept(self, concept: Concept):
        """添加概念"""
        self.concepts[concept.id] = concept
        self._graph.add_node(concept.id, **concept.__dict__)
        self.last_updated = datetime.now()
    
    def add_relationship(self, relationship: ConceptRelationship):
        """添加关系"""
        self.relationships.append(relationship)
        self._graph.add_edge(
            relationship.source_concept,
            relationship.target_concept,
            relationship_type=relationship.relationship_type.value,
            strength=relationship.strength,
            description=relationship.description
        )
        self.last_updated = datetime.now()
    
    def get_concept(self, concept_id: str) -> Optional[Concept]:
        """获取概念"""
        return self.concepts.get(concept_id)
    
    def get_related_concepts(self, concept_id: str, max_distance: int = 2) -> List[str]:
        """获取相关概念（基于图距离）"""
        if concept_id not in self._graph:
            return []
        
        related = []
        for target in self._graph.nodes():
            if target != concept_id:
                try:
                    distance = nx.shortest_path_length(self._graph, concept_id, target)
                    if distance <= max_distance:
                        related.append(target)
                except nx.NetworkXNoPath:
                    continue
        
        return related
    
    def get_prerequisites(self, concept_id: str) -> List[str]:
        """获取前置概念"""
        prerequisites = []
        for rel in self.relationships:
            if (rel.target_concept == concept_id and 
                rel.relationship_type == RelationshipType.PREREQUISITE):
                prerequisites.append(rel.source_concept)
        return prerequisites
    
    def get_graph_metrics(self) -> Dict[str, Any]:
        """计算图的基本指标"""
        if not self._graph.nodes():
            return {}
        
        return {
            "num_concepts": len(self._graph.nodes()),
            "num_relationships": len(self._graph.edges()),
            "density": nx.density(self._graph),
            "is_connected": nx.is_weakly_connected(self._graph),
            "num_components": nx.number_weakly_connected_components(self._graph),
            "avg_clustering": nx.average_clustering(self._graph.to_undirected()),
        }
    
    def export_to_networkx(self) -> nx.DiGraph:
        """导出为NetworkX图"""
        return self._graph.copy()
    
    def get_topological_order(self) -> List[str]:
        """获取拓扑排序（用于依赖关系排序）"""
        try:
            return list(nx.topological_sort(self._graph))
        except nx.NetworkXError:
            # 如果有环，返回近似排序
            return list(self._graph.nodes())

@dataclass
class ConceptCluster:
    """概念聚类"""
    cluster_id: str
    name: str
    concepts: List[str]  # 概念ID列表
    center_concept: Optional[str] = None  # 中心概念
    cohesion_score: float = 0.0  # 聚类内聚度
    
    def add_concept(self, concept_id: str):
        """添加概念到聚类"""
        if concept_id not in self.concepts:
            self.concepts.append(concept_id)

@dataclass
class LearningPath:
    """学习路径"""
    path_id: str
    name: str
    concepts: List[str]  # 按学习顺序排列的概念ID
    estimated_time: Dict[str, int] = field(default_factory=dict)  # 每个概念的预估学习时间（分钟）
    difficulty_progression: List[str] = field(default_factory=list)  # 难度递进
    
    created_at: datetime = field(default_factory=datetime.now)
    
    def get_total_time(self) -> int:
        """获取总学习时间"""
        return sum(self.estimated_time.values())
    
    def get_concept_position(self, concept_id: str) -> int:
        """获取概念在路径中的位置"""
        try:
            return self.concepts.index(concept_id)
        except ValueError:
            return -1
