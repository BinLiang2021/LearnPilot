"""
Guidance Teacher Agent
学习指导老师Agent，使用LLM进行个性化学习指导
"""

import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json

from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent
from src.learn_pilot.core.config.config import OPENAI_API_KEY, LANGUAGE

logger = logging.getLogger(__name__)

class StudyTip(BaseModel):
    category: str = Field(description="学习技巧类别")
    tip: str = Field(description="具体学习建议")
    
class LearningResource(BaseModel):
    type: str = Field(description="资源类型: video, book, paper, course")
    title: str = Field(description="资源标题")
    url: Optional[str] = Field(description="资源链接")
    description: str = Field(description="资源描述")

class GuidanceOutput(BaseModel):
    """学习指导输出结构"""
    personalized_advice: str = Field(description="个性化学习建议")
    study_tips: List[StudyTip] = Field(description="学习技巧列表")
    difficulty_adjustment: str = Field(description="难度调整建议")
    progress_feedback: str = Field(description="学习进度反馈")
    next_steps: List[str] = Field(description="下一步学习建议")
    recommended_resources: List[LearningResource] = Field(description="推荐学习资源")
    estimated_completion_time: int = Field(description="预计完成时间(天)")
    motivation_message: str = Field(description="激励性消息")

class GuidanceTeacher:
    """学习指导老师Agent - LLM驱动版本"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.model = self.config.get("model", "gpt-4o-2024-11-20")
        
    async def provide_guidance(self, 
                             user_profile: Dict[str, Any], 
                             learning_progress: Dict[str, Any],
                             paper_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """提供个性化学习指导"""
        try:
            self.logger.info(f"🎓 开始为用户提供学习指导")
            
            # 构建指导请求
            guidance_prompt = self._build_guidance_prompt(user_profile, learning_progress, paper_analysis)
            
            # 使用LLM生成指导建议
            agent = StructuredOutputAgent(
                api_key=OPENAI_API_KEY,
                model=self.model,
                output_model=GuidanceOutput,
                language=LANGUAGE
            )
            
            guidance_result = await agent.process(guidance_prompt)
            
            # 添加个性化调整
            adjusted_guidance = self._adjust_guidance_for_user(guidance_result, user_profile)
            
            self.logger.info("✅ 学习指导生成完成")
            return {
                "guidance": adjusted_guidance,
                "user_level": user_profile.get("level", "intermediate"),
                "total_papers": len(paper_analysis.get("papers", [])),
                "completion_rate": learning_progress.get("completion_rate", 0)
            }
            
        except Exception as e:
            self.logger.error(f"学习指导生成失败: {e}")
            return {"error": str(e)}
    
    def _build_guidance_prompt(self, 
                              user_profile: Dict[str, Any], 
                              learning_progress: Dict[str, Any],
                              paper_analysis: Dict[str, Any]) -> str:
        """构建指导提示"""
        
        user_level = user_profile.get("level", "intermediate")
        interests = user_profile.get("interests", [])
        daily_hours = user_profile.get("daily_hours", 2)
        language = user_profile.get("language", "Chinese")
        
        completed_papers = learning_progress.get("completed_papers", [])
        current_paper = learning_progress.get("current_paper", "")
        difficulties = learning_progress.get("difficulties", [])
        
        papers_summary = []
        for paper_id, analysis in paper_analysis.get("papers", {}).items():
            papers_summary.append({
                "id": paper_id,
                "title": analysis.get("title", ""),
                "difficulty": analysis.get("difficulty_level", "intermediate"),
                "concepts": analysis.get("core_concepts", [])[:5]  # 取前5个概念
            })
        
        prompt = f"""
作为一位经验丰富的学术导师，请为用户提供个性化的论文学习指导。

用户信息：
- 学习水平: {user_level}
- 兴趣领域: {', '.join(interests)}
- 每日学习时间: {daily_hours}小时
- 首选语言: {language}

学习进度：
- 已完成论文: {len(completed_papers)}篇
- 当前学习论文: {current_paper}
- 遇到的困难: {', '.join(difficulties)}

论文集合概览：
{json.dumps(papers_summary, ensure_ascii=False, indent=2)}

请提供：
1. 基于用户水平和进度的个性化学习建议
2. 针对当前困难的具体解决方案
3. 学习技巧和方法建议
4. 难度调整建议
5. 下一步学习计划
6. 推荐的补充学习资源
7. 预计完成时间
8. 激励性反馈

请确保建议具体可行，符合用户的时间安排和学习能力。
"""
        return prompt
    
    def _adjust_guidance_for_user(self, 
                                 guidance_result: Dict[str, Any], 
                                 user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """根据用户特征调整指导建议"""
        
        user_level = user_profile.get("level", "intermediate")
        daily_hours = user_profile.get("daily_hours", 2)
        
        # 根据用户水平调整建议
        if user_level == "beginner":
            # 为初学者提供更多基础资源和鼓励
            guidance_result["study_tips"].append({
                "category": "初学者建议",
                "tip": "建议先阅读综述性论文或教科书建立基础知识框架"
            })
            
        elif user_level == "advanced":
            # 为高级用户提供更具挑战性的建议
            guidance_result["study_tips"].append({
                "category": "高级学习",
                "tip": "可以尝试实现论文中的关键算法或进行批判性分析"
            })
        
        # 根据时间安排调整完成时间估算
        if daily_hours < 1:
            guidance_result["estimated_completion_time"] = int(guidance_result["estimated_completion_time"] * 1.5)
        elif daily_hours > 3:
            guidance_result["estimated_completion_time"] = int(guidance_result["estimated_completion_time"] * 0.7)
        
        return guidance_result
    
    async def provide_progress_feedback(self, 
                                      learning_progress: Dict[str, Any]) -> Dict[str, Any]:
        """提供学习进度反馈"""
        try:
            completion_rate = learning_progress.get("completion_rate", 0)
            time_spent = learning_progress.get("time_spent", 0)
            difficulties = learning_progress.get("difficulties", [])
            
            feedback = {
                "overall_progress": self._assess_progress(completion_rate),
                "time_efficiency": self._assess_time_efficiency(time_spent, completion_rate),
                "challenge_areas": difficulties,
                "recommendations": self._generate_progress_recommendations(completion_rate, difficulties)
            }
            
            return feedback
            
        except Exception as e:
            self.logger.error(f"进度反馈生成失败: {e}")
            return {"error": str(e)}
    
    def _assess_progress(self, completion_rate: float) -> str:
        """评估整体进度"""
        if completion_rate < 0.3:
            return "起步阶段，建议保持稳定的学习节奏"
        elif completion_rate < 0.7:
            return "进展良好，已经掌握了基础内容"
        else:
            return "优秀！即将完成学习计划"
    
    def _assess_time_efficiency(self, time_spent: int, completion_rate: float) -> str:
        """评估时间效率"""
        if completion_rate > 0 and time_spent > 0:
            efficiency = completion_rate / (time_spent / 60)  # 每小时完成率
            if efficiency > 0.1:
                return "学习效率很高"
            elif efficiency > 0.05:
                return "学习效率正常"
            else:
                return "建议优化学习方法提高效率"
        return "暂无法评估"
    
    def _generate_progress_recommendations(self, 
                                         completion_rate: float, 
                                         difficulties: List[str]) -> List[str]:
        """生成进度建议"""
        recommendations = []
        
        if completion_rate < 0.5:
            recommendations.append("建议制定更明确的日程安排")
            recommendations.append("可以尝试番茄工作法提高专注度")
        
        if difficulties:
            recommendations.append("针对困难点寻找额外的学习资源")
            recommendations.append("考虑加入学习小组或寻求导师指导")
        
        if completion_rate > 0.8:
            recommendations.append("准备总结和复习已学内容")
            recommendations.append("可以开始规划下一阶段的学习目标")
        
        return recommendations

if __name__ == "__main__":
    teacher = GuidanceTeacher()
    print("GuidanceTeacher 初始化完成")