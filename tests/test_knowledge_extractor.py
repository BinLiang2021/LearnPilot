"""
KnowledgeExtractor 实际运行测试
测试概念提取器的功能，使用 Attention Is All You Need 论文作为案例
"""

import asyncio
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.learn_pilot.agents.knowledge_extractor import KnowledgeExtractor, extract_concepts_from_papers
from src.learn_pilot.literature_utils.markdown_parser import parse_papers_from_directory
import logging

logging.basicConfig(level=logging.INFO)

async def test_knowledge_extractor():
    """测试概念提取器"""
    print("🧠 测试 KnowledgeExtractor")
    print("=" * 50)
    
    # 设置路径
    input_dir = "tests/test_marldown_folder"
    output_dir = "tests/outputs/knowledge_extraction"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 首先解析论文
        print("📖 解析论文文件...")
        papers = parse_papers_from_directory(input_dir)
        
        if not papers:
            print("❌ 没有找到论文文件")
            return None
        
        print(f"✅ 成功解析 {len(papers)} 篇论文")
        for i, paper in enumerate(papers, 1):
            print(f"   {i}. {paper.title}")
        
        # 方法1：使用便捷函数
        print("\n🔍 方法1: 使用便捷函数 extract_concepts_from_papers")
        results = await extract_concepts_from_papers(papers, output_dir)
        
        print("\n✅ 概念提取完成！结果概览:")
        print(f"📊 处理论文数量: {len(results.get('extractions', {}))}")
        
        # 展示第一篇论文的概念提取结果
        extractions = results.get('extractions', {})
        if extractions:
            first_paper_id = list(extractions.keys())[0]
            first_extraction = extractions[first_paper_id]['output']
            
            print(f"\n📖 论文概念提取详情:")
            print(f"   - 难度评估: {first_extraction['difficulty_assessment']}")
            print(f"   - 概念复杂度: {first_extraction['conceptual_complexity']}")
            print(f"   - 学习时间估算: {first_extraction['estimated_learning_time']} 分钟")
            print(f"   - 知识领域: {', '.join(first_extraction['knowledge_domains'])}")
            
            print(f"\n🎯 核心概念 ({len(first_extraction['core_concepts'])} 个):")
            for i, concept in enumerate(first_extraction['core_concepts'][:8], 1):
                print(f"   {i:2d}. {concept}")
            
            print(f"\n🔗 支撑概念 ({len(first_extraction['supporting_concepts'])} 个):")
            for i, concept in enumerate(first_extraction['supporting_concepts'][:5], 1):
                print(f"   {i:2d}. {concept}")
            
            print(f"\n📚 前置知识需求 ({len(first_extraction['prerequisites'])} 项):")
            for i, prereq in enumerate(first_extraction['prerequisites'][:5], 1):
                print(f"   {i:2d}. {prereq['name']} ({prereq['level']}) - {prereq['reason'][:50]}...")
            
            print(f"\n🔀 概念关系 ({len(first_extraction['concept_relationships'])} 个):")
            for i, rel in enumerate(first_extraction['concept_relationships'][:3], 1):
                print(f"   {i}. {rel['concept1']} --{rel['relationship']}--> {rel['concept2']}")
        
        # 展示跨论文分析结果
        cross_analysis = results.get('cross_paper_analysis', {}).get('output', {})
        if cross_analysis:
            print(f"\n🌐 跨论文概念分析:")
            
            if cross_analysis.get('common_concepts'):
                print(f"   - 共同概念 ({len(cross_analysis['common_concepts'])} 个):")
                for concept in cross_analysis['common_concepts'][:5]:
                    print(f"     • {concept}")
            
            if cross_analysis.get('concept_hierarchy'):
                print(f"   - 概念层次结构:")
                hierarchy = cross_analysis['concept_hierarchy']
                for level, concepts in hierarchy.items():
                    print(f"     • {level}: {len(concepts)} 个概念")
                    for concept in concepts[:3]:
                        print(f"       - {concept}")
            
            if cross_analysis.get('recommended_sequence'):
                print(f"   - 推荐学习顺序: {cross_analysis['recommended_sequence']}")
            
            if cross_analysis.get('concept_clusters'):
                print(f"   - 概念聚类 ({len(cross_analysis['concept_clusters'])} 个集群):")
                for cluster_name, concepts in list(cross_analysis['concept_clusters'].items())[:3]:
                    print(f"     • {cluster_name}: {len(concepts)} 个概念")
                    for concept in concepts[:2]:
                        print(f"       - {concept}")
        
        print(f"\n💾 详细结果已保存到: {output_dir}")
        
        # 计算资源使用
        total_cost = 0
        total_tokens = 0
        for paper_id, extraction in extractions.items():
            usage = extraction.get('usage', {})
            total_cost += usage.get('estimated_cost_usd', 0)
            total_tokens += usage.get('total_tokens', 0)
        
        # 加上跨论文分析的成本
        if results.get('cross_paper_analysis', {}).get('usage'):
            cross_usage = results['cross_paper_analysis']['usage']
            total_cost += cross_usage.get('estimated_cost_usd', 0)
            total_tokens += cross_usage.get('total_tokens', 0)
        
        print(f"\n💰 资源使用统计:")
        print(f"   - 总token数: {total_tokens:,}")
        print(f"   - 预估成本: ${total_cost:.4f}")
        
        return results
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_single_paper_extraction():
    """测试单篇论文的详细概念提取"""
    print("\n" + "="*50)
    print("🔬 详细单篇论文概念提取测试")
    print("="*50)
    
    try:
        # 解析论文
        papers = parse_papers_from_directory("tests/test_marldown_folder")
        if not papers:
            print("❌ 没有找到论文文件")
            return
        
        paper = papers[0]  # 取第一篇论文
        print(f"📖 分析论文: {paper.title}")
        
        # 创建提取器并分析
        extractor = KnowledgeExtractor()
        result = await extractor._extract_concepts_from_paper(paper)
        
        extraction = result['output']
        usage = result['usage']
        
        print(f"\n📊 详细概念提取结果:")
        print(f"   - 难度评估: {extraction['difficulty_assessment']}")
        print(f"   - 概念复杂度: {extraction['conceptual_complexity']}")
        print(f"   - 学习时间: {extraction['estimated_learning_time']} 分钟")
        
        print(f"\n🌐 知识领域 ({len(extraction['knowledge_domains'])} 个):")
        for i, domain in enumerate(extraction['knowledge_domains'], 1):
            print(f"   {i:2d}. {domain}")
        
        print(f"\n🎯 核心概念 ({len(extraction['core_concepts'])} 个):")
        for i, concept in enumerate(extraction['core_concepts'], 1):
            print(f"   {i:2d}. {concept}")
        
        print(f"\n🔗 支撑概念 ({len(extraction['supporting_concepts'])} 个):")
        for i, concept in enumerate(extraction['supporting_concepts'], 1):
            print(f"   {i:2d}. {concept}")
        
        print(f"\n📚 前置知识 ({len(extraction['prerequisites'])} 个):")
        for i, prereq in enumerate(extraction['prerequisites'], 1):
            print(f"   {i:2d}. [{prereq['level']}] {prereq['name']}")
            print(f"        理由: {prereq['reason']}")
        
        print(f"\n🔀 概念关系 ({len(extraction['concept_relationships'])} 个):")
        for i, rel in enumerate(extraction['concept_relationships'], 1):
            print(f"   {i:2d}. {rel['concept1']} --[{rel['relationship']}]--> {rel['concept2']}")
        
        print(f"\n💰 本次提取资源使用:")
        print(f"   - 输入tokens: {usage['input_tokens']:,}")
        print(f"   - 输出tokens: {usage['output_tokens']:,}")
        print(f"   - 总tokens: {usage['total_tokens']:,}")
        print(f"   - 预估成本: ${usage['estimated_cost_usd']:.4f}")
        
    except Exception as e:
        print(f"❌ 详细提取测试失败: {e}")
        import traceback
        traceback.print_exc()

async def test_cross_paper_analysis():
    """测试跨论文分析功能"""
    print("\n" + "="*50)
    print("🔀 跨论文概念关系分析测试")
    print("="*50)
    
    try:
        # 解析论文
        papers = parse_papers_from_directory("tests/test_marldown_folder")
        if not papers:
            print("❌ 没有找到论文文件")
            return
        
        # 创建提取器
        extractor = KnowledgeExtractor()
        
        # 先提取各论文的概念
        print("🔍 为每篇论文提取概念...")
        extractions = {}
        for i, paper in enumerate(papers):
            paper_id = f"paper_{i+1}"
            print(f"   处理 {paper_id}: {paper.title}")
            result = await extractor._extract_concepts_from_paper(paper)
            extractions[paper_id] = result
        
        print(f"✅ 完成 {len(extractions)} 篇论文的概念提取")
        
        # 进行跨论文分析
        print("\n🌐 执行跨论文概念关系分析...")
        cross_result = await extractor._analyze_cross_paper_concepts(extractions)
        
        analysis = cross_result['output']
        usage = cross_result['usage']
        
        print(f"\n📊 跨论文分析结果:")
        
        print(f"\n🎯 共同概念 ({len(analysis['common_concepts'])} 个):")
        for i, concept in enumerate(analysis['common_concepts'], 1):
            print(f"   {i:2d}. {concept}")
        
        print(f"\n📊 概念层次结构:")
        hierarchy = analysis['concept_hierarchy']
        for level, concepts in hierarchy.items():
            print(f"   📈 {level.upper()} ({len(concepts)} 个):")
            for concept in concepts[:5]:
                print(f"      • {concept}")
        
        print(f"\n📚 推荐学习顺序:")
        for i, paper_id in enumerate(analysis['recommended_sequence'], 1):
            print(f"   {i}. {paper_id}")
        
        print(f"\n🔗 论文依赖关系 ({len(analysis['learning_dependencies'])} 个):")
        for i, dep in enumerate(analysis['learning_dependencies'], 1):
            print(f"   {i}. {dep['prerequisite_paper']} → {dep['dependent_paper']}")
            print(f"      原因: {dep['reason']}")
        
        print(f"\n🎭 概念聚类 ({len(analysis['concept_clusters'])} 个集群):")
        for cluster_name, concepts in analysis['concept_clusters'].items():
            print(f"   📁 {cluster_name} ({len(concepts)} 个概念):")
            for concept in concepts[:4]:
                print(f"      • {concept}")
        
        print(f"\n🕸️ 知识图谱边 ({len(analysis['knowledge_graph_edges'])} 条):")
        for i, edge in enumerate(analysis['knowledge_graph_edges'][:8], 1):
            print(f"   {i:2d}. {edge['from']} --[{edge['relation']}]--> {edge['to']}")
        
        print(f"\n💰 跨论文分析资源使用:")
        print(f"   - 输入tokens: {usage['input_tokens']:,}")
        print(f"   - 输出tokens: {usage['output_tokens']:,}")
        print(f"   - 总tokens: {usage['total_tokens']:,}")
        print(f"   - 预估成本: ${usage['estimated_cost_usd']:.4f}")
        
    except Exception as e:
        print(f"❌ 跨论文分析测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 开始 KnowledgeExtractor 功能测试")
    
    # 运行基本测试
    results = asyncio.run(test_knowledge_extractor())
    
    # 运行详细测试
    asyncio.run(test_single_paper_extraction())
    
    # 运行跨论文分析测试
    asyncio.run(test_cross_paper_analysis())
    
    print("\n🎉 KnowledgeExtractor 测试完成！")
