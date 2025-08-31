"""
Optimized AI Agents
重构和优化的AI Agents，集成性能优化和质量控制
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .optimization import (
    AIOptimizer, PromptOptimizer, QualityValidator, BatchProcessor,
    TaskComplexity, ModelTier, optimize_ai_call, get_ai_optimizer
)

logger = logging.getLogger(__name__)

class OptimizedPaperAnalysisor:
    """优化的论文分析器"""
    
    def __init__(self):
        self.optimizer = get_ai_optimizer()
        self.prompt_optimizer = PromptOptimizer()
        self.validator = QualityValidator()
        self._setup_templates()
        self._setup_validators()
    
    def _setup_templates(self):
        """设置优化的prompt模板"""
        
        analysis_template = """
请深入分析以下学术论文，提取关键信息：

论文内容：
{content}

分析要求：
1. 准确识别研究问题和假设
2. 详细描述研究方法和技术路线
3. 总结核心贡献和创新点
4. 评估技术复杂度和学习难度
5. 提取关键概念和术语

请以JSON格式返回结果，包含以下字段：
- title: 论文标题
- authors: 作者列表
- venue: 发表会议/期刊
- year: 发表年份
- research_problem: 研究问题描述
- main_method: 主要方法和技术
- key_contributions: 关键贡献列表
- core_concepts: 核心概念列表
- difficulty_level: 难度级别(beginner/intermediate/advanced)
- technical_complexity: 技术复杂度(low/medium/high)
- reading_time_estimate: 阅读时间估算(分钟)
- prerequisites: 前置知识要求
- section_summary: 各章节摘要
"""
        
        self.prompt_optimizer.register_template("paper_analysis", analysis_template)
        
        # 添加few-shot examples
        examples = [
            {
                "input": "论文: Attention Is All You Need\n摘要: We propose the Transformer...",
                "output": json.dumps({
                    "title": "Attention Is All You Need",
                    "research_problem": "序列转录任务中的RNN和CNN局限性",
                    "main_method": "基于注意力机制的Transformer架构",
                    "key_contributions": ["提出Transformer架构", "消除循环和卷积", "实现并行化训练"],
                    "difficulty_level": "advanced",
                    "technical_complexity": "high"
                }, ensure_ascii=False)
            }
        ]
        
        self.prompt_optimizer.register_template("paper_analysis", analysis_template, examples)
    
    def _setup_validators(self):
        """设置验证器"""
        async def paper_analysis_validator(output: str, context: Dict[str, Any]):
            try:
                data = json.loads(output)
                required_fields = ["title", "research_problem", "main_method", "key_contributions"]
                
                issues = []
                confidence = 1.0
                
                for field in required_fields:
                    if field not in data or not data[field]:
                        issues.append(f"缺少字段: {field}")
                        confidence -= 0.2
                
                # 内容质量检查
                if len(data.get("research_problem", "")) < 30:
                    issues.append("研究问题描述过于简短")
                    confidence -= 0.1
                
                if len(data.get("key_contributions", [])) == 0:
                    issues.append("未识别到关键贡献")
                    confidence -= 0.2
                
                return confidence > 0.6, max(0.0, confidence), issues
                
            except json.JSONDecodeError:
                return False, 0.0, ["输出格式错误"]
        
        self.validator.register_validator("paper_analysis", paper_analysis_validator)
    
    @optimize_ai_call("paper_analysis", TaskComplexity.MODERATE)
    async def analyze_paper(self, content: str, quality_priority: bool = False) -> Dict[str, Any]:
        """分析单篇论文"""
        
        # 评估任务复杂度
        complexity = TaskComplexity.MODERATE
        if len(content) > 15000:
            complexity = TaskComplexity.COMPLEX
        elif len(content) < 5000:
            complexity = TaskComplexity.SIMPLE
        
        # 智能模型选择
        model_tier = await self.optimizer.smart_model_selection(
            complexity, len(content), quality_priority
        )
        
        # 构建优化的prompt
        messages = self.prompt_optimizer.build_optimized_prompt(
            "paper_analysis",
            {"content": content[:10000]},  # 限制长度避免token超限
            use_cot=True,
            use_examples=complexity != TaskComplexity.SIMPLE
        )
        
        # 调用LLM
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = await self.optimizer.cached_completion(
                    messages=messages,
                    model_tier=model_tier,
                    use_cache=True
                )
                
                # 验证输出质量
                is_valid, confidence, issues = await self.validator.validate_output(
                    "paper_analysis", result["content"], {"content": content}
                )
                
                if is_valid or attempt == max_retries - 1:
                    return {
                        "analysis": json.loads(result["content"]) if is_valid else result["content"],
                        "metadata": {
                            "model": result["model"],
                            "confidence": confidence,
                            "issues": issues,
                            "tokens_used": result["usage"]["total_tokens"],
                            "attempt": attempt + 1
                        }
                    }
                
                logger.warning(f"分析质量不足，重试 {attempt + 1}/{max_retries}")
                
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                logger.error(f"分析失败，重试 {attempt + 1}/{max_retries}: {e}")
                await asyncio.sleep(2 ** attempt)  # 指数退避
        
        raise Exception("论文分析失败")

class OptimizedKnowledgeExtractor:
    """优化的知识提取器"""
    
    def __init__(self):
        self.optimizer = get_ai_optimizer()
        self.prompt_optimizer = PromptOptimizer()
        self._setup_templates()
    
    def _setup_templates(self):
        """设置知识提取模板"""
        
        extraction_template = """
从以下论文中提取知识结构和概念关系：

论文标题：{title}
研究内容：{content}

提取任务：
1. 识别核心概念和支撑概念
2. 分析概念间的依赖关系
3. 确定学习前置知识
4. 评估概念复杂度
5. 估算学习时间

请以JSON格式返回：
{{
    "core_concepts": ["概念1", "概念2"],
    "supporting_concepts": ["支撑概念1", "支撑概念2"],
    "prerequisites": [
        {{"level": "basic", "name": "前置知识1"}},
        {{"level": "advanced", "name": "前置知识2"}}
    ],
    "concept_relationships": [
        {{"concept1": "概念A", "relationship": "depends_on", "concept2": "概念B"}}
    ],
    "difficulty_assessment": "intermediate",
    "estimated_learning_time": 120,
    "knowledge_domains": ["领域1", "领域2"]
}}
"""
        
        self.prompt_optimizer.register_template("concept_extraction", extraction_template)
    
    @optimize_ai_call("concept_extraction", TaskComplexity.MODERATE)
    async def extract_concepts(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """提取概念知识"""
        
        title = paper_data.get("title", "")
        content = paper_data.get("content", "")
        
        # 构建prompt
        messages = self.prompt_optimizer.build_optimized_prompt(
            "concept_extraction",
            {"title": title, "content": content[:8000]},
            use_cot=True
        )
        
        # 选择模型
        model_tier = ModelTier.BALANCED  # 知识提取使用平衡模型
        
        try:
            result = await self.optimizer.cached_completion(
                messages=messages,
                model_tier=model_tier
            )
            
            extracted_data = json.loads(result["content"])
            
            # 后处理：概念去重和标准化
            extracted_data = self._post_process_concepts(extracted_data)
            
            return {
                "concepts": extracted_data,
                "metadata": {
                    "model": result["model"],
                    "tokens_used": result["usage"]["total_tokens"],
                    "extraction_time": datetime.now().isoformat()
                }
            }
            
        except json.JSONDecodeError:
            logger.error("概念提取结果JSON解析失败")
            return {"error": "提取结果格式错误"}
    
    def _post_process_concepts(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """后处理概念数据"""
        
        # 去重和标准化概念
        if "core_concepts" in data:
            data["core_concepts"] = list(set(data["core_concepts"]))
        
        if "supporting_concepts" in data:
            data["supporting_concepts"] = list(set(data["supporting_concepts"]))
        
        # 验证关系的完整性
        if "concept_relationships" in data:
            valid_relationships = []
            all_concepts = set(data.get("core_concepts", []) + data.get("supporting_concepts", []))
            
            for rel in data["concept_relationships"]:
                if rel["concept1"] in all_concepts and rel["concept2"] in all_concepts:
                    valid_relationships.append(rel)
            
            data["concept_relationships"] = valid_relationships
        
        return data

class OptimizedLearningPlaner:
    """优化的学习计划制定器"""
    
    def __init__(self):
        self.optimizer = get_ai_optimizer()
        self.prompt_optimizer = PromptOptimizer()
        self._setup_templates()
    
    def _setup_templates(self):
        """设置学习计划模板"""
        
        planning_template = """
基于以下信息制定个性化学习计划：

用户信息：
- 学习水平：{user_level}
- 每日时间：{daily_hours}小时
- 兴趣领域：{interests}
- 语言偏好：{language}

论文集合：{papers_info}

知识分析：{concept_analysis}

制定要求：
1. 考虑知识依赖关系，合理安排学习顺序
2. 根据用户水平调整学习深度和时间分配
3. 设置阶段性目标和检查点
4. 包含复习和实践环节
5. 提供应急和调整方案

返回JSON格式的详细学习计划。
"""
        
        self.prompt_optimizer.register_template("learning_planning", planning_template)
    
    @optimize_ai_call("learning_planning", TaskComplexity.COMPLEX)
    async def create_learning_plan(self, 
                                 user_profile: Dict[str, Any],
                                 papers: List[Dict[str, Any]],
                                 concepts: Dict[str, Any]) -> Dict[str, Any]:
        """创建学习计划"""
        
        # 准备数据
        papers_info = [
            {
                "title": p.get("title", ""),
                "difficulty": p.get("difficulty_level", "intermediate"),
                "concepts": p.get("core_concepts", [])[:3]
            }
            for p in papers
        ]
        
        # 构建prompt
        messages = self.prompt_optimizer.build_optimized_prompt(
            "learning_planning",
            {
                "user_level": user_profile.get("level", "intermediate"),
                "daily_hours": user_profile.get("daily_hours", 2),
                "interests": user_profile.get("interests", []),
                "language": user_profile.get("language", "Chinese"),
                "papers_info": json.dumps(papers_info, ensure_ascii=False),
                "concept_analysis": json.dumps(concepts, ensure_ascii=False)
            }
        )
        
        # 使用高质量模型进行规划
        result = await self.optimizer.cached_completion(
            messages=messages,
            model_tier=ModelTier.PREMIUM,  # 学习计划使用最好的模型
            use_cache=True,
            cache_ttl=7200  # 2小时缓存
        )
        
        try:
            plan_data = json.loads(result["content"])
            
            # 优化学习计划
            optimized_plan = self._optimize_plan(plan_data, user_profile)
            
            return {
                "learning_plan": optimized_plan,
                "metadata": {
                    "model": result["model"],
                    "tokens_used": result["usage"]["total_tokens"],
                    "created_at": datetime.now().isoformat(),
                    "user_level": user_profile.get("level")
                }
            }
            
        except json.JSONDecodeError:
            logger.error("学习计划JSON解析失败")
            return {"error": "计划生成格式错误"}
    
    def _optimize_plan(self, plan: Dict[str, Any], user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """优化学习计划"""
        
        user_level = user_profile.get("level", "intermediate")
        daily_hours = user_profile.get("daily_hours", 2)
        
        # 根据用户水平调整
        if user_level == "beginner":
            # 为初学者增加更多基础时间
            if "total_duration_days" in plan:
                plan["total_duration_days"] = int(plan["total_duration_days"] * 1.3)
            
            # 添加基础资源
            if "resource_requirements" not in plan:
                plan["resource_requirements"] = []
            plan["resource_requirements"].extend([
                "基础教材和综述文章",
                "在线课程和视频资料",
                "术语词汇表"
            ])
        
        elif user_level == "advanced":
            # 为高级用户增加挑战性内容
            if "learning_milestones" not in plan:
                plan["learning_milestones"] = []
            plan["learning_milestones"].extend([
                "完成代码实现和实验",
                "进行批判性分析",
                "撰写技术总结"
            ])
        
        # 根据时间调整计划密度
        if daily_hours < 1.5:
            if "total_duration_days" in plan:
                plan["total_duration_days"] = int(plan["total_duration_days"] * 1.4)
        elif daily_hours > 3:
            if "total_duration_days" in plan:
                plan["total_duration_days"] = int(plan["total_duration_days"] * 0.8)
        
        return plan

class OptimizedAgentOrchestrator:
    """优化的Agent编排器"""
    
    def __init__(self):
        self.paper_analysisor = OptimizedPaperAnalysisor()
        self.knowledge_extractor = OptimizedKnowledgeExtractor()
        self.learning_planer = OptimizedLearningPlaner()
        self.batch_processor = BatchProcessor(get_ai_optimizer())
    
    async def process_papers_pipeline(self, 
                                    papers: List[str],
                                    user_profile: Dict[str, Any],
                                    quality_priority: bool = False) -> Dict[str, Any]:
        """处理论文的完整流水线"""
        
        start_time = datetime.now()
        
        try:
            # 第一阶段：并行分析所有论文
            logger.info(f"开始分析 {len(papers)} 篇论文")
            
            analysis_tasks = [
                {"content": paper, "quality_priority": quality_priority}
                for paper in papers
            ]
            
            analysis_results = await self.batch_processor.process_batch(
                analysis_tasks, "paper_analysis"
            )
            
            successful_analyses = [r for r in analysis_results if r["success"]]
            
            if not successful_analyses:
                raise Exception("所有论文分析都失败了")
            
            # 第二阶段：并行提取概念
            logger.info("开始提取概念知识")
            
            concept_tasks = []
            for result in successful_analyses:
                if "result" in result and "analysis" in result["result"]:
                    concept_tasks.append({
                        "title": result["result"]["analysis"].get("title", ""),
                        "content": result["result"]["analysis"].get("research_problem", "") + 
                                  result["result"]["analysis"].get("main_method", "")
                    })
            
            if concept_tasks:
                concept_results = await asyncio.gather(*[
                    self.knowledge_extractor.extract_concepts(task)
                    for task in concept_tasks
                ], return_exceptions=True)
                
                valid_concepts = [
                    r for r in concept_results 
                    if not isinstance(r, Exception) and "concepts" in r
                ]
            else:
                valid_concepts = []
            
            # 第三阶段：生成学习计划
            logger.info("生成学习计划")
            
            paper_data = [r["result"]["analysis"] for r in successful_analyses if "result" in r]
            concept_data = [c["concepts"] for c in valid_concepts]
            
            if paper_data:
                learning_plan = await self.learning_planer.create_learning_plan(
                    user_profile, paper_data, {"concepts": concept_data}
                )
            else:
                learning_plan = {"error": "无法生成学习计划"}
            
            # 编译最终结果
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            return {
                "status": "success",
                "processing_time": processing_time,
                "papers_processed": len(successful_analyses),
                "papers_failed": len(papers) - len(successful_analyses),
                "analysis_results": successful_analyses,
                "concept_extraction": valid_concepts,
                "learning_plan": learning_plan,
                "metadata": {
                    "started_at": start_time.isoformat(),
                    "completed_at": end_time.isoformat(),
                    "quality_priority": quality_priority,
                    "user_level": user_profile.get("level")
                }
            }
            
        except Exception as e:
            logger.error(f"流水线处理失败: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "processing_time": (datetime.now() - start_time).total_seconds()
            }

# 全局实例
_orchestrator_instance = None

def get_optimized_orchestrator() -> OptimizedAgentOrchestrator:
    """获取优化的编排器实例"""
    global _orchestrator_instance
    if _orchestrator_instance is None:
        _orchestrator_instance = OptimizedAgentOrchestrator()
    return _orchestrator_instance