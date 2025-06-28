"""
运行所有AI-Paper-Tutor测试的主脚本
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

def print_banner():
    """打印测试横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                    AI-Paper-Tutor 测试套件                    ║
║                                                              ║
║  🔍 PaperAnalysisor - 论文分析器测试                          ║
║  🧠 KnowledgeExtractor - 概念提取器测试                       ║
║  🚀 完整流水线功能测试                                         ║
║                                                              ║
║  测试案例: Attention Is All You Need                          ║
╚══════════════════════════════════════════════════════════════╝
"""
    print(banner)

def setup_test_environment():
    """设置测试环境"""
    print("🔧 设置测试环境...")
    
    # 创建必要的输出目录
    output_dirs = [
        "tests/outputs",
        "tests/outputs/paper_analysis",
        "tests/outputs/knowledge_extraction", 
        "tests/outputs/full_pipeline",
        "tests/outputs/step_analysis",
        "tests/outputs/step_extraction",
        "logs"
    ]
    
    for dir_path in output_dirs:
        os.makedirs(dir_path, exist_ok=True)
    
    # 检查输入文件
    input_dir = Path("tests/test_marldown_folder")
    if not input_dir.exists():
        print("❌ 测试输入目录不存在: tests/test_marldown_folder")
        return False
    
    md_files = list(input_dir.glob("*.md"))
    if not md_files:
        print("❌ 没有找到测试用的Markdown文件")
        return False
    
    print(f"✅ 测试环境设置完成，找到 {len(md_files)} 个测试文件")
    for md_file in md_files:
        print(f"   📄 {md_file.name}")
    
    return True

async def run_paper_analysisor_tests():
    """运行论文分析器测试"""
    print("\n" + "="*60)
    print("🔍 运行 PaperAnalysisor 测试")
    print("="*60)
    
    try:
        # 导入并运行测试
        from test_paper_analysisor import test_paper_analysisor, test_single_paper_analysis
        
        start_time = time.time()
        
        # 运行基本测试
        print("📝 运行基本功能测试...")
        results = await test_paper_analysisor()
        
        # 运行详细测试
        print("\n🔬 运行详细分析测试...")
        await test_single_paper_analysis()
        
        end_time = time.time()
        
        print(f"\n✅ PaperAnalysisor 测试完成 (耗时: {end_time - start_time:.1f}秒)")
        return True
        
    except Exception as e:
        print(f"❌ PaperAnalysisor 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_knowledge_extractor_tests():
    """运行概念提取器测试"""
    print("\n" + "="*60)
    print("🧠 运行 KnowledgeExtractor 测试")
    print("="*60)
    
    try:
        # 导入并运行测试
        from test_knowledge_extractor import test_knowledge_extractor, test_single_paper_extraction, test_cross_paper_analysis
        
        start_time = time.time()
        
        # 运行基本测试
        print("📝 运行基本功能测试...")
        results = await test_knowledge_extractor()
        
        # 运行详细测试
        print("\n🔬 运行详细提取测试...")
        await test_single_paper_extraction()
        
        # 运行跨论文分析测试
        print("\n🌐 运行跨论文分析测试...")
        await test_cross_paper_analysis()
        
        end_time = time.time()
        
        print(f"\n✅ KnowledgeExtractor 测试完成 (耗时: {end_time - start_time:.1f}秒)")
        return True
        
    except Exception as e:
        print(f"❌ KnowledgeExtractor 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_full_pipeline_tests():
    """运行完整流水线测试"""
    print("\n" + "="*60)
    print("🚀 运行完整流水线测试")
    print("="*60)
    
    try:
        # 导入并运行测试
        from test_full_pipeline import (
            test_full_pipeline, 
            test_single_step_execution, 
            test_different_user_preferences,
            check_output_quality
        )
        
        start_time = time.time()
        
        # 运行完整流水线测试
        print("🎓 运行完整流水线测试...")
        results = await test_full_pipeline()
        
        # 运行单步执行测试
        print("\n🔄 运行单步执行测试...")
        await test_single_step_execution()
        
        # 运行不同用户偏好测试
        print("\n👥 运行用户偏好测试...")
        await test_different_user_preferences()
        
        # 检查输出质量
        print("\n🔍 检查输出质量...")
        check_output_quality()
        
        end_time = time.time()
        
        print(f"\n✅ 完整流水线测试完成 (耗时: {end_time - start_time:.1f}秒)")
        return True
        
    except Exception as e:
        print(f"❌ 完整流水线测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def generate_test_summary():
    """生成测试总结报告"""
    print("\n" + "="*60)
    print("📊 测试结果总结")
    print("="*60)
    
    # 统计输出文件
    output_base = Path("tests/outputs")
    
    summary = {
        "论文分析结果": [],
        "概念提取结果": [],
        "流水线结果": [],
        "JSON数据文件": [],
        "Markdown报告": []
    }
    
    # 扫描输出文件
    if output_base.exists():
        for item in output_base.rglob("*"):
            if item.is_file():
                relative_path = str(item.relative_to(output_base))
                
                if "analysis" in relative_path:
                    summary["论文分析结果"].append(relative_path)
                elif "extraction" in relative_path:
                    summary["概念提取结果"].append(relative_path)
                elif "pipeline" in relative_path:
                    summary["流水线结果"].append(relative_path)
                
                if item.suffix == ".json":
                    summary["JSON数据文件"].append(relative_path)
                elif item.suffix == ".md":
                    summary["Markdown报告"].append(relative_path)
    
    # 打印总结
    print(f"📁 输出文件统计:")
    for category, files in summary.items():
        if files:
            print(f"\n   📂 {category} ({len(files)} 个文件):")
            for file in files[:5]:  # 最多显示5个
                print(f"      📄 {file}")
            if len(files) > 5:
                print(f"      ... 还有 {len(files) - 5} 个文件")
    
    # 计算总文件大小
    total_size = 0
    total_files = 0
    if output_base.exists():
        for item in output_base.rglob("*"):
            if item.is_file():
                total_size += item.stat().st_size
                total_files += 1
    
    print(f"\n📊 总体统计:")
    print(f"   - 总文件数: {total_files}")
    print(f"   - 总大小: {total_size / 1024:.1f} KB")
    print(f"   - 输出目录: tests/outputs/")

def print_usage_instructions():
    """打印使用说明"""
    print("\n" + "="*60)
    print("📖 使用说明")
    print("="*60)
    
    instructions = """
🎯 如何查看测试结果:

1. 📊 论文分析结果:
   tests/outputs/paper_analysis/analysis_report.md
   tests/outputs/full_pipeline/analysis/analysis_report.md

2. 🧠 概念提取结果:
   tests/outputs/knowledge_extraction/concept_extraction_report.md
   tests/outputs/full_pipeline/extraction/concept_extraction_report.md

3. 🎓 完整学习报告:
   tests/outputs/full_pipeline/pipeline_report.md

4. 📋 JSON数据文件:
   tests/outputs/**/**.json (可以用JSON查看器打开)

🚀 如何运行单个测试:
   python tests/test_paper_analysisor.py
   python tests/test_knowledge_extractor.py
   python tests/test_full_pipeline.py

🔧 如何使用main.py:
   python -m src.learn_pilot.main --input_dir=tests/test_marldown_folder --output_dir=my_output

💡 提示:
   - 测试使用的是经典论文 "Attention Is All You Need"
   - 所有输出都是中文，便于理解
   - LLM分析结果可能每次略有不同，这是正常的
"""
    print(instructions)

async def main():
    """主测试函数"""
    start_time = time.time()
    
    # 打印横幅
    print_banner()
    
    # 设置测试环境
    if not setup_test_environment():
        print("❌ 测试环境设置失败，退出")
        return
    
    # 运行所有测试
    test_results = []
    
    # 1. 论文分析器测试
    result1 = await run_paper_analysisor_tests()
    test_results.append(("PaperAnalysisor", result1))
    
    # 2. 概念提取器测试  
    result2 = await run_knowledge_extractor_tests()
    test_results.append(("KnowledgeExtractor", result2))
    
    # 3. 完整流水线测试
    result3 = await run_full_pipeline_tests()
    test_results.append(("完整流水线", result3))
    
    # 总结测试结果
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n" + "="*60)
    print("🎉 测试执行完成!")
    print("="*60)
    
    print(f"⏱️  总耗时: {total_time:.1f} 秒")
    print(f"📊 测试结果:")
    
    passed_tests = 0
    for test_name, result in test_results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   - {test_name}: {status}")
        if result:
            passed_tests += 1
    
    success_rate = (passed_tests / len(test_results)) * 100
    print(f"\n🎯 成功率: {success_rate:.1f}% ({passed_tests}/{len(test_results)})")
    
    if success_rate == 100:
        print("🎉 所有测试都通过了！系统运行正常。")
    elif success_rate >= 66:
        print("⚠️  大部分测试通过，有少量问题需要关注。")
    else:
        print("❌ 多个测试失败，需要检查系统配置。")
    
    # 生成测试总结
    generate_test_summary()
    
    # 打印使用说明
    print_usage_instructions()

if __name__ == "__main__":
    # 设置日志级别
    import logging
    logging.basicConfig(level=logging.WARNING)  # 减少日志输出，专注于测试结果
    
    # 运行测试
    asyncio.run(main()) 