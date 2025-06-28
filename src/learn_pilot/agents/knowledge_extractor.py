"""
Knowledge Extractor Agent
概念提取Agent，使用LLM进行智能概念提取和知识分析
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json

from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent
from src.learn_pilot.core.config.config import OPENAI_API_KEY, LANGUAGE
from src.learn_pilot.models.paper_models import Paper

logger = logging.getLogger(__name__)

class Prerequisite(BaseModel):
    level: str
    name: str
    
class ConceptRelationship(BaseModel):
    concept1: str
    relationship: str
    concept2: str

class ConceptExtractionOutput(BaseModel):
    """概念提取输出结构"""
    core_concepts: List[str] = Field(description="核心概念列表")
    supporting_concepts: List[str] = Field(description="支撑概念列表")
    prerequisites: List[Prerequisite] = Field(description="前置知识要求")
    difficulty_assessment: str = Field(description="难度评估: beginner, intermediate, advanced")
    conceptual_complexity: str = Field(description="概念复杂度: low, medium, high")
    estimated_learning_time: int = Field(description="学习时间估计(分钟)")
    concept_relationships: List[ConceptRelationship] = Field(description="概念关系")
    knowledge_domains: List[str] = Field(description="知识领域列表")

class KnowledgeExtractor:
    """知识提取器Agent - LLM驱动版本"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.model = self.config.get("model", "gpt-4o-2024-11-20")
        
    async def extract_concepts_from_papers(self, papers: List[Paper]) -> Dict[str, Any]:
        """从论文列表中提取概念"""
        try:
            self.logger.info(f"🧠 开始从 {len(papers)} 篇论文中提取概念")
            
            # 为每篇论文提取概念
            extractions = {}
            for i, paper in enumerate(papers):
                paper_id = f"paper_{i+1}"
                self.logger.info(f"🔍 提取论文概念 {paper_id}: {paper.title}")
                
                extraction = await self._extract_concepts_from_paper(paper)
                extractions[paper_id] = extraction
            
            # 生成跨论文的概念关系分析
            cross_paper_analysis = await self._analyze_cross_paper_concepts(extractions)
            
            result = {
                "extractions": extractions,
                "cross_paper_analysis": cross_paper_analysis,
                "paper_ids": list(extractions.keys())
            }
            
            self.logger.info(f"✅ 概念提取完成: {len(papers)} 篇论文")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 概念提取失败: {e}")
            raise
    
    async def _extract_concepts_from_paper(self, paper: Paper) -> Dict[str, Any]:
        """从单篇论文中提取概念"""
        
        # 构建论文内容
        paper_content = f"""
标题: {paper.title}

摘要:
{paper.abstract}

主要章节内容:
"""
        # 只包含主要章节，避免内容过长
        main_sections = [s for s in paper.sections if any(keyword in s.title.lower() 
                                                         for keyword in ['introduction', 'method', 'approach', 'model', 'algorithm', 'conclusion'])]
        for section in main_sections[:5]:  # 最多5个主要章节
            paper_content += f"\n## {section.title}\n{section.content[:2000]}...\n"  # 限制每个章节长度
        
        # 构建概念提取prompt
        instructions = f"""
你是一位资深的学术研究专家，专门负责从论文中提取和分析核心概念。

请仔细分析这篇论文，识别和提取：

1. **核心概念**: 论文的主要技术概念、方法、模型等
2. **支撑概念**: 论文中提到的相关技术和理论
3. **前置知识**: 理解这篇论文需要的基础知识
4. **概念关系**: 概念之间的依赖、扩展、相似关系
5. **知识领域**: 论文所属的技术领域

评估标准：
- 难度评估基于研究生水平
- 学习时间估算包括理解和掌握
- 前置知识应该具体且实用
- 概念关系要明确说明关系类型

请用{LANGUAGE}回答所有内容。
"""

        # 创建LLM提取器
        extractor = StructuredOutputAgent(
            model=self.model,
            api_key=OPENAI_API_KEY,
            instructions=instructions,
            output_type=ConceptExtractionOutput
        )
        
        input_messages = [
            {
                "role": "user", 
                "content": f"请提取以下论文的概念和知识结构：\n\n{paper_content}"
            }
        ]
        
        # 执行提取
        result = await extractor.run(input_messages)
        return result
    
    async def _analyze_cross_paper_concepts(self, extractions: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """分析跨论文的概念关系"""
        
        # 收集所有概念信息
        all_concepts_info = []
        for paper_id, extraction in extractions.items():
            output = extraction['output']
            all_concepts_info.append({
                'paper_id': paper_id,
                'core_concepts': output['core_concepts'],
                'supporting_concepts': output['supporting_concepts'],
                'knowledge_domains': output['knowledge_domains'],
                'difficulty': output['difficulty_assessment']
            })
        
        # 构建跨论文分析prompt
        cross_analysis_prompt = f"""
基于以下多篇论文的概念提取结果，请进行跨论文的概念关系分析：

{json.dumps(all_concepts_info, ensure_ascii=False, indent=2)}

请分析：
1. 共同出现的核心概念
2. 概念的依赖关系图
3. 论文间的知识递进关系
4. 推荐的学习路径
5. 概念集群分析

用{LANGUAGE}提供分析结果。
"""

        class ConceptCluster(BaseModel):
            concept: str
            related_concepts: List[str] 
            
        class LearningDependency(BaseModel):
            prerequisite_paper: str
            dependent_paper: str
            reason: str
            
        class ConceptHierarchy(BaseModel):
            level: str
            concepts: List[str]
            
        class KnowledgeGraphEdge(BaseModel):
            source: str
            target: str
            relationship: str

        # 定义跨论文分析输出结构
        class CrossPaperAnalysisOutput(BaseModel):
            common_concepts: List[str] = Field(description="共同概念列表")
            concept_hierarchy: List[ConceptHierarchy] = Field(description="概念层次结构")
            learning_dependencies: List[LearningDependency] = Field(description="学习依赖关系")
            recommended_sequence: List[str] = Field(description="推荐学习顺序")
            concept_clusters: List[ConceptCluster] = Field(description="概念聚类")
            knowledge_graph_edges: List[KnowledgeGraphEdge] = Field(description="知识图谱边")

        analyzer = StructuredOutputAgent(
            model=self.model,
            api_key=OPENAI_API_KEY,
            instructions="你是知识图谱专家，请分析论文间的概念关系并构建学习路径。",
            output_type=CrossPaperAnalysisOutput
        )
        
        result = await analyzer.run([{"role": "user", "content": cross_analysis_prompt}])
        return result
    
    def save_extraction_results(self, results: Dict[str, Any], output_dir: str):
        """保存概念提取结果"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存详细提取结果
        extraction_file = os.path.join(output_dir, "concept_extraction.json")
        
        # 准备可序列化的数据
        serializable_results = {
            "extractions": {},
            "cross_paper_analysis": results.get("cross_paper_analysis", {}),
            "paper_ids": results.get("paper_ids", [])
        }
        
        # 转换提取结果
        for paper_id, result in results.get("extractions", {}).items():
            serializable_results["extractions"][paper_id] = {
                "output": result["output"],
                "usage": result["usage"]
            }
        
        with open(extraction_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        # 生成概念图谱报告
        report = self._generate_concept_report(results)
        report_file = os.path.join(output_dir, "concept_extraction_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"🧠 概念提取结果已保存到: {output_dir}")
    
    def _generate_concept_report(self, results: Dict[str, Any]) -> str:
        """生成概念提取报告"""
        lines = ["# 🧠 概念提取与知识图谱报告", ""]
        
        extractions = results.get("extractions", {})
        cross_analysis = results.get("cross_paper_analysis", {}).get("output", {})
        
        # 基本统计
        lines.append("## 📊 提取统计")
        lines.append(f"- 处理论文数: {len(extractions)}")
        
        total_core_concepts = sum(len(e["output"]["core_concepts"]) for e in extractions.values())
        lines.append(f"- 核心概念总数: {total_core_concepts}")
        
        if cross_analysis.get("common_concepts"):
            lines.append(f"- 共同概念数: {len(cross_analysis['common_concepts'])}")
        
        lines.append("")
        
        # 概念层次结构
        if cross_analysis.get("concept_hierarchy"):
            lines.append("## 🎯 概念层次结构")
            hierarchy = cross_analysis["concept_hierarchy"]
            for data in hierarchy:
                level = data['level']
                concepts = data['concepts']
                lines.append(f"### {level.title()}")
                for concept in concepts[:8]:  # 限制显示数量
                    lines.append(f"- {concept}")
                lines.append("")
        
        # 推荐学习顺序
        if cross_analysis.get("recommended_sequence"):
            lines.append("## 📚 推荐学习顺序")
            for i, paper_id in enumerate(cross_analysis["recommended_sequence"], 1):
                if paper_id in extractions:
                    output = extractions[paper_id]["output"]
                    difficulty = output["difficulty_assessment"]
                    time = output["estimated_learning_time"]
                    domains = ", ".join(output["knowledge_domains"][:3])
                    lines.append(f"{i}. **{paper_id}** ({difficulty}, {time}分钟)")
                    lines.append(f"   - 领域: {domains}")
                    lines.append(f"   - 核心概念: {', '.join(output['core_concepts'][:3])}...")
            lines.append("")
        
        # 概念聚类
        if cross_analysis.get("concept_clusters"):
            lines.append("## 🎭 概念聚类")
            clusters = cross_analysis["concept_clusters"]
            for data in clusters:
                concept = data['concept']
                related_concepts = data['related_concepts']
                lines.append(f"### {concept}")
                for concept in related_concepts[:6]:
                    lines.append(f"- {concept}")
                lines.append("")
        
        # 学习依赖关系
        if cross_analysis.get("learning_dependencies"):
            lines.append("## 🔗 论文依赖关系")
            for dep in cross_analysis["learning_dependencies"][:5]:
                lines.append(f"- **{dep['prerequisite_paper']}** → **{dep['dependent_paper']}**")
                lines.append(f"  - 原因: {dep['reason']}")
            lines.append("")
        
        # 各论文详情
        lines.append("## 📋 各论文概念详情")
        for paper_id, extraction in extractions.items():
            output = extraction["output"]
            lines.append(f"### {paper_id}")
            lines.append(f"- **难度**: {output['difficulty_assessment']}")
            lines.append(f"- **学习时间**: {output['estimated_learning_time']} 分钟")
            lines.append(f"- **领域**: {', '.join(output['knowledge_domains'])}")
            lines.append(f"- **核心概念**: {', '.join(output['core_concepts'][:5])}")
            lines.append(f"- **前置知识**: {len(output['prerequisites'])} 项")
            lines.append("")
        
        return "\n".join(lines)

# 便捷函数
async def extract_concepts_from_papers(papers: List[Paper], output_dir: str = None) -> Dict[str, Any]:
    """便捷函数：从论文列表提取概念"""
    extractor = KnowledgeExtractor()
    results = await extractor.extract_concepts_from_papers(papers)
    
    if output_dir:
        extractor.save_extraction_results(results, output_dir)
    
    return results

if __name__ == "__main__":
    # 测试代码
    async def test():
        extractor = KnowledgeExtractor()
        print("✅ KnowledgeExtractor 初始化完成")
    
    asyncio.run(test()) 