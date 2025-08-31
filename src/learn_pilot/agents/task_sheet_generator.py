"""
Task Sheet Generator Agent
任务表生成Agent，使用LLM生成学习任务和练习题
"""

import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
import json

from src.learn_pilot.core.agents.structured_output_agent import StructuredOutputAgent
from src.learn_pilot.core.config.config import OPENAI_API_KEY, LANGUAGE

logger = logging.getLogger(__name__)

class Question(BaseModel):
    question_type: str = Field(description="题目类型: multiple_choice, short_answer, essay, coding")
    question: str = Field(description="问题内容")
    options: Optional[List[str]] = Field(description="选择题选项(仅适用于选择题)")
    correct_answer: Optional[str] = Field(description="正确答案")
    explanation: str = Field(description="答案解释")
    difficulty: str = Field(description="难度级别: easy, medium, hard")
    concepts_tested: List[str] = Field(description="测试的概念")

class CodingTask(BaseModel):
    task_title: str = Field(description="编程任务标题")
    description: str = Field(description="任务描述")
    requirements: List[str] = Field(description="具体要求")
    starter_code: Optional[str] = Field(description="起始代码模板")
    test_cases: List[str] = Field(description="测试用例")
    hints: List[str] = Field(description="提示信息")
    difficulty: str = Field(description="难度级别: easy, medium, hard")
    estimated_time: int = Field(description="预计完成时间(分钟)")

class StudyActivity(BaseModel):
    activity_type: str = Field(description="活动类型: reading, discussion, visualization, experiment")
    title: str = Field(description="活动标题")
    description: str = Field(description="活动描述")
    instructions: List[str] = Field(description="活动步骤")
    resources_needed: List[str] = Field(description="所需资源")
    learning_objectives: List[str] = Field(description="学习目标")
    estimated_time: int = Field(description="预计时间(分钟)")

class TaskSheetOutput(BaseModel):
    """任务表输出结构"""
    paper_title: str = Field(description="论文标题")
    learning_objectives: List[str] = Field(description="学习目标")
    comprehension_questions: List[Question] = Field(description="理解题目")
    application_questions: List[Question] = Field(description="应用题目")
    coding_tasks: List[CodingTask] = Field(description="编程任务")
    study_activities: List[StudyActivity] = Field(description="学习活动")
    assessment_rubric: Dict[str, str] = Field(description="评估标准")
    additional_resources: List[str] = Field(description="补充资源")

class TaskSheetGenerator:
    """任务表生成器Agent - LLM驱动版本"""
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logger
        self.model = self.config.get("model", "gpt-4o-2024-11-20")
        
    async def generate_task_sheet(self, 
                                paper_analysis: Dict[str, Any],
                                knowledge_extraction: Dict[str, Any],
                                user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """生成学习任务表"""
        try:
            self.logger.info(f"📝 开始生成学习任务表")
            
            # 构建任务生成提示
            task_prompt = self._build_task_prompt(paper_analysis, knowledge_extraction, user_profile)
            
            # 使用LLM生成任务表
            agent = StructuredOutputAgent(
                api_key=OPENAI_API_KEY,
                model=self.model,
                output_model=TaskSheetOutput,
                language=LANGUAGE
            )
            
            task_result = await agent.process(task_prompt)
            
            # 根据用户水平调整任务难度
            adjusted_tasks = self._adjust_tasks_for_user(task_result, user_profile)
            
            self.logger.info("✅ 学习任务表生成完成")
            return {
                "task_sheet": adjusted_tasks,
                "user_level": user_profile.get("level", "intermediate"),
                "paper_title": paper_analysis.get("title", ""),
                "total_tasks": self._count_total_tasks(adjusted_tasks)
            }
            
        except Exception as e:
            self.logger.error(f"任务表生成失败: {e}")
            return {"error": str(e)}
    
    def _build_task_prompt(self, 
                          paper_analysis: Dict[str, Any],
                          knowledge_extraction: Dict[str, Any],
                          user_profile: Dict[str, Any]) -> str:
        """构建任务生成提示"""
        
        paper_title = paper_analysis.get("title", "")
        research_problem = paper_analysis.get("research_problem", "")
        main_method = paper_analysis.get("main_method", "")
        key_contributions = paper_analysis.get("key_contributions", [])
        core_concepts = paper_analysis.get("core_concepts", [])
        difficulty_level = paper_analysis.get("difficulty_level", "intermediate")
        
        extracted_concepts = knowledge_extraction.get("core_concepts", [])
        prerequisites = knowledge_extraction.get("prerequisites", [])
        
        user_level = user_profile.get("level", "intermediate")
        interests = user_profile.get("interests", [])
        daily_hours = user_profile.get("daily_hours", 2)
        
        prompt = f"""
作为一位经验丰富的教育专家，请为以下论文设计综合性的学习任务表。

论文信息：
- 标题: {paper_title}
- 研究问题: {research_problem}
- 主要方法: {main_method}
- 关键贡献: {key_contributions}
- 核心概念: {core_concepts}
- 难度级别: {difficulty_level}

知识分析结果：
- 提取的概念: {extracted_concepts}
- 前置知识: {prerequisites}

用户特征：
- 学习水平: {user_level}
- 兴趣领域: {interests}
- 每日学习时间: {daily_hours}小时

请设计包含以下内容的学习任务表：

1. 明确的学习目标
2. 理解性问题（测试对论文内容的理解）
3. 应用性问题（测试概念应用能力）
4. 编程任务（如适用，基于论文的算法或实现）
5. 学习活动（讨论、可视化、实验等）
6. 评估标准
7. 补充学习资源

要求：
- 题目难度应符合用户水平
- 包含不同类型的问题（选择题、简答题、论述题、编程题）
- 提供详细的答案解释和评分标准
- 编程任务应提供起始代码模板和测试用例
- 学习活动应具有互动性和实践性

请使用{LANGUAGE}回答。
"""
        return prompt
    
    def _adjust_tasks_for_user(self, 
                              task_result: Dict[str, Any], 
                              user_profile: Dict[str, Any]) -> Dict[str, Any]:
        """根据用户特征调整任务"""
        
        user_level = user_profile.get("level", "intermediate")
        interests = user_profile.get("interests", [])
        
        # 根据用户水平调整任务数量和难度
        if user_level == "beginner":
            # 为初学者减少高难度任务，增加基础练习
            task_result["comprehension_questions"] = [
                q for q in task_result["comprehension_questions"] 
                if q.get("difficulty", "medium") != "hard"
            ]
            
            # 添加基础概念复习活动
            basic_activity = {
                "activity_type": "reading",
                "title": "基础概念复习",
                "description": "复习相关的基础概念和术语",
                "instructions": [
                    "查阅相关术语的定义",
                    "阅读基础教材的相关章节",
                    "制作概念卡片进行记忆"
                ],
                "resources_needed": ["基础教材", "在线词典"],
                "learning_objectives": ["掌握基础概念和术语"],
                "estimated_time": 30
            }
            task_result["study_activities"].insert(0, basic_activity)
            
        elif user_level == "advanced":
            # 为高级用户增加挑战性任务
            advanced_activity = {
                "activity_type": "experiment",
                "title": "创新性探索",
                "description": "基于论文内容进行创新性研究或改进",
                "instructions": [
                    "识别论文的局限性",
                    "提出改进方案",
                    "设计验证实验",
                    "分析结果并得出结论"
                ],
                "resources_needed": ["开发环境", "数据集", "计算资源"],
                "learning_objectives": ["培养批判性思维和创新能力"],
                "estimated_time": 120
            }
            task_result["study_activities"].append(advanced_activity)
        
        # 根据兴趣调整编程任务
        if any(interest in ["机器学习", "人工智能", "深度学习"] for interest in interests):
            # 为AI相关兴趣添加更多编程任务
            if len(task_result["coding_tasks"]) < 2:
                ai_task = {
                    "task_title": "算法实现与实验",
                    "description": "实现论文中的关键算法并进行实验验证",
                    "requirements": [
                        "使用Python实现核心算法",
                        "在标准数据集上测试性能",
                        "分析实验结果"
                    ],
                    "starter_code": "# TODO: 实现核心算法\nclass Algorithm:\n    def __init__(self):\n        pass\n    \n    def fit(self, X, y):\n        # TODO: 训练算法\n        pass\n    \n    def predict(self, X):\n        # TODO: 预测\n        pass",
                    "test_cases": ["使用iris数据集测试", "使用mnist数据集测试"],
                    "hints": ["参考论文中的伪代码", "注意算法的时间复杂度"],
                    "difficulty": "medium",
                    "estimated_time": 90
                }
                task_result["coding_tasks"].append(ai_task)
        
        return task_result
    
    def _count_total_tasks(self, task_sheet: Dict[str, Any]) -> Dict[str, int]:
        """统计任务总数"""
        return {
            "comprehension_questions": len(task_sheet.get("comprehension_questions", [])),
            "application_questions": len(task_sheet.get("application_questions", [])),
            "coding_tasks": len(task_sheet.get("coding_tasks", [])),
            "study_activities": len(task_sheet.get("study_activities", []))
        }
    
    async def generate_quiz(self, 
                           paper_analysis: Dict[str, Any],
                           difficulty: str = "medium",
                           num_questions: int = 10) -> Dict[str, Any]:
        """生成快速测验"""
        try:
            self.logger.info(f"🎯 生成 {difficulty} 难度的测验，共 {num_questions} 题")
            
            quiz_prompt = f"""
基于以下论文信息，生成 {num_questions} 道 {difficulty} 难度的测验题：

论文标题: {paper_analysis.get('title', '')}
核心概念: {paper_analysis.get('core_concepts', [])}
主要方法: {paper_analysis.get('main_method', '')}

要求：
- 包含选择题、简答题等多种题型
- 每题提供正确答案和详细解释
- 难度保持在 {difficulty} 级别
- 题目应测试对核心概念的理解

请使用{LANGUAGE}回答。
"""
            
            # 简化的问题模型
            class QuizQuestion(BaseModel):
                question: str
                type: str
                options: Optional[List[str]] = None
                correct_answer: str
                explanation: str
            
            class QuizOutput(BaseModel):
                questions: List[QuizQuestion]
                total_score: int = Field(default=100)
                passing_score: int = Field(default=70)
            
            agent = StructuredOutputAgent(
                api_key=OPENAI_API_KEY,
                model=self.model,
                output_model=QuizOutput,
                language=LANGUAGE
            )
            
            quiz_result = await agent.process(quiz_prompt)
            
            self.logger.info("✅ 测验生成完成")
            return {
                "quiz": quiz_result,
                "paper_title": paper_analysis.get("title", ""),
                "difficulty": difficulty,
                "question_count": len(quiz_result.get("questions", []))
            }
            
        except Exception as e:
            self.logger.error(f"测验生成失败: {e}")
            return {"error": str(e)}
    
    def generate_practice_schedule(self, 
                                 task_sheet: Dict[str, Any],
                                 user_daily_hours: float = 2) -> Dict[str, Any]:
        """生成练习时间安排"""
        try:
            tasks = task_sheet.get("task_sheet", {})
            
            # 计算各类任务的总时间
            comprehension_time = len(tasks.get("comprehension_questions", [])) * 5  # 每题5分钟
            application_time = len(tasks.get("application_questions", [])) * 10   # 每题10分钟
            coding_time = sum(task.get("estimated_time", 60) for task in tasks.get("coding_tasks", []))
            activity_time = sum(activity.get("estimated_time", 30) for activity in tasks.get("study_activities", []))
            
            total_minutes = comprehension_time + application_time + coding_time + activity_time
            total_hours = total_minutes / 60
            
            # 计算需要的天数
            days_needed = max(1, int(total_hours / user_daily_hours))
            
            # 分配每日任务
            daily_schedule = []
            daily_minutes = user_daily_hours * 60
            
            for day in range(days_needed):
                day_tasks = []
                remaining_minutes = daily_minutes
                
                # 优先分配理解题
                if tasks.get("comprehension_questions"):
                    questions_per_day = min(3, len(tasks["comprehension_questions"]))
                    day_tasks.append({
                        "type": "comprehension",
                        "count": questions_per_day,
                        "estimated_time": questions_per_day * 5
                    })
                    remaining_minutes -= questions_per_day * 5
                
                # 分配应用题
                if remaining_minutes > 20 and tasks.get("application_questions"):
                    questions_per_day = min(2, len(tasks["application_questions"]))
                    day_tasks.append({
                        "type": "application", 
                        "count": questions_per_day,
                        "estimated_time": questions_per_day * 10
                    })
                    remaining_minutes -= questions_per_day * 10
                
                # 分配编程任务（如果时间充足）
                if remaining_minutes > 30 and tasks.get("coding_tasks"):
                    day_tasks.append({
                        "type": "coding",
                        "count": 1,
                        "estimated_time": min(remaining_minutes, 60)
                    })
                
                daily_schedule.append({
                    "day": day + 1,
                    "tasks": day_tasks,
                    "total_time": daily_minutes - remaining_minutes
                })
            
            return {
                "schedule": daily_schedule,
                "total_days": days_needed,
                "total_hours": round(total_hours, 1),
                "daily_hours": user_daily_hours,
                "completion_estimate": f"{days_needed} 天"
            }
            
        except Exception as e:
            self.logger.error(f"练习安排生成失败: {e}")
            return {"error": str(e)}

if __name__ == "__main__":
    generator = TaskSheetGenerator()
    print("TaskSheetGenerator 初始化完成")