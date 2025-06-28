## 🧠 LearnPilot: Your AI-Powered Research Learning Companion

> 纸上得来终觉浅，绝知此事要躬行。

**LearnPilot** is an open-source intelligent assistant designed to help you learn research papers deeply, efficiently, and interactively. Whether you're a student, researcher, or self-learner, LearnPilot guides you from "finding what to learn" to "mastering it through tasks, feedback, and exploration."

### 🎯 Project Vision
LearnPilot is not designed as a general-purpose tutor for traditional textbook-heavy subjects. Instead, it was born from a very focused need:
To help learners—especially researchers, engineers, and self-learners—deeply engage with small, curated sets of papers around a specific topic or academic subfield.

In real-world learning, we often don't face an entire curriculum—we face 3 to 10 key papers that define a method, a trend, or a research direction. LearnPilot is built exactly for this context:
To help you navigate, understand, and apply the core ideas of a paper cluster—whether you're entering a new research domain, evaluating recent breakthroughs, or preparing for a technical deep dive.

This makes LearnPilot ideal for:
- Quickly onboarding into a new research area (e.g. "Diffusion Models" or "RLHF"),
- Understanding paper collections from a reading group or course syllabus,
- Building task-driven, output-oriented learning paths without getting overwhelmed.

### 🚀 What Can LearnPilot Do?

* 🔍 **Search smartly**: Automatically retrieve high-quality papers across the web (arXiv, Semantic Scholar, etc.) based on your topic or question.
* 🗺️ **Plan your study**: Generate structured reading plans and prerequisite learning paths for each paper.
* 🧪 **Practice through tasks**: Convert concepts into coding exercises, reproduction challenges, and Q\&A sheets.
* 🧠 **Review your learning**: Analyze your code, summaries, and answers with AI feedback and suggestions.
* 🌱 **Grow deeper**: Recommend follow-up materials, related work, and provide in-depth concept explanations.

### 📦 Who is this for?

* Researchers needing a smarter way to digest papers.
* Developers learning new AI/ML techniques.
* Students building structured, project-based learning paths.
* Anyone lost in a sea of resources and looking for **clarity, direction, and interaction**.

### 🛠️ Built with

* Python / Agents-SDK / LLM API 
* ArXiv / Semantic Scholar / LLM-based Search
* Streamlit / Markdown Task Sheets
* Optional: Code evaluation via PyLint, GPT Review Agent

---

## 📂 Project Structure

```
src/learn_pilot/
├── agents/                           # AI Agent 模块
│   ├── paper_analysisor.py          # 论文分析 Agent
│   ├── knowledge_extractor.py       # 概念提取 Agent
│   ├── learning_planer.py           # 学习计划 Agent
│   ├── task_sheet_generator.py      # 任务生成 Agent
│   ├── guidance_teacher.py          # 学习指导 Agent
│   ├── filter/                      # 过滤器 Agents
│   └── monitoring/                  # 监控 Agents
├── core/                            # 核心配置与基础功能
│   ├── config/                      # 配置管理
│   ├── logging/                     # 日志系统
│   └── agents/                      # Agent 基础框架
├── services/                        # 业务服务层
│   ├── arxiv_monitor/              # arXiv 监控服务
│   └── vector_search/              # 向量搜索服务
├── literature_utils/               # 文献处理工具
│   ├── knowledge_parser/           # 知识解析
│   └── knowledge_search/           # 知识搜索
├── tools/                          # 通用工具
│   ├── file_system/               # 文件系统工具
│   ├── database/                  # 数据库工具
│   ├── translation/               # 翻译工具
│   └── pricing/                   # 成本计算工具
├── models/                         # 数据模型定义
└── main.py                        # 主入口文件
```

### 📋 Core AI-Paper-Tutor Pipeline

LearnPilot 的核心功能基于以下 Agent 工作流：

```
User Input (Papers) → PaperAnalysisor
                          ↓
                   KnowledgeExtractor
                          ↓
                    LearningPlaner
                          ↓
                  TaskSheetGenerator
                          ↓
                   GuidanceTeacher
```

**主要输出文件格式：**
- `/user_data/outputs/schedule.json`：个性化学习计划
- `/user_data/outputs/task_sheet.md`：任务总表（问答 + 编程实验）
- `/user_data/outputs/lab_code_skeleton.py`：代码填空模板
- `/user_data/outputs/knowledge_graph.json`：知识图谱数据

---
## ✅ TODO List – LearnPilot Development Roadmap

### 🚧 Phase 1: Minimum Viable Prototype (MVP)

#### 📚 Paper Collection & Management

* [ ] Implement keyword-based paper search via arXiv API or Semantic Scholar API
* [ ] Support manual PDF uploads + metadata extraction (title, abstract, authors, sections)
* [ ] Enable tagging/grouping papers into "topics" or "collections"

#### 🗺️ Study Plan Generator

* [ ] Parse paper structure to generate a section-wise reading plan
* [ ] Identify prerequisites and auto-generate recommended reading list
* [ ] Support simple prompt-based plan customization (e.g., "I have 5 days", "I'm new to RL")

#### 🧪 Task Sheet Builder

* [ ] Auto-generate tasks from papers:

  * [ ] Reading comprehension tasks
  * [ ] Algorithm implementation tasks
  * [ ] Summary writing or concept explanation tasks
* [ ] Export as Markdown or JSON with checkboxes

#### 🧠 Review & Feedback System

* [ ] Allow users to upload:

  * [ ] Code (Jupyter / .py)
  * [ ] Summaries / Reports
* [ ] Integrate LLM-based review:

  * [ ] Code correctness & style feedback
  * [ ] Textual feedback on clarity and depth

---

### 🧠 Phase 2: Smart Interaction & Learning Loop

* [ ] LLM-powered Q\&A assistant for each paper (retrieval-based)
* [ ] "Explain this section" / "Give a simplified summary" interactive mode
* [ ] Multi-paper concept graph: link common terms, methods, citations across papers
* [ ] Flashcard or quiz generation from a paper or topic

---

### 🌱 Phase 3: Personalization & Knowledge Growth

* [ ] User progress tracking: which tasks completed, which concepts mastered
* [ ] Adaptive study planner (adjust based on user performance or speed)
* [ ] Paper-based roadmap generator: recommend next 3–5 papers to explore
* [ ] Support for team learning mode / reading groups

---

### 🧪 Bonus: Developer & Open Research Tools

* [ ] CLI mode: command-line paper planner for power users
* [ ] Plugin system: allow external LLMs, PDF parsers, or evaluation modules
* [ ] Dataset collection: anonymized learning traces for future research on "AI-aided learning"

## 🚀 Quick Start

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 LearnPilot
python -m src.learn_pilot.main

# 运行特定功能模块
python -m src.learn_pilot.agents.paper_analysisor --input_dir=./user_data/papers
```


