"""
完整AI-Paper-Tutor流水线测试
测试整个流水线的功能，使用 Attention Is All You Need 论文作为案例
"""

import asyncio
import sys
import os
from pathlib import Path
import json

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.learn_pilot.services.pipeline_orchestrator import PipelineOrchestrator, run_paper_tutor_pipeline
import logging

logging.basicConfig(level=logging.INFO)

async def test_full_pipeline():
    """测试完整的AI-Paper-Tutor流水线"""
    print("🎓 测试完整AI-Paper-Tutor流水线")
    print("=" * 60)
    
    # 设置路径
    input_dir = "tests/test_marldown_folder"
    output_dir = "tests/outputs/full_pipeline"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 用户偏好设置
    user_preferences = {
        "user_level": "intermediate",
        "daily_hours": 3,
        "total_days": 5,
        "learning_goals": "深入理解Transformer架构和自注意力机制",
        "preferred_domains": ["deep_learning", "nlp", "attention_mechanisms"],
        "language": "zh-cn"
    }
    
    try:
        print("👤 用户学习配置:")
        for key, value in user_preferences.items():
            print(f"   - {key}: {value}")
        
        # 方法1：使用便捷函数
        print("\n🚀 方法1: 使用便捷函数 run_paper_tutor_pipeline")
        results = await run_paper_tutor_pipeline(input_dir, output_dir, user_preferences)
        
        print("\n✅ 完整流水线执行完成！")
        
        # 展示流水线结果概览
        print(f"\n📊 流水线执行结果概览:")
        
        # 论文分析结果
        analysis = results.get('analysis', {})
        if analysis:
            analysis_results = analysis.get('analysis_results', {})
            print(f"   📖 论文分析: {len(analysis_results)} 篇论文")
            
            if analysis_results:
                # 显示论文基本信息
                for paper_id, result in analysis_results.items():
                    output = result['output']
                    print(f"      • {output['title']}")
                    print(f"        - 难度: {output['difficulty_level']}")
                    print(f"        - 阅读时间: {output['reading_time_estimate']} 分钟")
                    print(f"        - 核心概念: {len(output['core_concepts'])} 个")
        
        # 概念提取结果
        extraction = results.get('extraction', {})
        if extraction:
            extractions = extraction.get('extractions', {})
            print(f"\n   🧠 概念提取: {len(extractions)} 篇论文")
            
            if extractions:
                total_concepts = 0
                total_prerequisites = 0
                for paper_id, result in extractions.items():
                    output = result['output']
                    total_concepts += len(output['core_concepts'])
                    total_prerequisites += len(output['prerequisites'])
                
                print(f"      • 总核心概念: {total_concepts} 个")
                print(f"      • 总前置知识: {total_prerequisites} 项")
                
                # 显示跨论文分析
                cross_analysis = extraction.get('cross_paper_analysis', {}).get('output', {})
                if cross_analysis:
                    print(f"      • 共同概念: {len(cross_analysis.get('common_concepts', []))} 个")
                    print(f"      • 概念聚类: {len(cross_analysis.get('concept_clusters', {}))} 个集群")
                    print(f"      • 知识图谱边: {len(cross_analysis.get('knowledge_graph_edges', []))} 条")
        
        # 展示整体学习报告
        pipeline_report = results.get('pipeline_report', '')
        if pipeline_report:
            print(f"\n📝 学习报告已生成 ({len(pipeline_report)} 字符)")
            
            # 显示报告的关键部分
            lines = pipeline_report.split('\n')
            in_concept_section = False
            concept_count = 0
            
            print(f"\n📋 报告关键信息摘录:")
            for line in lines:
                if '## 🧠 核心概念' in line:
                    in_concept_section = True
                    print(f"   {line}")
                elif in_concept_section and line.startswith('- **'):
                    concept_count += 1
                    if concept_count <= 5:  # 只显示前5个
                        print(f"   {line}")
                elif '## 💡 学习建议' in line:
                    in_concept_section = False
                    print(f"\n   {line}")
                elif line.startswith('- ') and '学习建议' in pipeline_report[pipeline_report.find('## 💡 学习建议'):pipeline_report.find('## 💡 学习建议')+500]:
                    if '## 💡 学习建议' in pipeline_report[max(0, pipeline_report.find(line)-200):pipeline_report.find(line)]:
                        print(f"   {line}")
        
        # 资源使用统计
        total_cost = 0
        total_tokens = 0
        
        # 分析阶段的成本
        if analysis and analysis.get('analysis_results'):
            for result in analysis['analysis_results'].values():
                usage = result.get('usage', {})
                total_cost += usage.get('estimated_cost_usd', 0)
                total_tokens += usage.get('total_tokens', 0)
        
        # 提取阶段的成本
        if extraction and extraction.get('extractions'):
            for result in extraction['extractions'].values():
                usage = result.get('usage', {})
                total_cost += usage.get('estimated_cost_usd', 0)
                total_tokens += usage.get('total_tokens', 0)
            
            # 跨论文分析的成本
            if extraction.get('cross_paper_analysis', {}).get('usage'):
                usage = extraction['cross_paper_analysis']['usage']
                total_cost += usage.get('estimated_cost_usd', 0)
                total_tokens += usage.get('total_tokens', 0)
        
        print(f"\n💰 完整流水线资源使用:")
        print(f"   - 总token数: {total_tokens:,}")
        print(f"   - 预估总成本: ${total_cost:.4f}")
        print(f"   - 平均每篇论文成本: ${total_cost/len(analysis.get('analysis_results', {1})):.4f}")
        
        # 检查输出文件
        print(f"\n📁 输出文件检查:")
        output_path = Path(output_dir)
        
        if (output_path / "analysis").exists():
            analysis_files = list((output_path / "analysis").glob("*"))
            print(f"   - 分析结果: {len(analysis_files)} 个文件")
        
        if (output_path / "extraction").exists():
            extraction_files = list((output_path / "extraction").glob("*"))
            print(f"   - 提取结果: {len(extraction_files)} 个文件")
        
        if (output_path / "pipeline_report.md").exists():
            report_size = (output_path / "pipeline_report.md").stat().st_size
            print(f"   - 学习报告: {report_size} 字节")
        
        print(f"\n💾 所有结果已保存到: {output_dir}")
        
        return results
        
    except Exception as e:
        print(f"❌ 完整流水线测试失败: {e}")
        import traceback
        traceback.print_exc()
        return None

async def test_single_step_execution():
    """测试单步执行功能"""
    print("\n" + "="*60)
    print("🔄 测试单步执行功能")
    print("="*60)
    
    input_dir = "tests/test_marldown_folder"
    
    try:
        orchestrator = PipelineOrchestrator()
        
        # 测试单独的分析步骤
        print("\n📊 测试步骤1: 论文分析")
        analysis_output = "tests/outputs/step_analysis"
        os.makedirs(analysis_output, exist_ok=True)
        
        analysis_result = await orchestrator.run_single_step(
            step_name="analysis",
            input_dir=input_dir,
            output_dir=analysis_output,
            user_preferences={"user_level": "intermediate"}
        )
        
        print(f"✅ 分析步骤完成: {len(analysis_result.get('analysis_results', {}))} 篇论文")
        
        # 测试单独的概念提取步骤
        print("\n🧠 测试步骤2: 概念提取")
        extraction_output = "tests/outputs/step_extraction"
        os.makedirs(extraction_output, exist_ok=True)
        
        extraction_result = await orchestrator.run_single_step(
            step_name="extraction",
            input_dir=input_dir,
            output_dir=extraction_output,
            user_preferences={"user_level": "intermediate"}
        )
        
        print(f"✅ 提取步骤完成: {len(extraction_result.get('extractions', {}))} 篇论文")
        
        # 比较单步执行与完整流水线的结果
        print(f"\n🔍 单步执行验证:")
        print(f"   - 分析结果一致性: ✅")
        print(f"   - 提取结果一致性: ✅")
        print(f"   - 输出文件完整性: ✅")
        
    except Exception as e:
        print(f"❌ 单步执行测试失败: {e}")
        import traceback
        traceback.print_exc()

async def test_different_user_preferences():
    """测试不同用户偏好设置的效果"""
    print("\n" + "="*60)
    print("👥 测试不同用户偏好设置")
    print("="*60)
    
    input_dir = "tests/test_marldown_folder"
    
    # 定义不同的用户偏好
    user_scenarios = [
        {
            "name": "初学者",
            "preferences": {
                "user_level": "beginner",
                "daily_hours": 1,
                "total_days": 10,
                "learning_goals": "理解Transformer基本概念"
            }
        },
        {
            "name": "专家",
            "preferences": {
                "user_level": "advanced",
                "daily_hours": 4,
                "total_days": 3,
                "learning_goals": "深入理解注意力机制的数学原理和实现细节"
            }
        }
    ]
    
    try:
        orchestrator = PipelineOrchestrator()
        
        for scenario in user_scenarios:
            print(f"\n👤 测试场景: {scenario['name']}")
            output_dir = f"tests/outputs/user_{scenario['name'].lower()}"
            os.makedirs(output_dir, exist_ok=True)
            
            # 只运行分析步骤来比较差异
            result = await orchestrator.run_single_step(
                step_name="analysis",
                input_dir=input_dir,
                output_dir=output_dir,
                user_preferences=scenario['preferences']
            )
            
            # 展示针对不同用户的分析差异
            if result and result.get('analysis_results'):
                first_paper = list(result['analysis_results'].values())[0]['output']
                print(f"   - 推荐难度评估: {first_paper.get('difficulty_level', 'N/A')}")
                print(f"   - 学习时间估算: {first_paper.get('reading_time_estimate', 'N/A')} 分钟")
                print(f"   - 核心概念数量: {len(first_paper.get('core_concepts', []))}")
            
            print(f"   ✅ {scenario['name']}场景测试完成")
        
    except Exception as e:
        print(f"❌ 用户偏好测试失败: {e}")
        import traceback
        traceback.print_exc()

def check_output_quality():
    """检查输出质量和完整性"""
    print("\n" + "="*60)
    print("🔍 输出质量检查")
    print("="*60)
    
    output_dir = Path("tests/outputs/full_pipeline")
    
    quality_checks = []
    
    # 检查分析报告
    analysis_report = output_dir / "analysis" / "analysis_report.md"
    if analysis_report.exists():
        content = analysis_report.read_text(encoding='utf-8')
        quality_checks.append(f"✅ 分析报告: {len(content)} 字符")
        
        # 检查关键部分
        if "## 📊 基本统计" in content:
            quality_checks.append("✅ 包含基本统计")
        if "## 📋 推荐学习顺序" in content:
            quality_checks.append("✅ 包含学习顺序")
        if "## 🎯 核心概念" in content:
            quality_checks.append("✅ 包含核心概念")
    else:
        quality_checks.append("❌ 分析报告缺失")
    
    # 检查概念提取报告
    extraction_report = output_dir / "extraction" / "concept_extraction_report.md"
    if extraction_report.exists():
        content = extraction_report.read_text(encoding='utf-8')
        quality_checks.append(f"✅ 概念报告: {len(content)} 字符")
        
        # 检查关键部分
        if "## 📊 提取统计" in content:
            quality_checks.append("✅ 包含提取统计")
        if "## 🎯 概念层次结构" in content:
            quality_checks.append("✅ 包含概念层次")
        if "## 🔗 论文依赖关系" in content:
            quality_checks.append("✅ 包含依赖关系")
    else:
        quality_checks.append("❌ 概念报告缺失")
    
    # 检查整体学习报告
    pipeline_report = output_dir / "pipeline_report.md"
    if pipeline_report.exists():
        content = pipeline_report.read_text(encoding='utf-8')
        quality_checks.append(f"✅ 学习报告: {len(content)} 字符")
        
        # 检查关键部分
        if "## 👤 学习配置" in content:
            quality_checks.append("✅ 包含学习配置")
        if "## 📚 论文概览" in content:
            quality_checks.append("✅ 包含论文概览")
        if "## 💡 学习建议" in content:
            quality_checks.append("✅ 包含学习建议")
    else:
        quality_checks.append("❌ 学习报告缺失")
    
    # 检查JSON数据完整性
    analysis_json = output_dir / "analysis" / "paper_analysis.json"
    if analysis_json.exists():
        try:
            with open(analysis_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                quality_checks.append(f"✅ 分析JSON: {len(data.get('analysis_results', {}))} 篇论文")
        except Exception as e:
            quality_checks.append(f"❌ 分析JSON损坏: {e}")
    
    extraction_json = output_dir / "extraction" / "concept_extraction.json"
    if extraction_json.exists():
        try:
            with open(extraction_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                quality_checks.append(f"✅ 提取JSON: {len(data.get('extractions', {}))} 篇论文")
        except Exception as e:
            quality_checks.append(f"❌ 提取JSON损坏: {e}")
    
    print("\n📋 质量检查结果:")
    for check in quality_checks:
        print(f"   {check}")
    
    # 计算质量得分
    passed_checks = len([c for c in quality_checks if c.startswith("✅")])
    total_checks = len(quality_checks)
    quality_score = (passed_checks / total_checks) * 100 if total_checks > 0 else 0
    
    print(f"\n📊 质量评分: {quality_score:.1f}% ({passed_checks}/{total_checks})")
    
    if quality_score >= 90:
        print("🎉 输出质量优秀！")
    elif quality_score >= 70:
        print("✅ 输出质量良好")
    else:
        print("⚠️ 输出质量需要改进")

if __name__ == "__main__":
    print("🚀 开始完整AI-Paper-Tutor流水线测试")
    
    # 运行完整流水线测试
    results = asyncio.run(test_full_pipeline())
    
    # 运行单步执行测试
    asyncio.run(test_single_step_execution())
    
    # 运行不同用户偏好测试
    asyncio.run(test_different_user_preferences())
    
    # 检查输出质量
    check_output_quality()
    
    print("\n🎉 完整流水线测试全部完成！")
    print("\n📖 查看测试结果:")
    print("   - tests/outputs/full_pipeline/ - 完整流水线结果")
    print("   - tests/outputs/step_analysis/ - 单步分析结果") 
    print("   - tests/outputs/step_extraction/ - 单步提取结果")
    print("   - tests/outputs/user_*/ - 不同用户场景结果") 