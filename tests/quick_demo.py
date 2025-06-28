"""
AI-Paper-Tutor 快速演示
快速展示系统的核心功能，适合演示和快速验证
"""

import asyncio
import sys
import os
from pathlib import Path
import time

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.learn_pilot.agents.paper_analysisor import PaperAnalysisor
from src.learn_pilot.agents.knowledge_extractor import KnowledgeExtractor
from src.learn_pilot.services.pipeline_orchestrator import PipelineOrchestrator
from src.learn_pilot.literature_utils.markdown_parser import parse_papers_from_directory

def print_demo_banner():
    """打印演示横幅"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                   🎓 AI-Paper-Tutor 快速演示                   ║
║                                                                ║
║  体验智能论文学习助手的核心功能                                  ║
║  📖 论文解析 → 🧠 概念提取 → 📋 学习规划                        ║
║                                                                ║
║  演示案例: Attention Is All You Need (Transformer论文)          ║
╚════════════════════════════════════════════════════════════════╝
"""
    print(banner)

async def demo_paper_parsing():
    """演示论文解析功能"""
    print("🔍 演示1: 论文解析与基本信息提取")
    print("-" * 50)
    
    try:
        # 解析论文
        papers = parse_papers_from_directory("tests/test_marldown_folder")
        
        if not papers:
            print("❌ 没有找到论文文件")
            return None
        
        paper = papers[0]
        
        print(f"📖 论文标题: {paper.title}")
        print(f"👥 作者数量: {len(paper.authors)}")
        print(f"📝 摘要长度: {len(paper.abstract)} 字符")
        print(f"📑 章节数量: {len(paper.sections)}")
        
        print(f"\n📋 章节列表:")
        for i, section in enumerate(paper.sections[:5], 1):
            print(f"   {i}. {section.title} ({len(section.content)} 字符)")
        
        if len(paper.sections) > 5:
            print(f"   ... 还有 {len(paper.sections) - 5} 个章节")
        
        print(f"\n✅ 论文解析成功！")
        return paper
        
    except Exception as e:
        print(f"❌ 论文解析失败: {e}")
        return None

async def demo_paper_analysis(paper):
    """演示论文分析功能"""
    print(f"\n📊 演示2: 智能论文分析")
    print("-" * 50)
    
    try:
        analyzer = PaperAnalysisor()
        
        print("🤖 AI正在分析论文...")
        start_time = time.time()
        
        result = await analyzer._analyze_single_paper_with_llm(paper)
        
        end_time = time.time()
        analysis = result['output']
        usage = result['usage']
        
        print(f"✅ 分析完成! (耗时: {end_time - start_time:.1f}秒)")
        
        print(f"\n🎯 分析结果:")
        print(f"   📚 研究问题: {analysis['research_problem'][:80]}...")
        print(f"   🔬 主要方法: {analysis['main_method'][:80]}...")
        print(f"   📈 难度等级: {analysis['difficulty_level']}")
        print(f"   ⏱️  阅读时间: {analysis['reading_time_estimate']} 分钟")
        print(f"   🧩 技术复杂度: {analysis['technical_complexity']}")
        
        print(f"\n🏆 核心贡献 (前3项):")
        for i, contrib in enumerate(analysis['key_contributions'][:3], 1):
            print(f"   {i}. {contrib}")
        
        print(f"\n🎯 核心概念 (前5个):")
        for i, concept in enumerate(analysis['core_concepts'][:5], 1):
            print(f"   {i}. {concept}")
        
        print(f"\n💰 资源使用: {usage['total_tokens']:,} tokens, ${usage['estimated_cost_usd']:.4f}")
        
        return analysis
        
    except Exception as e:
        import traceback
        error_message = traceback.format_exc() 
        print(f"❌ 论文分析失败: \n{error_message}")
        return None

async def demo_concept_extraction(paper):
    """演示概念提取功能"""
    print(f"\n🧠 演示3: 概念提取与知识图谱")
    print("-" * 50)
    
    try:
        extractor = KnowledgeExtractor()
        
        print("🤖 AI正在提取概念...")
        start_time = time.time()
        
        result = await extractor._extract_concepts_from_paper(paper)
        
        end_time = time.time()
        extraction = result['output']
        usage = result['usage']
        
        print(f"✅ 提取完成! (耗时: {end_time - start_time:.1f}秒)")
        
        print(f"\n🎯 概念提取结果:")
        print(f"   📊 难度评估: {extraction['difficulty_assessment']}")
        print(f"   🧩 概念复杂度: {extraction['conceptual_complexity']}")
        print(f"   ⏱️  学习时间: {extraction['estimated_learning_time']} 分钟")
        
        print(f"\n🌐 知识领域:")
        for i, domain in enumerate(extraction['knowledge_domains'][:4], 1):
            print(f"   {i}. {domain}")
        
        print(f"\n🎯 核心概念 (前6个):")
        for i, concept in enumerate(extraction['core_concepts'][:6], 1):
            print(f"   {i}. {concept}")
        
        print(f"\n📚 前置知识需求 (前4个):")
        for i, prereq in enumerate(extraction['prerequisites'][:4], 1):
            print(f"   {i}. [{prereq['level']}] {prereq['name']}")
        
        print(f"\n🔗 概念关系 (前3个):")
        for i, rel in enumerate(extraction['concept_relationships'][:3], 1):
            print(f"   {i}. {rel['concept1']} --{rel['relationship']}--> {rel['concept2']}")
        
        print(f"\n💰 资源使用: {usage['total_tokens']:,} tokens, ${usage['estimated_cost_usd']:.4f}")
        
        return extraction
        
    except Exception as e:
        print(f"❌ 概念提取失败: {e}")
        return None

async def demo_quick_pipeline():
    """演示快速流水线"""
    print(f"\n🚀 演示4: 快速完整流水线")
    print("-" * 50)
    
    try:
        input_dir = "tests/test_marldown_folder"
        output_dir = "tests/outputs/quick_demo"
        
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 用户偏好
        user_preferences = {
            "user_level": "intermediate",
            "daily_hours": 2,
            "total_days": 5,
            "learning_goals": "快速理解Transformer架构"
        }
        
        print("🤖 启动完整流水线...")
        print("👤 用户配置: 中级水平, 每日2小时, 5天完成")
        
        orchestrator = PipelineOrchestrator()
        start_time = time.time()
        
        results = await orchestrator.run_full_pipeline(
            input_dir=input_dir,
            output_dir=output_dir,
            user_preferences=user_preferences
        )
        
        end_time = time.time()
        
        print(f"✅ 流水线完成! (总耗时: {end_time - start_time:.1f}秒)")
        
        # 展示关键结果
        analysis = results.get('analysis', {})
        extraction = results.get('extraction', {})
        
        if analysis and analysis.get('analysis_results'):
            analysis_result = list(analysis['analysis_results'].values())[0]['output']
            print(f"\n📊 论文分析: {analysis_result['difficulty_level']} 难度，{analysis_result['reading_time_estimate']}分钟")
        
        if extraction and extraction.get('extractions'):
            extraction_result = list(extraction['extractions'].values())[0]['output']
            print(f"🧠 概念提取: {len(extraction_result['core_concepts'])} 个核心概念")
        
        # 计算总成本
        total_cost = 0
        total_tokens = 0
        
        if analysis and analysis.get('analysis_results'):
            for result in analysis['analysis_results'].values():
                usage = result.get('usage', {})
                total_cost += usage.get('estimated_cost_usd', 0)
                total_tokens += usage.get('total_tokens', 0)
        
        if extraction and extraction.get('extractions'):
            for result in extraction['extractions'].values():
                usage = result.get('usage', {})
                total_cost += usage.get('estimated_cost_usd', 0)
                total_tokens += usage.get('total_tokens', 0)
        
        print(f"\n💰 总资源使用: {total_tokens:,} tokens, ${total_cost:.4f}")
        print(f"💾 完整结果保存在: {output_dir}")
        
        return results
        
    except Exception as e:
        import traceback
        error_message = traceback.format_exc() 
        print(f"❌ 流水线演示失败: \n{error_message}")
        return None

def demo_summary():
    """演示总结"""
    print(f"\n🎉 演示总结")
    print("=" * 60)
    
    summary = """
💡 AI-Paper-Tutor 核心功能展示完成！

✨ 已演示的功能:
   📖 智能论文解析 - 自动提取标题、作者、章节结构
   📊 深度内容分析 - 研究问题、方法、贡献、难度评估
   🧠 概念知识提取 - 核心概念、前置知识、概念关系
   🚀 完整学习流水线 - 一站式论文学习方案生成

🎯 系统优势:
   🤖 LLM智能驱动 - 深度理解论文内容
   🔄 模块化设计 - 可单独使用各个功能
   📋 个性化适配 - 根据用户水平调整建议
   💰 成本透明 - 实时显示资源使用情况

🚀 下一步:
   • 查看 tests/outputs/ 中的详细结果
   • 使用 python -m src.learn_pilot.main 运行完整系统
   • 尝试分析你自己的论文！
"""
    print(summary)

async def main():
    """主演示函数"""
    print_demo_banner()
    
    print("🔧 检查演示环境...")
    
    # 检查输入文件
    input_dir = Path("tests/test_marldown_folder")
    if not input_dir.exists() or not list(input_dir.glob("*.md")):
        print("❌ 没有找到演示用的论文文件")
        print("请确保 tests/test_marldown_folder/ 目录下有Markdown格式的论文")
        return
    
    print("✅ 演示环境就绪，开始演示...\n")
    
    # 运行演示
    total_start = time.time()
    
    # 演示1: 论文解析
    paper = await demo_paper_parsing()
    if not paper:
        return
    
    # 演示2: 论文分析
    # analysis = await demo_paper_analysis(paper)
    
    # 演示3: 概念提取
    # extraction = await demo_concept_extraction(paper)
    
    # 演示4: 快速流水线
    pipeline_result = await demo_quick_pipeline()
    
    total_end = time.time()
    
    print(f"\n⏱️  总演示时间: {total_end - total_start:.1f} 秒")
    
    # 演示总结
    demo_summary()

if __name__ == "__main__":
    # 减少日志噪音
    import logging
    logging.basicConfig(level=logging.ERROR)
    
    print("🚀 启动 AI-Paper-Tutor 快速演示...")
    asyncio.run(main()) 