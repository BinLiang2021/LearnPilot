"""
AI System Optimization Module
Advanced LLM calling, caching, and performance optimization
"""

import asyncio
import hashlib
import json
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import logging
from functools import wraps
from contextlib import asynccontextmanager

import aiohttp
import openai
from openai import AsyncOpenAI
import tiktoken

logger = logging.getLogger(__name__)

class ModelTier(Enum):
    """模型层级定义"""
    FAST = "gpt-3.5-turbo"           # 快速、低成本
    BALANCED = "gpt-4o-mini"         # 平衡性能和成本
    PREMIUM = "gpt-4o"               # 高质量、高成本

@dataclass
class ModelConfig:
    """模型配置"""
    name: str
    cost_per_token: float
    max_tokens: int
    temperature: float = 0.7
    quality_score: float = 0.8

# 模型配置映射
MODEL_CONFIGS = {
    ModelTier.FAST: ModelConfig("gpt-3.5-turbo", 0.002, 4096, 0.7, 0.7),
    ModelTier.BALANCED: ModelConfig("gpt-4o-mini", 0.15, 8192, 0.7, 0.85),
    ModelTier.PREMIUM: ModelConfig("gpt-4o", 0.60, 8192, 0.7, 0.95),
}

class TaskComplexity(Enum):
    """任务复杂度评估"""
    SIMPLE = 1      # 简单任务：分类、提取
    MODERATE = 2    # 中等任务：总结、分析
    COMPLEX = 3     # 复杂任务：推理、创作

class AIOptimizer:
    """AI系统优化器"""
    
    def __init__(self, api_key: str, max_concurrent: int = 10):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=api_key)
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.cache = {}
        self.stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "total_cost": 0.0,
            "avg_response_time": 0.0,
            "error_count": 0
        }
        
    async def smart_model_selection(self, 
                                   task_complexity: TaskComplexity,
                                   content_length: int,
                                   quality_priority: bool = False) -> ModelTier:
        """智能模型选择"""
        
        # 基于任务复杂度的基础选择
        if task_complexity == TaskComplexity.SIMPLE:
            base_model = ModelTier.FAST
        elif task_complexity == TaskComplexity.MODERATE:
            base_model = ModelTier.BALANCED
        else:
            base_model = ModelTier.PREMIUM
            
        # 基于内容长度调整
        if content_length > 4000:  # 长文本需要更强模型
            if base_model == ModelTier.FAST:
                base_model = ModelTier.BALANCED
        
        # 质量优先模式
        if quality_priority and base_model != ModelTier.PREMIUM:
            base_model = ModelTier.BALANCED if base_model == ModelTier.FAST else ModelTier.PREMIUM
            
        return base_model

    def _create_cache_key(self, messages: List[Dict], model: str, **kwargs) -> str:
        """创建缓存键"""
        content = json.dumps({
            "messages": messages,
            "model": model,
            **kwargs
        }, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()

    async def cached_completion(self, 
                               messages: List[Dict],
                               model_tier: ModelTier,
                               use_cache: bool = True,
                               cache_ttl: int = 3600,
                               **kwargs) -> Dict[str, Any]:
        """带缓存的completion调用"""
        
        model_config = MODEL_CONFIGS[model_tier]
        cache_key = self._create_cache_key(messages, model_config.name, **kwargs)
        
        # 检查缓存
        if use_cache and cache_key in self.cache:
            cache_data = self.cache[cache_key]
            if time.time() - cache_data['timestamp'] < cache_ttl:
                self.stats["cache_hits"] += 1
                logger.debug(f"缓存命中: {cache_key[:8]}")
                return cache_data['response']
        
        # API调用
        start_time = time.time()
        async with self.semaphore:  # 限制并发数
            try:
                response = await self.client.chat.completions.create(
                    model=model_config.name,
                    messages=messages,
                    temperature=model_config.temperature,
                    max_tokens=kwargs.get('max_tokens', model_config.max_tokens),
                    **{k: v for k, v in kwargs.items() if k != 'max_tokens'}
                )
                
                # 统计信息更新
                response_time = time.time() - start_time
                self._update_stats(response, model_config, response_time)
                
                # 转换为字典格式
                result = {
                    "content": response.choices[0].message.content,
                    "model": response.model,
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens,
                        "completion_tokens": response.usage.completion_tokens,
                        "total_tokens": response.usage.total_tokens
                    }
                }
                
                # 缓存结果
                if use_cache:
                    self.cache[cache_key] = {
                        "response": result,
                        "timestamp": time.time()
                    }
                
                return result
                
            except Exception as e:
                self.stats["error_count"] += 1
                logger.error(f"API调用失败: {e}")
                raise
    
    def _update_stats(self, response, model_config: ModelConfig, response_time: float):
        """更新统计信息"""
        self.stats["total_requests"] += 1
        
        # 计算成本
        if hasattr(response, 'usage'):
            cost = response.usage.total_tokens * model_config.cost_per_token / 1000
            self.stats["total_cost"] += cost
        
        # 更新平均响应时间
        self.stats["avg_response_time"] = (
            (self.stats["avg_response_time"] * (self.stats["total_requests"] - 1) + response_time) 
            / self.stats["total_requests"]
        )

class PromptOptimizer:
    """Prompt优化器"""
    
    def __init__(self):
        self.templates = {}
        self.examples = {}
    
    def register_template(self, task_type: str, template: str, examples: List[Dict] = None):
        """注册prompt模板"""
        self.templates[task_type] = template
        if examples:
            self.examples[task_type] = examples
    
    def build_optimized_prompt(self, 
                              task_type: str,
                              context: Dict[str, Any],
                              use_cot: bool = True,
                              use_examples: bool = True) -> List[Dict[str, str]]:
        """构建优化的prompt"""
        
        if task_type not in self.templates:
            raise ValueError(f"未知任务类型: {task_type}")
        
        messages = [
            {"role": "system", "content": self._build_system_prompt(task_type, use_cot)}
        ]
        
        # 添加few-shot examples
        if use_examples and task_type in self.examples:
            for example in self.examples[task_type]:
                messages.extend([
                    {"role": "user", "content": example["input"]},
                    {"role": "assistant", "content": example["output"]}
                ])
        
        # 添加用户查询
        user_prompt = self.templates[task_type].format(**context)
        messages.append({"role": "user", "content": user_prompt})
        
        return messages
    
    def _build_system_prompt(self, task_type: str, use_cot: bool) -> str:
        """构建系统prompt"""
        base_prompts = {
            "paper_analysis": "你是一位专业的学术论文分析专家，擅长快速理解和分析研究论文的核心内容。",
            "concept_extraction": "你是一位知识工程专家，专门从学术文献中提取和组织概念知识。",
            "learning_planning": "你是一位经验丰富的学习规划师，专门为研究人员制定个性化学习计划。",
            "knowledge_graph": "你是一位知识图谱专家，擅长分析概念间的关系和依赖。",
            "task_generation": "你是一位教育专家，专门设计学习任务和练习题目。"
        }
        
        prompt = base_prompts.get(task_type, "你是一位AI助手。")
        
        if use_cot:
            prompt += "\n\n请按以下步骤思考：\n1. 分析输入内容的关键信息\n2. 确定处理策略和方法\n3. 逐步执行分析过程\n4. 整理和验证结果\n5. 提供结构化的最终输出"
        
        return prompt

class QualityValidator:
    """输出质量验证器"""
    
    def __init__(self):
        self.validators = {}
    
    def register_validator(self, task_type: str, validator_func):
        """注册验证函数"""
        self.validators[task_type] = validator_func
    
    async def validate_output(self, 
                             task_type: str, 
                             output: str,
                             context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
        """验证输出质量"""
        
        if task_type not in self.validators:
            return True, 1.0, []
        
        try:
            is_valid, confidence, issues = await self.validators[task_type](output, context)
            return is_valid, confidence, issues
        except Exception as e:
            logger.error(f"验证失败: {e}")
            return False, 0.0, [f"验证错误: {str(e)}"]

def paper_analysis_validator(output: str, context: Dict[str, Any]) -> Tuple[bool, float, List[str]]:
    """论文分析验证器"""
    issues = []
    confidence = 1.0
    
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return False, 0.0, ["输出格式不是有效的JSON"]
    
    required_fields = ["title", "research_problem", "main_method", "key_contributions"]
    for field in required_fields:
        if field not in data or not data[field]:
            issues.append(f"缺少必填字段: {field}")
            confidence -= 0.2
    
    # 检查内容质量
    if len(data.get("research_problem", "")) < 50:
        issues.append("研究问题描述过于简短")
        confidence -= 0.1
    
    if len(data.get("key_contributions", [])) == 0:
        issues.append("未提取到关键贡献")
        confidence -= 0.2
    
    is_valid = confidence > 0.6
    return is_valid, max(0.0, confidence), issues

class BatchProcessor:
    """批量处理器"""
    
    def __init__(self, optimizer: AIOptimizer, max_batch_size: int = 5):
        self.optimizer = optimizer
        self.max_batch_size = max_batch_size
    
    async def process_batch(self, 
                           tasks: List[Dict[str, Any]],
                           task_type: str) -> List[Dict[str, Any]]:
        """批量处理任务"""
        
        results = []
        
        # 按batch_size分组
        for i in range(0, len(tasks), self.max_batch_size):
            batch = tasks[i:i + self.max_batch_size]
            
            # 并发处理batch中的任务
            batch_tasks = []
            for task in batch:
                batch_tasks.append(
                    self._process_single_task(task, task_type)
                )
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            
            # 处理结果
            for j, result in enumerate(batch_results):
                if isinstance(result, Exception):
                    logger.error(f"任务处理失败: {result}")
                    results.append({
                        "task_id": batch[j].get("task_id", f"task_{i+j}"),
                        "error": str(result),
                        "success": False
                    })
                else:
                    results.append({
                        "task_id": batch[j].get("task_id", f"task_{i+j}"),
                        "result": result,
                        "success": True
                    })
        
        return results
    
    async def _process_single_task(self, task: Dict[str, Any], task_type: str) -> Any:
        """处理单个任务"""
        
        # 根据任务类型选择处理方法
        if task_type == "paper_analysis":
            return await self._analyze_paper(task)
        elif task_type == "concept_extraction":
            return await self._extract_concepts(task)
        # 可扩展其他任务类型
        
        raise ValueError(f"不支持的任务类型: {task_type}")
    
    async def _analyze_paper(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """分析单篇论文"""
        
        content = task.get("content", "")
        complexity = TaskComplexity.MODERATE
        
        if len(content) > 10000:
            complexity = TaskComplexity.COMPLEX
        elif len(content) < 3000:
            complexity = TaskComplexity.SIMPLE
        
        model_tier = await self.optimizer.smart_model_selection(
            complexity, len(content), task.get("quality_priority", False)
        )
        
        messages = [
            {"role": "system", "content": "分析给定的研究论文，提取关键信息。"},
            {"role": "user", "content": f"请分析以下论文内容：\n\n{content}"}
        ]
        
        result = await self.optimizer.cached_completion(
            messages=messages,
            model_tier=model_tier,
            use_cache=True
        )
        
        return result

class AIMonitor:
    """AI系统监控"""
    
    def __init__(self):
        self.metrics = {
            "response_times": [],
            "error_rates": {},
            "cost_tracking": {},
            "quality_scores": []
        }
    
    def log_request(self, 
                   task_type: str,
                   model: str,
                   response_time: float,
                   success: bool,
                   cost: float,
                   quality_score: float = None):
        """记录请求日志"""
        
        timestamp = time.time()
        
        self.metrics["response_times"].append({
            "timestamp": timestamp,
            "task_type": task_type,
            "response_time": response_time
        })
        
        if task_type not in self.metrics["error_rates"]:
            self.metrics["error_rates"][task_type] = {"total": 0, "errors": 0}
        
        self.metrics["error_rates"][task_type]["total"] += 1
        if not success:
            self.metrics["error_rates"][task_type]["errors"] += 1
        
        if model not in self.metrics["cost_tracking"]:
            self.metrics["cost_tracking"][model] = {"total_cost": 0, "request_count": 0}
        
        self.metrics["cost_tracking"][model]["total_cost"] += cost
        self.metrics["cost_tracking"][model]["request_count"] += 1
        
        if quality_score is not None:
            self.metrics["quality_scores"].append({
                "timestamp": timestamp,
                "task_type": task_type,
                "score": quality_score
            })
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """获取性能摘要"""
        
        summary = {
            "avg_response_time": self._calculate_avg_response_time(),
            "error_rates": self._calculate_error_rates(),
            "total_cost": self._calculate_total_cost(),
            "avg_quality_score": self._calculate_avg_quality_score()
        }
        
        return summary
    
    def _calculate_avg_response_time(self) -> float:
        """计算平均响应时间"""
        if not self.metrics["response_times"]:
            return 0.0
        
        total_time = sum(r["response_time"] for r in self.metrics["response_times"])
        return total_time / len(self.metrics["response_times"])
    
    def _calculate_error_rates(self) -> Dict[str, float]:
        """计算错误率"""
        error_rates = {}
        
        for task_type, data in self.metrics["error_rates"].items():
            if data["total"] > 0:
                error_rates[task_type] = data["errors"] / data["total"]
            else:
                error_rates[task_type] = 0.0
        
        return error_rates
    
    def _calculate_total_cost(self) -> float:
        """计算总成本"""
        return sum(data["total_cost"] for data in self.metrics["cost_tracking"].values())
    
    def _calculate_avg_quality_score(self) -> float:
        """计算平均质量分数"""
        if not self.metrics["quality_scores"]:
            return 0.0
        
        total_score = sum(q["score"] for q in self.metrics["quality_scores"])
        return total_score / len(self.metrics["quality_scores"])

# 全局优化器实例
_optimizer_instance = None
_monitor_instance = None

def get_ai_optimizer() -> AIOptimizer:
    """获取AI优化器实例"""
    global _optimizer_instance
    if _optimizer_instance is None:
        from src.learn_pilot.core.config.config import OPENAI_API_KEY
        _optimizer_instance = AIOptimizer(OPENAI_API_KEY)
    return _optimizer_instance

def get_ai_monitor() -> AIMonitor:
    """获取AI监控实例"""
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = AIMonitor()
    return _monitor_instance

# 装饰器工具
def optimize_ai_call(task_type: str, complexity: TaskComplexity = TaskComplexity.MODERATE):
    """AI调用优化装饰器"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            optimizer = get_ai_optimizer()
            monitor = get_ai_monitor()
            
            try:
                # 执行原函数
                result = await func(*args, **kwargs)
                
                # 记录成功
                response_time = time.time() - start_time
                monitor.log_request(
                    task_type=task_type,
                    model="unknown",  # 从result中提取
                    response_time=response_time,
                    success=True,
                    cost=0.0  # 从optimizer stats中获取
                )
                
                return result
                
            except Exception as e:
                # 记录失败
                response_time = time.time() - start_time
                monitor.log_request(
                    task_type=task_type,
                    model="unknown",
                    response_time=response_time,
                    success=False,
                    cost=0.0
                )
                raise
        
        return wrapper
    return decorator