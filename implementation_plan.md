# LearnPilot AI-Paper-Tutor 实施计划

## 📋 文件结构调整清单

### ✅ 现有文件保留
以下文件保持现有结构，可能需要扩展功能：

```
src/learn_pilot/
├── agents/
│   ├── knowledge_extractor.py     ✅ 已存在，需扩展功能
│   ├── guidance_teacher.py        ✅ 已存在，需扩展功能
│   ├── learning_planer.py         ✅ 已存在，需扩展功能
│   └── task_sheet_generator.py    ✅ 已存在，需扩展功能
├── core/                          ✅ 保持现有结构
├── services/                      ✅ 保持现有结构
├── literature_utils/              ✅ 保持现有结构
├── tools/                         ✅ 保持现有结构
├── models/                        ✅ 保持现有结构
└── main.py                        ✅ 已存在，需扩展功能
```

### 🆕 需要新增的文件

#### 1. Agent 模块新增文件
```bash
# 在 src/learn_pilot/agents/ 目录下创建
touch src/learn_pilot/agents/code_skeleton_generator.py
touch src/learn_pilot/agents/knowledge_graph_agent.py
```

#### 2. 工具模块新增文件
```bash
# 在 src/learn_pilot/tools/ 目录下创建
touch src/learn_pilot/tools/graph_utils.py

# 在 src/learn_pilot/literature_utils/ 目录下创建
touch src/learn_pilot/literature_utils/markdown_parser.py
touch src/learn_pilot/literature_utils/faiss_store.py
```

#### 3. 数据模型新增文件
```bash
# 在 src/learn_pilot/models/ 目录下创建
touch src/learn_pilot/models/paper_models.py
touch src/learn_pilot/models/task_models.py
touch src/learn_pilot/models/graph_models.py
```

#### 4. 服务层新增文件
```bash
# 在 src/learn_pilot/services/ 目录下创建
touch src/learn_pilot/services/pipeline_orchestrator.py
```

#### 5. Prompt 模板目录
```bash
# 创建新的 prompts 目录和文件
mkdir -p src/learn_pilot/prompts
touch src/learn_pilot/prompts/concept_extraction.txt
touch src/learn_pilot/prompts/task_generation.txt
touch src/learn_pilot/prompts/code_skeleton.txt
touch src/learn_pilot/prompts/paper_analysis.txt
touch src/learn_pilot/prompts/learning_plan.txt
```

---

## 🔧 具体实施步骤

### Phase 1: 基础框架搭建 (1-2天)

1. **创建数据模型**
   ```python
   # src/learn_pilot/models/paper_models.py
   class Paper:
       title: str
       authors: List[str]
       abstract: str
       sections: List[Section]
       metadata: dict
   
   class Section:
       title: str
       content: str
       concepts: List[str]
       level: str  # intro, method, experiment, etc.
   ```

2. **创建 Prompt 模板**
   ```
   # src/learn_pilot/prompts/concept_extraction.txt
   分析以下论文段落，提取核心概念和前置知识要求...
   ```

3. **更新 main.py 入口**
   - 添加命令行参数解析
   - 集成 pipeline orchestrator
   - 添加日志配置

### Phase 2: 核心 Agent 实现 (3-5天)

#### 实现优先级：
1. **PaperAnalysisor** (修改现有 paper_analysisor.py)
2. **KnowledgeExtractor** (扩展现有 knowledge_extractor.py)
3. **KnowledgeGraphAgent** (新建 knowledge_graph_agent.py)
4. **LearningPlaner** (扩展现有 learning_planer.py)
5. **TaskSheetGenerator** (扩展现有 task_sheet_generator.py)
6. **CodeSkeletonGenerator** (新建 code_skeleton_generator.py)

### Phase 3: 流水线集成 (2-3天)

1. **PipelineOrchestrator 实现**
   ```python
   # src/learn_pilot/services/pipeline_orchestrator.py
   class PipelineOrchestrator:
       def run_full_pipeline(self, input_papers: List[str]) -> dict:
           # 按顺序调用各个 Agent
           pass
   ```

2. **输入输出管理**
   - 设置 `user_data/papers/` 输入目录
   - 设置 `user_data/outputs/` 输出目录
   - 实现文件监控和批处理

### Phase 4: 测试和优化 (2-3天)

1. **单元测试编写**
   ```bash
   mkdir tests/
   touch tests/test_paper_analysisor.py
   touch tests/test_knowledge_extractor.py
   # ... 其他测试文件
   ```

2. **集成测试**
   - 准备测试论文集（如 LoRA, Attention is All You Need）
   - 端到端流水线测试
   - 性能优化

---

## 📂 目录结构最终状态

```
src/learn_pilot/
├── agents/                              # AI Agent 模块
│   ├── paper_analysisor.py            # ✅ 扩展现有
│   ├── knowledge_extractor.py         # ✅ 扩展现有
│   ├── learning_planer.py             # ✅ 扩展现有
│   ├── task_sheet_generator.py        # ✅ 扩展现有
│   ├── guidance_teacher.py            # ✅ 扩展现有
│   ├── code_skeleton_generator.py     # 🆕 新建
│   ├── knowledge_graph_agent.py       # 🆕 新建
│   ├── filter/                        # ✅ 保持现有
│   ├── monitoring/                    # ✅ 保持现有
│   └── tools/                         # ✅ 保持现有
├── core/                              # ✅ 保持现有结构
├── services/                          # 业务服务层
│   ├── arxiv_monitor/                # ✅ 保持现有
│   ├── vector_search/                # ✅ 保持现有
│   └── pipeline_orchestrator.py      # 🆕 新建
├── literature_utils/                 # 文献处理工具
│   ├── knowledge_parser/             # ✅ 保持现有
│   ├── knowledge_search/             # ✅ 保持现有
│   ├── markdown_parser.py            # 🆕 新建
│   └── faiss_store.py               # 🆕 新建
├── tools/                            # 通用工具
│   ├── file_system/                 # ✅ 保持现有
│   ├── database/                    # ✅ 保持现有
│   ├── translation/                 # ✅ 保持现有
│   ├── pricing/                     # ✅ 保持现有
│   └── graph_utils.py              # 🆕 新建
├── models/                          # 数据模型定义
│   ├── paper_models.py             # 🆕 新建
│   ├── task_models.py              # 🆕 新建
│   └── graph_models.py             # 🆕 新建
├── prompts/                         # 🆕 新建目录
│   ├── concept_extraction.txt       # 🆕 新建
│   ├── task_generation.txt          # 🆕 新建
│   ├── code_skeleton.txt           # 🆕 新建
│   ├── paper_analysis.txt          # 🆕 新建
│   └── learning_plan.txt           # 🆕 新建
└── main.py                         # ✅ 扩展现有
```

---

## 🚀 快速开始命令

```bash
# 1. 创建所有需要的新文件
./scripts/create_new_files.sh

# 2. 安装新增依赖
pip install networkx faiss-cpu

# 3. 准备测试数据
mkdir -p user_data/papers user_data/outputs user_data/temp

# 4. 运行测试
python -m src.learn_pilot.main --input_dir=./user_data/papers --output_dir=./user_data/outputs

# 5. 单独测试某个 Agent
python -m src.learn_pilot.agents.paper_analysisor --help
```

---

## 📝 注意事项

1. **保持向后兼容**: 所有现有功能继续工作
2. **模块化设计**: 每个 Agent 可以独立测试和运行
3. **配置管理**: 使用现有的 core/config 管理新增配置
4. **日志系统**: 使用现有的 core/logging 系统
5. **错误处理**: 统一的异常处理和错误返回格式

## 📊 进度跟踪

- [ ] Phase 1: 基础框架搭建 (估计 1-2天)
- [ ] Phase 2: 核心 Agent 实现 (估计 3-5天)
- [ ] Phase 3: 流水线集成 (估计 2-3天)
- [ ] Phase 4: 测试和优化 (估计 2-3天)

**总估计工时**: 8-13天

## 🔗 相关文档

- [开发文档](./development_step2.md) - 详细的技术规格
- [README.md](./README.md) - 项目概览和使用说明 