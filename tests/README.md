# AI-Paper-Tutor 测试指南

这个目录包含了 AI-Paper-Tutor 系统的测试文件和演示脚本。

## 📁 目录结构

```
tests/
├── test_marldown_folder/           # 测试案例论文
│   └── 1706.03762v7.Attention_Is_All_You_Need.md
├── outputs/                        # 测试输出结果 (运行后生成)
├── test_paper_analysisor.py        # 论文分析器测试
├── test_knowledge_extractor.py     # 概念提取器测试
├── test_full_pipeline.py           # 完整流水线测试
├── run_all_tests.py                # 运行所有测试的主脚本
├── quick_demo.py                   # 快速演示脚本
└── README.md                       # 本说明文件
```

## 🚀 快速开始

### 1. 快速演示 (推荐开始)

```bash
# 运行快速演示，体验核心功能
python tests/quick_demo.py
```

演示包含：
- 📖 论文解析与基本信息提取
- 📊 智能论文分析
- 🧠 概念提取与知识图谱  
- 🚀 完整学习流水线

### 2. 完整测试套件

```bash
# 运行所有测试
python tests/run_all_tests.py
```

包含功能：
- ✅ PaperAnalysisor 全功能测试
- ✅ KnowledgeExtractor 全功能测试
- ✅ 完整流水线功能测试
- ✅ 不同用户偏好测试
- ✅ 输出质量检查

## 📋 单独测试

### 论文分析器测试

```bash
python tests/test_paper_analysisor.py
```

测试内容：
- 批量论文分析功能
- 单篇论文详细分析
- 资源使用统计
- 输出格式验证

### 概念提取器测试

```bash
python tests/test_knowledge_extractor.py
```

测试内容：
- 概念提取功能
- 跨论文概念关系分析
- 知识图谱构建
- 学习路径推荐

### 完整流水线测试

```bash
python tests/test_full_pipeline.py
```

测试内容：
- 端到端流水线执行
- 单步执行验证
- 用户偏好差异化测试
- 输出质量评估

## 📊 测试案例

所有测试使用经典论文 **"Attention Is All You Need"** 作为案例：
- 📄 文件：`tests/test_marldown_folder/1706.03762v7.Attention_Is_All_You_Need.md`
- 🎯 内容：Transformer 架构的开创性论文
- 📏 规模：393行，45KB，包含完整的数学公式和图表

## 📁 输出结果

测试运行后，结果保存在 `tests/outputs/` 目录：

```
tests/outputs/
├── paper_analysis/                 # 论文分析结果
│   ├── analysis_report.md         # 分析报告
│   └── paper_analysis.json        # JSON数据
├── knowledge_extraction/           # 概念提取结果
│   ├── concept_extraction_report.md
│   └── concept_extraction.json
├── full_pipeline/                  # 完整流水线结果
│   ├── analysis/
│   ├── extraction/
│   └── pipeline_report.md         # 最终学习报告
├── quick_demo/                     # 快速演示结果
├── step_analysis/                  # 单步分析结果
├── step_extraction/                # 单步提取结果
└── user_*/                         # 不同用户场景结果
```

## 🎯 重要文件说明

### 核心报告文件

1. **`pipeline_report.md`** - 🎓 最终学习报告
   - 综合分析结果
   - 个性化学习建议
   - 完整学习路径

2. **`analysis_report.md`** - 📊 论文分析报告
   - 论文基本信息
   - 难度评估
   - 核心概念总结

3. **`concept_extraction_report.md`** - 🧠 概念提取报告
   - 概念层次结构
   - 知识图谱关系
   - 跨论文分析

### JSON数据文件

- **`paper_analysis.json`** - 论文分析的结构化数据
- **`concept_extraction.json`** - 概念提取的结构化数据
- 可以用 JSON 查看器或编程方式处理

## 💡 使用技巧

### 查看测试结果

1. **Markdown 报告**：用任何文本编辑器或 Markdown 查看器打开
2. **JSON 数据**：用 VS Code、JSONLint 等工具查看
3. **文件大小**：检查输出文件大小判断是否正常生成

### 自定义测试

1. **替换论文**：在 `test_marldown_folder/` 中放入你的论文
2. **修改用户偏好**：编辑测试脚本中的 `user_preferences`
3. **调整输出路径**：修改 `output_dir` 参数

### 性能调优

1. **减少 token 使用**：调整 prompt 长度
2. **并行处理**：多篇论文时使用异步处理
3. **缓存结果**：避免重复分析同一论文

## 🔧 故障排除

### 常见问题

1. **找不到论文文件**
   ```
   ❌ 没有找到论文文件
   ```
   解决：确保 `tests/test_marldown_folder/` 目录存在且包含 `.md` 文件

2. **LLM API 错误**
   ```
   ❌ API调用失败
   ```
   解决：检查网络连接和 API 配置

3. **输出目录权限错误**
   ```
   ❌ 无法创建输出目录
   ```
   解决：确保有写入权限或使用其他目录

### 调试模式

修改日志级别查看详细信息：
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 预期资源使用

基于 "Attention Is All You Need" 论文的预期使用量：

- **单次论文分析**：~8,000-12,000 tokens，$0.01-0.02
- **概念提取**：~10,000-15,000 tokens，$0.015-0.025
- **完整流水线**：~20,000-30,000 tokens，$0.03-0.05

> 💡 实际用量可能因 LLM 响应长度而有所不同

## 🎉 成功标准

测试成功的标志：
- ✅ 所有脚本运行无错误
- ✅ 生成了完整的输出文件
- ✅ Markdown 报告内容丰富且格式正确
- ✅ JSON 数据结构完整且可解析
- ✅ 资源使用在预期范围内

---

🚀 **开始测试**: `python tests/quick_demo.py`

📖 **查看完整文档**: 项目根目录的 `README.md` 