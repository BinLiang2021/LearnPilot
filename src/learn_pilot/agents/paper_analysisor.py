"""
Paper Analysisor Agent
论文分析Agent，使用LLM进行智能分析
"""

import logging
import asyncio
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json

from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent
from src.learn_pilot.core.config.config import OPENAI_API_KEY, LANGUAGE
from src.learn_pilot.models.paper_models import Paper
from src.learn_pilot.literature_utils.markdown_parser import parse_papers_from_directory

logger = logging.getLogger(__name__)

class SectionSummary(BaseModel):
    sub_title: str
    summary: str

class PaperAnalysisOutput(BaseModel):
    """论文分析输出结构"""
    title: str
    authors: List[str]
    venue: str = Field(default="Unknown", description="发表会议或期刊")
    year: str = Field(default="Unknown", description="发表年份")
    research_problem: str
    main_method: str
    key_contributions: List[str]
    core_concepts: List[str]
    difficulty_level: str = Field(description="难度级别: beginner, intermediate, advanced")
    reading_time_estimate: int = Field(description="阅读时间估算(分钟)")
    section_summary: List[SectionSummary] = Field(description="章节摘要字典")
    technical_complexity: str = Field(description="技术复杂度: low, medium, high")
    prerequisites: List[str]

class PaperAnalysisor:
    """论文分析器Agent - LLM驱动版本"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.model = self.config.get("model", "gpt-4o-2024-11-20")
        
    async def analyze_papers(self, input_dir: str) -> Dict[str, Any]:
        """分析论文目录中的所有论文"""
        try:
            self.logger.info(f"🔍 开始分析论文目录: {input_dir}")
            
            # 解析论文文件
            papers = parse_papers_from_directory(input_dir)
            
            if not papers:
                self.logger.warning("没有找到有效的论文文件")
                return {"papers": [], "analysis_results": {}}
            
            # 使用LLM分析每篇论文
            analysis_results = {}
            for i, paper in enumerate(papers):
                paper_id = f"paper_{i+1}"
                self.logger.info(f"📝 分析论文 {paper_id}: {paper.title}")
                
                analysis = await self._analyze_single_paper_with_llm(paper)
                analysis_results[paper_id] = analysis
            
            # 生成整体分析报告
            overall_analysis = await self._generate_overall_analysis(analysis_results)
            
            result = {
                "papers": papers,
                "analysis_results": analysis_results,
                "overall_analysis": overall_analysis,
                "paper_ids": list(analysis_results.keys())
            }
            
            self.logger.info(f"✅ 论文分析完成: {len(papers)} 篇论文")
            return result
            
        except Exception as e:
            self.logger.error(f"❌ 论文分析失败: {e}")
            raise
    
    async def _analyze_single_paper_with_llm(self, paper: Paper) -> Dict[str, Any]:
        """使用LLM分析单篇论文"""
        
        # 构建论文内容
        paper_content = f"""
标题: {paper.title}

作者: {', '.join(author.name for author in paper.authors)}

摘要:
{paper.abstract}

章节内容:
"""
        for section in paper.sections:
            paper_content += f"\n## {section.title}\n{section.content}\n"
        
        # 构建分析prompt
        instructions = f"""
你是一位资深的学术论文分析专家。请仔细分析以下论文，提取关键信息并进行深度分析。

请分析论文的：
1. 基本信息（标题、作者、发表信息等）
2. 研究问题和主要方法
3. 核心贡献和关键概念
4. 技术难度和学习要求
5. 各章节内容摘要

注意：
- 所有分析内容请用{LANGUAGE}回答
- 难度级别分为 beginner/intermediate/advanced
- 技术复杂度分为 low/medium/high  
- 阅读时间估算基于研究生水平（分钟）
- 前置知识应该具体且实用
"""

        # 创建LLM分析器
        analyzer = StructuredOutputAgent(
            model=self.model,
            api_key=OPENAI_API_KEY,
            instructions=instructions,
            output_type=PaperAnalysisOutput
        )
        
        input_messages = [
            {
                "role": "user", 
                "content": f"请分析以下论文：\n\n{paper_content}"
            }
        ]
        
        # 执行分析
        result = await analyzer.run(input_messages)
        return result
    
    async def _generate_overall_analysis(self, analysis_results: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """生成整体分析"""
        
        # 提取所有分析结果
        all_analyses = []
        for paper_id, result in analysis_results.items():
            analysis = result['output']
            all_analyses.append({
                'paper_id': paper_id,
                'title': analysis['title'],
                'difficulty_level': analysis['difficulty_level'],
                'core_concepts': analysis['core_concepts'],
                'prerequisites': analysis['prerequisites'],
                'reading_time': analysis['reading_time_estimate']
            })
        
        # 使用LLM生成整体分析
        overall_prompt = f"""
基于以下论文集的分析结果，请生成一个整体的学习建议和分析总结：

{json.dumps(all_analyses, ensure_ascii=False, indent=2)}

请分析：
1. 论文集的整体难度分布
2. 核心概念的分布和关联
3. 推荐的学习顺序
4. 总体学习时间估算
5. 学习建议和注意事项

用{LANGUAGE}回答，提供具体可操作的建议。
"""

        class DifficultyDistribution(BaseModel):
            level: str
            count: int
            
        class ConceptCluster(BaseModel):
            concept: str
            related_concepts: List[str]

        # 使用简单的LLM调用生成总结
        class OverallAnalysisOutput(BaseModel):
            difficulty_distribution: List[DifficultyDistribution] = Field(description="难度分布统计")
            common_concepts: List[str] = Field(description="共同概念列表")
            recommended_order: List[str] = Field(description="推荐论文学习顺序")
            total_estimated_time: int = Field(description="总学习时间(分钟)")
            learning_suggestions: List[str] = Field(description="学习建议列表")
            concept_clusters: List[ConceptCluster] = Field(description="概念聚类")

        analyzer = StructuredOutputAgent(
            model=self.model,
            api_key=OPENAI_API_KEY,
            instructions="你是学习规划专家，请基于论文分析结果生成整体学习建议。",
            output_type=OverallAnalysisOutput
        )
        
        result = await analyzer.run([{"role": "user", "content": overall_prompt}])
        return result
    
    def save_analysis_results(self, results: Dict[str, Any], output_dir: str):
        """保存分析结果"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存详细分析结果
        analysis_file = os.path.join(output_dir, "paper_analysis.json")
        
        # 准备可序列化的数据
        serializable_results = {
            "analysis_results": {},
            "overall_analysis": results.get("overall_analysis", {}),
            "paper_ids": results.get("paper_ids", [])
        }
        
        # 转换分析结果
        for paper_id, result in results.get("analysis_results", {}).items():
            serializable_results["analysis_results"][paper_id] = {
                "output": result["output"],
                "usage": result["usage"]
            }
        
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        # 生成简要报告
        report = self._generate_simple_report(results)
        report_file = os.path.join(output_dir, "analysis_report.md")
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        self.logger.info(f"📊 分析结果已保存到: {output_dir}")
    
    def _generate_simple_report(self, results: Dict[str, Any]) -> str:
        """生成简要报告"""
        lines = ["# 📚 论文分析报告", ""]
        
        analysis_results = results.get("analysis_results", {})
        overall = results.get("overall_analysis", {}).get("output", {})
        
        # 基本统计
        lines.append("## 📊 基本统计")
        lines.append(f"- 论文总数: {len(analysis_results)}")
        
        if overall.get("difficulty_distribution"):
            lines.append("- 难度分布:")
            for data in overall["difficulty_distribution"]:
                level = data['level']
                count = data['count']
                lines.append(f"  - {level}: {count} 篇")
        
        if overall.get("total_estimated_time"):
            lines.append(f"- 总学习时间: {overall['total_estimated_time']} 分钟")
        
        lines.append("")
        
        # 推荐学习顺序
        if overall.get("recommended_order"):
            lines.append("## 📋 推荐学习顺序")
            for i, paper_id in enumerate(overall["recommended_order"], 1):
                if paper_id in analysis_results:
                    title = analysis_results[paper_id]["output"]["title"]
                    difficulty = analysis_results[paper_id]["output"]["difficulty_level"]
                    time = analysis_results[paper_id]["output"]["reading_time_estimate"]
                    lines.append(f"{i}. **{title}** ({difficulty}, {time}分钟)")
            lines.append("")
        
        # 核心概念
        if overall.get("common_concepts"):
            lines.append("## 🎯 核心概念")
            for concept in overall["common_concepts"][:10]:
                lines.append(f"- {concept}")
            lines.append("")
        
        # 学习建议
        if overall.get("learning_suggestions"):
            lines.append("## 💡 学习建议")
            for suggestion in overall["learning_suggestions"]:
                lines.append(f"- {suggestion}")
            lines.append("")
        
        return "\n".join(lines)

# 便捷函数
async def analyze_papers_directory(input_dir: str, output_dir: str = None) -> Dict[str, Any]:
    """便捷函数：分析论文目录"""
    analyzer = PaperAnalysisor()
    results = await analyzer.analyze_papers(input_dir)
    
    if output_dir:
        analyzer.save_analysis_results(results, output_dir)
    
    return results

if __name__ == "__main__":
    # 测试代码
    async def test():
        analyzer = PaperAnalysisor()
        print("✅ PaperAnalysisor 初始化完成")
    
    asyncio.run(test()) 