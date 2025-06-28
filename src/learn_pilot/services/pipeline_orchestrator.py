"""
Pipeline Orchestrator
流水线编排器，协调各个Agent的执行
"""

import logging
import asyncio
from typing import Dict, Any, Optional
import os

from src.learn_pilot.agents.paper_analysisor import PaperAnalysisor
from src.learn_pilot.agents.knowledge_extractor import KnowledgeExtractor

logger = logging.getLogger(__name__)

class PipelineOrchestrator:
    """AI-Paper-Tutor 流水线编排器"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        
        # 初始化Agent
        self.paper_analysisor = PaperAnalysisor(config)
        self.knowledge_extractor = KnowledgeExtractor(config)
        
    async def run_full_pipeline(self, input_dir: str, output_dir: str, 
                               user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """运行完整的AI-Paper-Tutor流水线"""
        try:
            self.logger.info("🚀 启动完整AI-Paper-Tutor流水线")
            
            # 确保输出目录存在
            os.makedirs(output_dir, exist_ok=True)
            
            results = {}
            
            # Step 1: 论文分析
            self.logger.info("📊 Step 1: 论文分析")
            analysis_results = await self.paper_analysisor.analyze_papers(input_dir)
            results['analysis'] = analysis_results
            self.paper_analysisor.save_analysis_results(analysis_results, 
                                                       os.path.join(output_dir, "analysis"))
            
            # Step 2: 概念提取
            self.logger.info("🧠 Step 2: 概念提取")
            papers = analysis_results.get('papers', [])
            if papers:
                extraction_results = await self.knowledge_extractor.extract_concepts_from_papers(papers)
                results['extraction'] = extraction_results
                self.knowledge_extractor.save_extraction_results(extraction_results, 
                                                                os.path.join(output_dir, "extraction"))
            
            # Step 3: 生成整体报告
            self.logger.info("📝 Step 3: 生成整体报告")
            overall_report = self._generate_pipeline_report(results, user_preferences)
            
            # 保存整体报告
            report_file = os.path.join(output_dir, "pipeline_report.md")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(overall_report)
            
            results['pipeline_report'] = overall_report
            results['output_dir'] = output_dir
            
            self.logger.info("✅ AI-Paper-Tutor流水线执行完成!")
            return results
            
        except Exception as e:
            self.logger.error(f"❌ 流水线执行失败: {e}")
            raise
    
    async def run_single_step(self, step_name: str, input_dir: str, output_dir: str, 
                             user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
        """运行单个步骤"""
        try:
            self.logger.info(f"🔄 执行单步骤: {step_name}")
            
            os.makedirs(output_dir, exist_ok=True)
            
            if step_name == "analysis":
                results = await self.paper_analysisor.analyze_papers(input_dir)
                self.paper_analysisor.save_analysis_results(results, output_dir)
                return results
                
            elif step_name == "extraction":
                # 需要先运行分析步骤
                analysis_results = await self.paper_analysisor.analyze_papers(input_dir)
                papers = analysis_results.get('papers', [])
                results = await self.knowledge_extractor.extract_concepts_from_papers(papers)
                self.knowledge_extractor.save_extraction_results(results, output_dir)
                return results
                
            else:
                raise ValueError(f"未知的步骤: {step_name}")
                
        except Exception as e:
            self.logger.error(f"❌ 单步骤执行失败 {step_name}: {e}")
            raise
    
    def _generate_pipeline_report(self, results: Dict[str, Any], 
                                user_preferences: Dict[str, Any] = None) -> str:
        """生成流水线整体报告"""
        lines = ["# 🎓 AI-Paper-Tutor 学习报告", ""]
        
        user_prefs = user_preferences or {}
        
        # 用户配置
        lines.append("## 👤 学习配置")
        lines.append(f"- 学习水平: {user_prefs.get('user_level', '中级')}")
        lines.append(f"- 每日时间: {user_prefs.get('daily_hours', 2)} 小时")
        lines.append(f"- 学习天数: {user_prefs.get('total_days', 7)} 天")
        lines.append(f"- 学习目标: {user_prefs.get('learning_goals', '深入理解论文核心概念')}")
        lines.append("")
        
        # 论文分析摘要
        analysis = results.get('analysis', {})
        if analysis.get('analysis_results'):
            lines.append("## 📚 论文概览")
            analysis_results = analysis['analysis_results']
            lines.append(f"- 论文总数: {len(analysis_results)}")
            
            # 难度分布
            difficulties = [r['output']['difficulty_level'] for r in analysis_results.values()]
            difficulty_count = {d: difficulties.count(d) for d in set(difficulties)}
            lines.append("- 难度分布:")
            for level, count in difficulty_count.items():
                lines.append(f"  - {level}: {count} 篇")
            
            # 总学习时间
            total_time = sum(r['output']['reading_time_estimate'] for r in analysis_results.values())
            lines.append(f"- 总预估学习时间: {total_time} 分钟 ({total_time/60:.1f} 小时)")
            lines.append("")
        
        # 概念提取摘要
        extraction = results.get('extraction', {})
        if extraction.get('extractions'):
            lines.append("## 🧠 核心概念")
            extractions = extraction['extractions']
            
            # 统计所有核心概念
            all_concepts = []
            for e in extractions.values():
                all_concepts.extend(e['output']['core_concepts'])
            
            # 概念频次统计
            concept_count = {}
            for concept in all_concepts:
                concept_count[concept] = concept_count.get(concept, 0) + 1
            
            # 显示高频概念
            top_concepts = sorted(concept_count.items(), key=lambda x: x[1], reverse=True)[:10]
            lines.append("### 🎯 高频核心概念")
            for concept, count in top_concepts:
                lines.append(f"- **{concept}** (出现 {count} 次)")
            lines.append("")
            
            # 显示知识领域
            all_domains = []
            for e in extractions.values():
                all_domains.extend(e['output']['knowledge_domains'])
            
            domain_count = {}
            for domain in all_domains:
                domain_count[domain] = domain_count.get(domain, 0) + 1
            
            lines.append("### 🌐 涉及领域")
            for domain, count in sorted(domain_count.items(), key=lambda x: x[1], reverse=True)[:5]:
                lines.append(f"- {domain} ({count} 篇论文)")
            lines.append("")
        
        # 学习建议
        lines.append("## 💡 学习建议")
        
        # 基于分析结果生成建议
        if analysis.get('overall_analysis', {}).get('output', {}).get('learning_suggestions'):
            suggestions = analysis['overall_analysis']['output']['learning_suggestions']
            for suggestion in suggestions[:5]:
                lines.append(f"- {suggestion}")
        else:
            # 默认建议
            lines.append("- 建议按照推荐顺序逐步学习")
            lines.append("- 重点关注高频核心概念的理解")
            lines.append("- 每篇论文学习后进行概念总结")
            lines.append("- 定期复习前置知识点")
        
        lines.append("")
        
        # 推荐学习路径
        if analysis.get('overall_analysis', {}).get('output', {}).get('recommended_order'):
            lines.append("## 📋 推荐学习路径")
            recommended_order = analysis['overall_analysis']['output']['recommended_order']
            analysis_results = analysis.get('analysis_results', {})
            
            for i, paper_id in enumerate(recommended_order, 1):
                if paper_id in analysis_results:
                    paper_analysis = analysis_results[paper_id]['output']
                    lines.append(f"### 第{i}步: {paper_analysis['title']}")
                    lines.append(f"- **难度**: {paper_analysis['difficulty_level']}")
                    lines.append(f"- **学习时间**: {paper_analysis['reading_time_estimate']} 分钟")
                    lines.append(f"- **核心概念**: {', '.join(paper_analysis['core_concepts'][:3])}")
                    lines.append(f"- **学习重点**: {paper_analysis['main_method']}")
                    lines.append("")
        
        # 文件位置说明
        lines.append("## 📁 输出文件说明")
        lines.append("- `analysis/` - 论文分析详细结果")
        lines.append("- `extraction/` - 概念提取和知识图谱")
        lines.append("- `pipeline_report.md` - 本学习报告")
        lines.append("")
        
        lines.append("---")
        lines.append("*由 AI-Paper-Tutor 自动生成*")
        
        return "\n".join(lines)

# 便捷函数
async def run_paper_tutor_pipeline(input_dir: str, output_dir: str, 
                                  user_preferences: Dict[str, Any] = None) -> Dict[str, Any]:
    """便捷函数：运行完整的论文学习辅导流水线"""
    orchestrator = PipelineOrchestrator()
    return await orchestrator.run_full_pipeline(input_dir, output_dir, user_preferences)

if __name__ == "__main__":
    # 测试代码
    async def test():
        orchestrator = PipelineOrchestrator()
        print("✅ PipelineOrchestrator 初始化完成")
    
    asyncio.run(test())
