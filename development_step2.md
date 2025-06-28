# AI-Paper-Tutor 系统开发文档

## 📌 项目简介

**AI-Paper-Tutor** 是一个基于 `agents-sdk` 框架构建的智能 Agent 系统，输入一组论文（以 Markdown 格式），输出包含：

* 阅读顺序推荐
* 前置知识抽取与知识图谱构建
* 个性化学习计划
* 问答任务 + 编程实验任务 Task Sheet
* 带提示的代码骨架（可供填空练习）

适用于科研入门、技术深度学习等任务型读论文场景。

---

## 🧱 技术栈

| 功能模块    | 技术选择                      |
| ------- | ------------------------- |
| Agent框架 | `agents-sdk`              |
| 知识图谱    | `networkx` / `Neo4j`（可选）  |
| 文本向量存储  | `FAISS` 或 `ChromaDB`      |
| 分段语义抽取  | `GPT-4o` + Tool 模式        |
| 编程实验生成  | 自定义 `TaskGenerator` Agent |
| 前端（可选）  | `Next.js + Tailwind`      |

---

## 📥 输入格式说明

系统输入为 Markdown 格式的论文内容，要求如下：

```markdown
# Paper Title: LoRA: Low-Rank Adaptation of Large Language Models

## Abstract
Lorem ipsum...

## Introduction
...

## Method
...

## Experiments
...

## References
...
```

支持多篇论文作为列表输入。每篇论文可以用 YAML 元信息标注：

```yaml
---
title: "LoRA: Low-Rank Adaptation"
authors: ["Edward Hu", "Yelong Shen"]
year: 2021
---
```

---

## 📦 系统模块结构

### 🏗️ 融入现有 src/learn_pilot 结构的调整方案

基于现有的 `src/learn_pilot` 项目结构，建议按以下方式组织 AI-Paper-Tutor 功能：

```
src/learn_pilot/
├── agents/                              # AI Agent 模块
│   ├── paper_analysisor.py            # 论文分析 Agent (对应 ParserAgent)
│   ├── knowledge_extractor.py         # 概念提取 Agent (对应 ConceptMiner)
│   ├── learning_planer.py             # 学习计划 Agent (对应 CurriculumPlanner)
│   ├── task_sheet_generator.py        # 任务生成 Agent (对应 TaskSheetGenerator)
│   ├── guidance_teacher.py            # 学习指导 Agent (新增)
│   ├── code_skeleton_generator.py     # 代码骨架生成 Agent (新增)
│   ├── knowledge_graph_agent.py       # 知识图谱构建 Agent (新增)
│   ├── filter/                        # 过滤器 Agents
│   └── monitoring/                    # 监控 Agents
├── core/                              # 核心配置与基础功能
│   ├── config/                        # 配置管理
│   ├── logging/                       # 日志系统
│   └── agents/                        # Agent 基础框架
├── services/                          # 业务服务层
│   ├── arxiv_monitor/                # arXiv 监控服务
│   ├── vector_search/                # 向量搜索服务
│   └── pipeline_orchestrator.py      # 流水线编排服务 (新增)
├── literature_utils/                 # 文献处理工具
│   ├── knowledge_parser/             # 知识解析
│   ├── knowledge_search/             # 知识搜索
│   ├── markdown_parser.py            # Markdown 解析工具 (新增)
│   └── faiss_store.py               # 向量存储操作 (新增)
├── tools/                            # 通用工具
│   ├── file_system/                 # 文件系统工具
│   ├── database/                    # 数据库工具
│   ├── translation/                 # 翻译工具
│   ├── pricing/                     # 成本计算工具
│   └── graph_utils.py              # 图操作工具 (新增)
├── models/                          # 数据模型定义
│   ├── paper_models.py             # 论文数据模型 (新增)
│   ├── task_models.py              # 任务数据模型 (新增)
│   └── graph_models.py             # 图数据模型 (新增)
├── prompts/                         # Prompt 模板目录 (新增)
│   ├── concept_extraction.txt       # 概念提取 prompt
│   ├── task_generation.txt          # 任务生成 prompt
│   └── code_skeleton.txt           # 代码骨架 prompt
└── main.py                         # 主入口文件
```

### 📋 新增目录说明

**prompts/** 目录：
- 存放各种 LLM prompt 模板
- 便于模块化管理和版本控制
- 支持多语言 prompt 模板

**数据输入输出路径：**
- 输入：`user_data/papers/` (markdown 文件)
- 输出：`user_data/outputs/` (生成的计划、任务表等)
- 临时文件：`user_data/temp/` (中间处理文件)

---

## 🔁 Agent 流程结构

使用 `agents-sdk` 搭建如下工作流：

```
User Input (.md) → PaperAnalysisor (paper_analysisor.py)
                    ↓
               KnowledgeExtractor (knowledge_extractor.py)
                    ↓
             KnowledgeGraphAgent (knowledge_graph_agent.py)
                    ↓
             LearningPlaner (learning_planer.py)
                    ↓
            TaskSheetGenerator (task_sheet_generator.py)
                    ↓
         CodeSkeletonGenerator (code_skeleton_generator.py)
                    ↓
            GuidanceTeacher (guidance_teacher.py)
```

---

## 🧠 核心 Agent 功能

### 1. `PaperAnalysisor` (paper_analysisor.py)

* 输入：Markdown 文本（支持多个）
* 输出：段落切分 + 元信息抽取（Title、作者、章节等）

```python
Agent.run("parse_md", {"md_text": "..."})
# 返回结构： {"sections": [...], "metadata": {...} }
```

### 2. `KnowledgeExtractor` (knowledge_extractor.py)

* 对每个段落提问 LLM：有哪些新概念、方法、是否涉及已有知识点
* 输出结构：

```json
{
  "core_concepts": ["Low-rank decomposition", "Adapter layer"],
  "prerequisites": [
    {"name": "Matrix multiplication", "level": "foundational"},
    {"name": "Fine-tuning", "level": "intermediate"}
  ]
}
```

### 3. `KnowledgeGraphAgent` (knowledge_graph_agent.py)

* 输入所有论文的 `prerequisites`
* 输出拓扑有向图 `paper_i → paper_j`
* 使用 `networkx` 存储依赖图，并暴露 `topo_sort()` 方法给 PlannerAgent 使用

### 4. `LearningPlaner` (learning_planer.py)

* 输入：依赖图、用户时间预算（如每周 10h）
* 输出：有节奏的学习计划

```json
{
  "schedule": [
    {"day": 1, "paper": "LoRA", "pages": 5},
    {"day": 2, "review": true},
    ...
  ]
}
```

### 5. `TaskSheetGenerator` (task_sheet_generator.py)

* 输入：每篇论文结构、概念、方法
* 输出：Markdown 格式的 Task Sheet，包括：

  * 概念问答题
  * 编程实验任务（含实验目标、步骤、结果格式）

### 6. `CodeSkeletonGenerator` (code_skeleton_generator.py)

* 输入：某个实验目标与方法名称
* 输出：带 `TODO` 的 Python 代码骨架

```python
# 示例输出

def prune_heads(model, mask):
    """
    TODO:
    1. 遍历每一层 encoder
    2. 调用 prune_heads
    """
    pass
```

### 7. `GuidanceTeacher` (guidance_teacher.py)

* 输入：用户提交的作业、代码、总结
* 输出：AI 评估反馈和改进建议

---

## 📤 输出文件格式

1. `user_data/outputs/schedule.json`：每日学习计划
2. `user_data/outputs/task_sheet.md`：任务总表（问答题 + 实验）
3. `user_data/outputs/lab_code_skeleton.py`：代码填空模板
4. `user_data/outputs/knowledge_graph.graphml`：知识图谱可视化（可选）

---

## 🚀 运行方式（本地测试）

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 main pipeline
python -m src.learn_pilot.main --input_dir=./user_data/papers --output_dir=./user_data/outputs

# 运行特定 Agent
python -m src.learn_pilot.agents.paper_analysisor --input_file=./user_data/papers/lora.md
```

或可封装成命令行工具 / Web API。

---

## 📚 后续计划

* 加入"阅读后反馈"模块，持续调整任务难度
* 支持嵌入 YouTube / arXiv 链接自动转换为 markdown
* 加入评估机制：用户打分 + GPT 自评
* 开源项目模板（可推到 HuggingFace Space）
