"""
AI System Monitoring and Analytics
AI系统监控和分析工具
"""

import json
import time
import asyncio
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import logging
import sqlite3
from pathlib import Path

logger = logging.getLogger(__name__)

@dataclass
class AIMetrics:
    """AI指标数据"""
    timestamp: float
    task_type: str
    model: str
    response_time: float
    success: bool
    cost: float
    input_tokens: int
    output_tokens: int
    quality_score: float = 0.0
    user_id: Optional[str] = None
    session_id: Optional[str] = None

class AIMonitoringSystem:
    """AI系统监控"""
    
    def __init__(self, db_path: str = "ai_monitoring.db"):
        self.db_path = db_path
        self.metrics_buffer = deque(maxlen=1000)  # 内存缓冲区
        self.real_time_stats = {
            "requests_per_minute": deque(maxlen=60),
            "error_counts": defaultdict(int),
            "cost_tracking": defaultdict(float),
            "response_times": defaultdict(list)
        }
        
        self._init_database()
        self._start_background_tasks()
    
    def _init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ai_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                task_type TEXT NOT NULL,
                model TEXT NOT NULL,
                response_time REAL NOT NULL,
                success BOOLEAN NOT NULL,
                cost REAL NOT NULL,
                input_tokens INTEGER NOT NULL,
                output_tokens INTEGER NOT NULL,
                quality_score REAL DEFAULT 0.0,
                user_id TEXT,
                session_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON ai_metrics(timestamp);
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_task_type ON ai_metrics(task_type);
        """)
        
        conn.commit()
        conn.close()
    
    def _start_background_tasks(self):
        """启动后台任务"""
        asyncio.create_task(self._periodic_flush())
        asyncio.create_task(self._update_real_time_stats())
    
    async def _periodic_flush(self):
        """定期刷新到数据库"""
        while True:
            await asyncio.sleep(30)  # 每30秒刷新一次
            self.flush_to_database()
    
    async def _update_real_time_stats(self):
        """更新实时统计"""
        while True:
            await asyncio.sleep(1)  # 每秒更新
            current_time = time.time()
            
            # 更新每分钟请求数
            minute_ago = current_time - 60
            recent_requests = sum(1 for m in self.metrics_buffer 
                                if m.timestamp > minute_ago)
            self.real_time_stats["requests_per_minute"].append(recent_requests)
    
    def record_metric(self, metric: AIMetrics):
        """记录指标"""
        self.metrics_buffer.append(metric)
        
        # 更新实时统计
        task_type = metric.task_type
        
        if not metric.success:
            self.real_time_stats["error_counts"][task_type] += 1
        
        self.real_time_stats["cost_tracking"][task_type] += metric.cost
        
        # 保持响应时间历史（最近100个）
        if len(self.real_time_stats["response_times"][task_type]) >= 100:
            self.real_time_stats["response_times"][task_type].pop(0)
        self.real_time_stats["response_times"][task_type].append(metric.response_time)
    
    def flush_to_database(self):
        """刷新到数据库"""
        if not self.metrics_buffer:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 批量插入
        metrics_data = []
        while self.metrics_buffer:
            metric = self.metrics_buffer.popleft()
            metrics_data.append((
                metric.timestamp,
                metric.task_type,
                metric.model,
                metric.response_time,
                metric.success,
                metric.cost,
                metric.input_tokens,
                metric.output_tokens,
                metric.quality_score,
                metric.user_id,
                metric.session_id
            ))
        
        cursor.executemany("""
            INSERT INTO ai_metrics 
            (timestamp, task_type, model, response_time, success, cost,
             input_tokens, output_tokens, quality_score, user_id, session_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, metrics_data)
        
        conn.commit()
        conn.close()
        
        logger.info(f"刷新 {len(metrics_data)} 条指标到数据库")
    
    def get_real_time_dashboard(self) -> Dict[str, Any]:
        """获取实时仪表板数据"""
        current_time = time.time()
        hour_ago = current_time - 3600
        
        # 从数据库获取最近一小时的数据
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总体统计
        cursor.execute("""
            SELECT COUNT(*), AVG(response_time), SUM(cost), 
                   SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count
            FROM ai_metrics 
            WHERE timestamp > ?
        """, (hour_ago,))
        
        total_requests, avg_response_time, total_cost, success_count = cursor.fetchone()
        
        success_rate = (success_count / total_requests) if total_requests > 0 else 0
        
        # 按任务类型统计
        cursor.execute("""
            SELECT task_type, COUNT(*), AVG(response_time), SUM(cost),
                   AVG(quality_score), SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END)
            FROM ai_metrics 
            WHERE timestamp > ?
            GROUP BY task_type
        """, (hour_ago,))
        
        task_stats = {}
        for row in cursor.fetchall():
            task_type, count, avg_time, cost, avg_quality, successes = row
            task_stats[task_type] = {
                "requests": count,
                "avg_response_time": round(avg_time, 2) if avg_time else 0,
                "total_cost": round(cost, 4) if cost else 0,
                "avg_quality": round(avg_quality, 2) if avg_quality else 0,
                "success_rate": round(successes / count, 2) if count > 0 else 0
            }
        
        # 模型使用统计
        cursor.execute("""
            SELECT model, COUNT(*), SUM(cost), AVG(response_time)
            FROM ai_metrics 
            WHERE timestamp > ?
            GROUP BY model
        """, (hour_ago,))
        
        model_stats = {}
        for row in cursor.fetchall():
            model, count, cost, avg_time = row
            model_stats[model] = {
                "requests": count,
                "total_cost": round(cost, 4) if cost else 0,
                "avg_response_time": round(avg_time, 2) if avg_time else 0
            }
        
        conn.close()
        
        # 实时请求率
        current_rpm = list(self.real_time_stats["requests_per_minute"])[-1] if self.real_time_stats["requests_per_minute"] else 0
        
        return {
            "overview": {
                "total_requests_hour": total_requests or 0,
                "avg_response_time": round(avg_response_time, 2) if avg_response_time else 0,
                "total_cost_hour": round(total_cost, 4) if total_cost else 0,
                "success_rate": round(success_rate, 2),
                "requests_per_minute": current_rpm
            },
            "by_task": task_stats,
            "by_model": model_stats,
            "alerts": self._check_alerts()
        }
    
    def _check_alerts(self) -> List[Dict[str, Any]]:
        """检查告警"""
        alerts = []
        
        # 检查错误率
        total_requests = sum(len(times) for times in self.real_time_stats["response_times"].values())
        total_errors = sum(self.real_time_stats["error_counts"].values())
        
        if total_requests > 0:
            error_rate = total_errors / total_requests
            if error_rate > 0.1:  # 错误率超过10%
                alerts.append({
                    "type": "high_error_rate",
                    "message": f"错误率过高: {error_rate:.2%}",
                    "severity": "critical" if error_rate > 0.2 else "warning"
                })
        
        # 检查响应时间
        for task_type, times in self.real_time_stats["response_times"].items():
            if times:
                avg_time = sum(times) / len(times)
                if avg_time > 10:  # 响应时间超过10秒
                    alerts.append({
                        "type": "slow_response",
                        "message": f"{task_type} 响应时间过慢: {avg_time:.2f}秒",
                        "severity": "warning"
                    })
        
        # 检查成本
        total_cost = sum(self.real_time_stats["cost_tracking"].values())
        if total_cost > 100:  # 小时成本超过$100
            alerts.append({
                "type": "high_cost",
                "message": f"小时成本过高: ${total_cost:.2f}",
                "severity": "warning"
            })
        
        return alerts
    
    def get_performance_report(self, 
                              start_time: Optional[datetime] = None,
                              end_time: Optional[datetime] = None) -> Dict[str, Any]:
        """获取性能报告"""
        
        if not start_time:
            start_time = datetime.now() - timedelta(days=1)
        if not end_time:
            end_time = datetime.now()
        
        start_timestamp = start_time.timestamp()
        end_timestamp = end_time.timestamp()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 性能趋势
        cursor.execute("""
            SELECT 
                strftime('%H', datetime(timestamp, 'unixepoch')) as hour,
                COUNT(*) as requests,
                AVG(response_time) as avg_response_time,
                SUM(cost) as total_cost,
                AVG(quality_score) as avg_quality
            FROM ai_metrics
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY hour
            ORDER BY hour
        """, (start_timestamp, end_timestamp))
        
        hourly_stats = []
        for row in cursor.fetchall():
            hour, requests, avg_time, cost, quality = row
            hourly_stats.append({
                "hour": int(hour),
                "requests": requests,
                "avg_response_time": round(avg_time, 2) if avg_time else 0,
                "total_cost": round(cost, 4) if cost else 0,
                "avg_quality": round(quality, 2) if quality else 0
            })
        
        # 质量分析
        cursor.execute("""
            SELECT task_type, AVG(quality_score), COUNT(*)
            FROM ai_metrics
            WHERE timestamp BETWEEN ? AND ? AND quality_score > 0
            GROUP BY task_type
        """, (start_timestamp, end_timestamp))
        
        quality_by_task = {}
        for row in cursor.fetchall():
            task_type, avg_quality, count = row
            quality_by_task[task_type] = {
                "avg_quality": round(avg_quality, 2),
                "sample_size": count
            }
        
        # 成本分析
        cursor.execute("""
            SELECT model, SUM(cost), COUNT(*), 
                   SUM(input_tokens), SUM(output_tokens)
            FROM ai_metrics
            WHERE timestamp BETWEEN ? AND ?
            GROUP BY model
        """, (start_timestamp, end_timestamp))
        
        cost_by_model = {}
        for row in cursor.fetchall():
            model, cost, requests, input_tokens, output_tokens = row
            cost_by_model[model] = {
                "total_cost": round(cost, 4) if cost else 0,
                "requests": requests,
                "input_tokens": input_tokens or 0,
                "output_tokens": output_tokens or 0,
                "cost_per_request": round(cost / requests, 4) if requests > 0 and cost else 0
            }
        
        conn.close()
        
        return {
            "period": {
                "start": start_time.isoformat(),
                "end": end_time.isoformat()
            },
            "hourly_trends": hourly_stats,
            "quality_analysis": quality_by_task,
            "cost_analysis": cost_by_model,
            "summary": self._calculate_summary_stats(start_timestamp, end_timestamp)
        }
    
    def _calculate_summary_stats(self, start_time: float, end_time: float) -> Dict[str, Any]:
        """计算汇总统计"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_requests,
                SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as successful_requests,
                AVG(response_time) as avg_response_time,
                MAX(response_time) as max_response_time,
                SUM(cost) as total_cost,
                AVG(quality_score) as avg_quality,
                SUM(input_tokens) as total_input_tokens,
                SUM(output_tokens) as total_output_tokens
            FROM ai_metrics
            WHERE timestamp BETWEEN ? AND ?
        """, (start_time, end_time))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row or not row[0]:
            return {}
        
        (total_requests, successful_requests, avg_response_time, 
         max_response_time, total_cost, avg_quality, 
         total_input_tokens, total_output_tokens) = row
        
        return {
            "total_requests": total_requests,
            "success_rate": round(successful_requests / total_requests, 3) if total_requests > 0 else 0,
            "avg_response_time": round(avg_response_time, 2) if avg_response_time else 0,
            "max_response_time": round(max_response_time, 2) if max_response_time else 0,
            "total_cost": round(total_cost, 4) if total_cost else 0,
            "avg_quality_score": round(avg_quality, 2) if avg_quality else 0,
            "total_tokens": (total_input_tokens or 0) + (total_output_tokens or 0),
            "cost_per_request": round(total_cost / total_requests, 4) if total_requests > 0 and total_cost else 0
        }

class PerformanceBenchmark:
    """性能基准测试"""
    
    def __init__(self, monitoring_system: AIMonitoringSystem):
        self.monitoring = monitoring_system
        self.benchmark_results = {}
    
    async def run_benchmark_suite(self) -> Dict[str, Any]:
        """运行基准测试套件"""
        
        logger.info("开始运行AI系统基准测试")
        
        benchmarks = {
            "paper_analysis_speed": self._benchmark_paper_analysis,
            "concept_extraction_accuracy": self._benchmark_concept_extraction,
            "concurrent_processing": self._benchmark_concurrent_processing,
            "cache_performance": self._benchmark_cache_performance
        }
        
        results = {}
        
        for benchmark_name, benchmark_func in benchmarks.items():
            try:
                logger.info(f"运行基准测试: {benchmark_name}")
                result = await benchmark_func()
                results[benchmark_name] = result
                logger.info(f"基准测试 {benchmark_name} 完成")
            except Exception as e:
                logger.error(f"基准测试 {benchmark_name} 失败: {e}")
                results[benchmark_name] = {"error": str(e)}
        
        # 生成综合评分
        results["overall_score"] = self._calculate_overall_score(results)
        
        return results
    
    async def _benchmark_paper_analysis(self) -> Dict[str, Any]:
        """基准测试论文分析性能"""
        
        from .optimized_agents import OptimizedPaperAnalysisor
        
        analyzer = OptimizedPaperAnalysisor()
        
        # 测试用例
        test_papers = [
            "This paper introduces a novel neural network architecture...",  # 短文本
            "Abstract: " + "A" * 1000 + " Introduction: " + "B" * 2000,  # 中等长度
            "Full paper content: " + "C" * 5000 + " Methodology: " + "D" * 3000  # 长文本
        ]
        
        results = []
        
        for i, paper in enumerate(test_papers):
            start_time = time.time()
            
            try:
                result = await analyzer.analyze_paper(paper)
                response_time = time.time() - start_time
                
                results.append({
                    "paper_length": len(paper),
                    "response_time": response_time,
                    "success": True,
                    "tokens_used": result.get("metadata", {}).get("tokens_used", 0)
                })
                
            except Exception as e:
                results.append({
                    "paper_length": len(paper),
                    "response_time": time.time() - start_time,
                    "success": False,
                    "error": str(e)
                })
        
        # 计算统计数据
        successful_results = [r for r in results if r["success"]]
        
        return {
            "total_tests": len(results),
            "successful_tests": len(successful_results),
            "avg_response_time": sum(r["response_time"] for r in successful_results) / len(successful_results) if successful_results else 0,
            "avg_tokens_per_test": sum(r.get("tokens_used", 0) for r in successful_results) / len(successful_results) if successful_results else 0,
            "results": results
        }
    
    async def _benchmark_concept_extraction(self) -> Dict[str, Any]:
        """基准测试概念提取准确性"""
        
        from .optimized_agents import OptimizedKnowledgeExtractor
        
        extractor = OptimizedKnowledgeExtractor()
        
        # 测试用例（已知正确答案）
        test_cases = [
            {
                "title": "Attention Is All You Need",
                "content": "We propose the Transformer, a model architecture based solely on attention mechanisms...",
                "expected_concepts": ["attention mechanism", "transformer", "encoder-decoder"]
            },
            {
                "title": "BERT: Pre-training of Deep Bidirectional Transformers",
                "content": "BERT is designed to pre-train deep bidirectional representations...",
                "expected_concepts": ["BERT", "bidirectional", "pre-training", "transformer"]
            }
        ]
        
        results = []
        
        for test_case in test_cases:
            try:
                result = await extractor.extract_concepts(test_case)
                
                extracted_concepts = result.get("concepts", {}).get("core_concepts", [])
                expected_concepts = test_case["expected_concepts"]
                
                # 计算准确性（简单的重叠度量）
                intersection = set(extracted_concepts) & set(expected_concepts)
                precision = len(intersection) / len(extracted_concepts) if extracted_concepts else 0
                recall = len(intersection) / len(expected_concepts) if expected_concepts else 0
                f1_score = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
                
                results.append({
                    "title": test_case["title"],
                    "extracted_concepts": extracted_concepts,
                    "expected_concepts": expected_concepts,
                    "precision": precision,
                    "recall": recall,
                    "f1_score": f1_score
                })
                
            except Exception as e:
                results.append({
                    "title": test_case["title"],
                    "error": str(e),
                    "success": False
                })
        
        successful_results = [r for r in results if "f1_score" in r]
        
        return {
            "total_tests": len(results),
            "successful_tests": len(successful_results),
            "avg_precision": sum(r["precision"] for r in successful_results) / len(successful_results) if successful_results else 0,
            "avg_recall": sum(r["recall"] for r in successful_results) / len(successful_results) if successful_results else 0,
            "avg_f1_score": sum(r["f1_score"] for r in successful_results) / len(successful_results) if successful_results else 0,
            "results": results
        }
    
    async def _benchmark_concurrent_processing(self) -> Dict[str, Any]:
        """基准测试并发处理性能"""
        
        from .optimized_agents import OptimizedPaperAnalysisor
        
        analyzer = OptimizedPaperAnalysisor()
        
        # 创建多个并发任务
        test_paper = "Sample paper content for concurrent processing test..."
        concurrent_levels = [1, 5, 10, 20]
        
        results = {}
        
        for level in concurrent_levels:
            start_time = time.time()
            
            # 创建并发任务
            tasks = [analyzer.analyze_paper(test_paper) for _ in range(level)]
            
            try:
                # 执行并发任务
                task_results = await asyncio.gather(*tasks, return_exceptions=True)
                
                total_time = time.time() - start_time
                successful_tasks = sum(1 for r in task_results if not isinstance(r, Exception))
                
                results[f"concurrent_{level}"] = {
                    "total_tasks": level,
                    "successful_tasks": successful_tasks,
                    "total_time": total_time,
                    "avg_time_per_task": total_time / level,
                    "throughput": successful_tasks / total_time if total_time > 0 else 0
                }
                
            except Exception as e:
                results[f"concurrent_{level}"] = {"error": str(e)}
        
        return results
    
    async def _benchmark_cache_performance(self) -> Dict[str, Any]:
        """基准测试缓存性能"""
        
        from .optimization import get_ai_optimizer
        
        optimizer = get_ai_optimizer()
        
        test_messages = [
            {"role": "user", "content": "What is machine learning?"}
        ]
        
        # 清空缓存
        optimizer.cache.clear()
        
        # 第一次调用（无缓存）
        start_time = time.time()
        try:
            await optimizer.cached_completion(
                messages=test_messages,
                model_tier=optimizer.ModelTier.FAST,
                use_cache=True
            )
            first_call_time = time.time() - start_time
        except Exception as e:
            return {"error": f"首次调用失败: {str(e)}"}
        
        # 第二次调用（有缓存）
        start_time = time.time()
        try:
            await optimizer.cached_completion(
                messages=test_messages,
                model_tier=optimizer.ModelTier.FAST,
                use_cache=True
            )
            cached_call_time = time.time() - start_time
        except Exception as e:
            return {"error": f"缓存调用失败: {str(e)}"}
        
        speedup_ratio = first_call_time / cached_call_time if cached_call_time > 0 else 0
        
        return {
            "first_call_time": first_call_time,
            "cached_call_time": cached_call_time,
            "speedup_ratio": speedup_ratio,
            "cache_hit_rate": optimizer.stats["cache_hits"] / optimizer.stats["total_requests"] if optimizer.stats["total_requests"] > 0 else 0
        }
    
    def _calculate_overall_score(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """计算综合评分"""
        
        scores = {}
        
        # 速度评分（基于响应时间）
        if "paper_analysis_speed" in results and "avg_response_time" in results["paper_analysis_speed"]:
            avg_time = results["paper_analysis_speed"]["avg_response_time"]
            # 2秒以下得满分，超过10秒得0分
            speed_score = max(0, min(100, 100 - (avg_time - 2) * 12.5))
            scores["speed_score"] = round(speed_score, 1)
        
        # 准确性评分（基于F1分数）
        if "concept_extraction_accuracy" in results and "avg_f1_score" in results["concept_extraction_accuracy"]:
            f1_score = results["concept_extraction_accuracy"]["avg_f1_score"]
            accuracy_score = f1_score * 100
            scores["accuracy_score"] = round(accuracy_score, 1)
        
        # 并发性能评分
        if "concurrent_processing" in results:
            concurrent_results = results["concurrent_processing"]
            if "concurrent_10" in concurrent_results:
                throughput = concurrent_results["concurrent_10"].get("throughput", 0)
                # 1 req/s得满分
                concurrency_score = min(100, throughput * 100)
                scores["concurrency_score"] = round(concurrency_score, 1)
        
        # 缓存效率评分
        if "cache_performance" in results and "speedup_ratio" in results["cache_performance"]:
            speedup = results["cache_performance"]["speedup_ratio"]
            # 10倍加速得满分
            cache_score = min(100, speedup * 10)
            scores["cache_score"] = round(cache_score, 1)
        
        # 计算总分
        if scores:
            total_score = sum(scores.values()) / len(scores)
            scores["overall_score"] = round(total_score, 1)
            
            # 评级
            if total_score >= 90:
                scores["grade"] = "A+"
            elif total_score >= 80:
                scores["grade"] = "A"
            elif total_score >= 70:
                scores["grade"] = "B"
            elif total_score >= 60:
                scores["grade"] = "C"
            else:
                scores["grade"] = "D"
        
        return scores

# 全局实例
_monitoring_system = None

def get_monitoring_system() -> AIMonitoringSystem:
    """获取监控系统实例"""
    global _monitoring_system
    if _monitoring_system is None:
        _monitoring_system = AIMonitoringSystem()
    return _monitoring_system