"""
PaperAnalysisor 实际运行测试
测试论文分析器的功能，使用 Attention Is All You Need 论文作为案例
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.learn_pilot.agents.paper_analysisor import PaperAnalysisor, analyze_papers_directory
import logging

logging.basicConfig(level=logging.INFO)

async def test_paper_analysisor():
    """测试论文分析器"""
    print("🔍 测试 PaperAnalysisor")
    print("=" * 50)
    
    # 设置路径
    input_dir = "tests/test_marldown_folder"
    output_dir = "tests/outputs/paper_analysis"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 方法1：直接使用便捷函数
        print("\n📝 方法1: 使用便捷函数 analyze_papers_directory")
        results = await analyze_papers_directory(input_dir, output_dir)
        
        print("\n✅ 分析完成！结果概览:")
        print(f"📊 分析的论文数量: {len(results.get('papers', []))}")
        print(f"📋 分析结果: {len(results.get('analysis_results', {}))}")
        
        # 展示第一篇论文的分析结果
        analysis_results = results.get('analysis_results', {})
        if analysis_results:
            first_paper_id = list(analysis_results.keys())[0]
            first_result = analysis_results[first_paper_id]['output']
            
            print(f"\n📖 论文《{first_result['title']}》分析结果:")
            print(f"   - 研究问题: {first_result['research_problem'][:100]}...")
            print(f"   - 主要方法: {first_result['main_method'][:100]}...")
            print(f"   - 难度等级: {first_result['difficulty_level']}")
            print(f"   - 阅读时间估算: {first_result['reading_time_estimate']} 分钟")
            print(f"   - 技术复杂度: {first_result['technical_complexity']}")
            print(f"   - 核心概念数量: {len(first_result['core_concepts'])}")
            print(f"   - 前置知识数量: {len(first_result['prerequisites'])}")
            
            print(f"\n🎯 前5个核心概念:")
            for i, concept in enumerate(first_result['core_concepts'][:5], 1):
                print(f"   {i}. {concept}")
            
            print(f"\n📚 前3个前置知识:")
            for i, prereq in enumerate(first_result['prerequisites'][:3], 1):
                print(f"   {i}. {prereq}")
        
        # 展示整体分析
        overall = results.get('overall_analysis', {}).get('output', {})
        if overall:
            print(f"\n📈 整体分析:")
            if overall.get('difficulty_distribution'):
                print(f"   - 难度分布: {overall['difficulty_distribution']}")
            if overall.get('total_estimated_time'):
                print(f"   - 总学习时间: {overall['total_estimated_time']} 分钟")
            if overall.get('recommended_order'):
                print(f"   - 推荐学习顺序: {overall['recommended_order']}")
        
        print(f"\n💾 详细结果已保存到: {output_dir}")
        
        # 方法2：直接使用类实例
        print("\n📝 方法2: 直接使用 PaperAnalysisor 类")
        analyzer = PaperAnalysisor()
        results2 = await analyzer.analyze_papers(input_dir)
        
        print(f"✅ 第二次分析完成，论文数量: {len(results2.get('papers', []))}")
        
        # 测试 token 使用情况
        total_cost = 0
        total_tokens = 0
        for paper_id, result in results.get('analysis_results', {}).items():
            usage = result.get('usage', {})
            total_cost += usage.get('estimated_cost_usd', 0)
            total_tokens += usage.get('total_tokens', 0)
        
        print(f"\n💰 资源使用统计:")
        print(f"   - 总token数: {total_tokens:,}")
        print(f"   - 预估成本: ${total_cost:.4f}")
        
        return results
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_single_paper_analysis():
    """测试单篇论文分析的详细输出"""
    print("\n" + "="*50)
    print("🔬 详细单篇论文分析测试")
    print("="*50)
    
    try:
        from src.learn_pilot.literature_utils.markdown_parser import parse_papers_from_directory
        from src.learn_pilot.agents.paper_analysisor import PaperAnalysisor
        
        # 解析论文
        papers = parse_papers_from_directory("tests/test_marldown_folder")
        if not papers:
            print("❌ 没有找到论文文件")
            return
        
        paper = papers[0]  # 取第一篇论文
        print(f"📖 分析论文: {paper.title}")
        print(f"📝 摘要长度: {len(paper.abstract)} 字符")
        print(f"📑 章节数量: {len(paper.sections)}")
        
        # 创建分析器并分析
        analyzer = PaperAnalysisor()
        result = await analyzer._analyze_single_paper_with_llm(paper)
        
        analysis = result['output']
        usage = result['usage']
        
        print(f"\n📊 详细分析结果:")
        print(f"   - 标题: {analysis['title']}")
        print(f"   - 作者: {', '.join(analysis['authors'])}")
        print(f"   - 研究问题: {analysis['research_problem']}")
        print(f"   - 主要方法: {analysis['main_method']}")
        
        print(f"\n🎯 核心概念 ({len(analysis['core_concepts'])} 个):")
        for i, concept in enumerate(analysis['core_concepts'], 1):
            print(f"   {i:2d}. {concept}")
        
        print(f"\n📚 前置知识 ({len(analysis['prerequisites'])} 个):")
        for i, prereq in enumerate(analysis['prerequisites'], 1):
            print(f"   {i:2d}. {prereq}")
        
        print(f"\n🏆 关键贡献:")
        for i, contrib in enumerate(analysis['key_contributions'], 1):
            print(f"   {i}. {contrib}")
        
        print(f"\n📖 章节摘要:")
        for section, summary in analysis['section_summary'].items():
            print(f"   - {section}: {summary[:100]}...")
        
        print(f"\n💰 本次分析资源使用:")
        print(f"   - 输入tokens: {usage['input_tokens']:,}")
        print(f"   - 输出tokens: {usage['output_tokens']:,}")
        print(f"   - 总tokens: {usage['total_tokens']:,}")
        print(f"   - 预估成本: ${usage['estimated_cost_usd']:.4f}")
        
    except Exception as e:
        print(f"❌ 详细分析测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 开始 PaperAnalysisor 功能测试")
    
    # 运行基本测试
    results = asyncio.run(test_paper_analysisor())
    
    # 运行详细测试
    asyncio.run(test_single_paper_analysis())
    
    print("\n🎉 PaperAnalysisor 测试完成！")
