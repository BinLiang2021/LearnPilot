"""
Learning Planer Agent
学习计划制定Agent，使用LLM生成个性化学习计划
"""

import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timedelta

from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent
from src.learn_pilot.core.config.config import OPENAI_API_KEY, LANGUAGE

logger = logging.getLogger(__name__)

class StudySession(BaseModel):
    day: int = Field(description="学习日期(相对天数)")
    paper_id: str = Field(description="论文ID")
    paper_title: str = Field(description="论文标题")
    focus_areas: List[str] = Field(description="重点学习内容")
    estimated_hours: float = Field(description="预计学习时长")
    learning_objectives: List[str] = Field(description="学习目标")
    
class WeeklyPlan(BaseModel):
    week_number: int = Field(description="第几周")
    sessions: List[StudySession] = Field(description="本周学习安排")
    weekly_goals: List[str] = Field(description="本周学习目标")
    review_topics: List[str] = Field(description="复习主题")

class LearningPlanOutput(BaseModel):
    """学习计划输出结构"""
    plan_overview: str = Field(description="计划总览")
    total_duration_days: int = Field(description="总计划时长(天)")
    weekly_plans: List[WeeklyPlan] = Field(description="每周学习计划")
    learning_milestones: List[str] = Field(description="学习里程碑")
    assessment_schedule: List[str] = Field(description="评估时间表")
    resource_requirements: List[str] = Field(description="所需资源清单")
    success_metrics: List[str] = Field(description="成功评估指标")
    contingency_plans: List[str] = Field(description="应急计划")

class LearningPlaner:
    """学习计划制定器Agent - LLM驱动版本"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.model = self.config.get("model", "gpt-4o-2024-11-20")
        
    async def create_learning_plan(self, 
                                 user_profile: Dict[str, Any],
                                 paper_analysis: Dict[str, Any],
                                 knowledge_extraction: Dict[str, Any],
                                 dependency_graph: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """创建个性化学习计划"""
        try:
            self.logger.info("📅 开始创建学习计划")
            
            # 分析用户需求和论文复杂度
            plan_requirements = self._analyze_planning_requirements(
                user_profile, paper_analysis, knowledge_extraction, dependency_graph
            )
            
            # 构建计划生成提示
            planning_prompt = self._build_planning_prompt(plan_requirements)
            
            # 使用LLM生成学习计划
            agent = StructuredOutputAgent(
                api_key=OPENAI_API_KEY,
                model=self.model,
                output_model=LearningPlanOutput,
                language=LANGUAGE
            )
            
            plan_result = await agent.process(planning_prompt)
            
            # 优化和调整计划
            optimized_plan = self._optimize_plan(plan_result, user_profile)
            
            self.logger.info("✅ 学习计划生成完成")
            return {
                "learning_plan": optimized_plan,
                "user_level": user_profile.get("level", "intermediate"),
                "total_papers": len(paper_analysis.get("papers", [])),
                "plan_created_at": datetime.now().isoformat(),
                "estimated_completion": (datetime.now() + timedelta(days=optimized_plan["total_duration_days"])).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"学习计划生成失败: {e}")
            return {"error": str(e)}
    
    def _analyze_planning_requirements(self, 
                                     user_profile: Dict[str, Any],
                                     paper_analysis: Dict[str, Any],
                                     knowledge_extraction: Dict[str, Any],
                                     dependency_graph: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """分析计划制定需求"""
        
        user_level = user_profile.get("level", "intermediate")
        daily_hours = user_profile.get("daily_hours", 2)
        interests = user_profile.get("interests", [])
        
        papers = paper_analysis.get("papers", {})
        concepts = knowledge_extraction.get("concepts", {})
        
        # 计算总体复杂度
        total_complexity = 0
        paper_difficulties = {}
        
        for paper_id, analysis in papers.items():
            difficulty = analysis.get("difficulty_level", "intermediate")
            if difficulty == "beginner":
                complexity = 1
            elif difficulty == "intermediate":
                complexity = 2
            else:
                complexity = 3
            
            paper_difficulties[paper_id] = complexity
            total_complexity += complexity
        
        # 确定学习顺序
        if dependency_graph and "reading_order" in dependency_graph:
            reading_order = dependency_graph["reading_order"]
        else:
            reading_order = sorted(paper_difficulties.keys(), 
                                 key=lambda x: paper_difficulties[x])
        
        # 估算总学习时间
        base_time_per_paper = {
            "beginner": 3,
            "intermediate": 5,
            "advanced": 8
        }
        
        total_hours = 0
        for paper_id in reading_order:
            analysis = papers.get(paper_id, {})
            difficulty = analysis.get("difficulty_level", "intermediate")
            total_hours += base_time_per_paper.get(difficulty, 5)
        
        # 根据用户水平调整时间
        level_multiplier = {
            "beginner": 1.5,
            "intermediate": 1.0,
            "advanced": 0.8
        }
        
        adjusted_hours = total_hours * level_multiplier.get(user_level, 1.0)
        estimated_days = max(1, int(adjusted_hours / daily_hours))
        
        return {
            "user_profile": user_profile,
            "papers": papers,
            "concepts": concepts,
            "reading_order": reading_order,
            "paper_difficulties": paper_difficulties,
            "total_complexity": total_complexity,
            "estimated_hours": adjusted_hours,
            "estimated_days": estimated_days
        }
    
    def _build_planning_prompt(self, requirements: Dict[str, Any]) -> str:
        """构建计划生成提示"""
        
        user_profile = requirements["user_profile"]
        papers = requirements["papers"]
        reading_order = requirements["reading_order"]
        estimated_days = requirements["estimated_days"]
        
        user_level = user_profile.get("level", "intermediate")
        daily_hours = user_profile.get("daily_hours", 2)
        interests = user_profile.get("interests", [])
        
        # 构建论文信息
        papers_info = []
        for paper_id in reading_order:
            paper = papers.get(paper_id, {})
            papers_info.append({
                "id": paper_id,
                "title": paper.get("title", ""),
                "difficulty": paper.get("difficulty_level", "intermediate"),
                "concepts": paper.get("core_concepts", [])[:3],
                "reading_time": paper.get("reading_time_estimate", 60)
            })
        
        prompt = f"""
作为一位专业的学习规划师，请为用户制定详细的论文学习计划。

用户信息：
- 学习水平: {user_level}
- 每日可用时间: {daily_hours}小时
- 兴趣领域: {', '.join(interests)}
- 预计总时长: {estimated_days}天

论文学习序列：
{str(papers_info)}

请制定包含以下内容的详细学习计划：

1. 计划总览和学习路径说明
2. 按周分解的详细学习安排
3. 每日学习任务和重点
4. 学习里程碑和检查点
5. 定期评估和复习安排
6. 所需学习资源清单
7. 成功评估指标
8. 应对困难的应急策略

请确保计划：
- 符合用户的时间安排和学习能力
- 考虑知识的递进性和连贯性
- 包含适量的复习和巩固时间
- 设置合理的学习目标和里程碑
- 提供灵活性以应对学习进度变化

请使用{LANGUAGE}回答。
"""
        return prompt
    
    def _optimize_plan(self, 
                      plan_result: Dict[str, Any], 
                      user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """优化学习计划"""
        
        user_level = user_profile.get("level", "intermediate")
        daily_hours = user_profile.get("daily_hours", 2)
        
        # 根据用户水平调整计划细节
        if user_level == "beginner":
            plan_result["total_duration_days"] = int(plan_result["total_duration_days"] * 1.2)
            plan_result["resource_requirements"].extend([
                "相关领域的基础教科书或综述文章",
                "在线基础课程或教学视频",
                "专业术语词汇表"
            ])
            
        elif user_level == "advanced":
            plan_result["learning_milestones"].extend([
                "完成关键算法的代码实现",
                "进行批判性分析和改进建议",
                "撰写学习心得和技术总结"
            ])
        
        # 根据时间安排调整计划密度
        if daily_hours < 1.5:
            plan_result["total_duration_days"] = int(plan_result["total_duration_days"] * 1.3)
            plan_result["contingency_plans"].append("如时间不足，优先掌握核心概念和主要方法")
            
        elif daily_hours > 3:
            plan_result["learning_milestones"].append("完成相关实验或案例研究")
            plan_result["success_metrics"].append("能够应用所学知识解决实际问题")
        
        return plan_result

if __name__ == "__main__":
    planer = LearningPlaner()
    print("LearningPlaner 初始化完成")