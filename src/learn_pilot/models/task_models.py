"""
任务相关数据模型
用于定义学习任务、练习题、代码骨架等数据结构
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class TaskType(Enum):
    """任务类型枚举"""
    COMPREHENSION = "comprehension"  # 理解检查题
    CODING = "coding"               # 编程实验
    THINKING = "thinking"           # 拓展思考题
    FILL_BLANK = "fill_blank"       # 填空题
    REVIEW = "review"               # 复习任务

class DifficultyLevel(Enum):
    """难度级别枚举"""
    BEGINNER = "★☆☆"
    INTERMEDIATE = "★★☆" 
    ADVANCED = "★★★"

@dataclass
class Task:
    """基础任务数据模型"""
    id: str
    title: str
    task_type: TaskType
    difficulty: DifficultyLevel
    estimated_time: int  # 估计完成时间（分钟）
    description: str
    evaluation_criteria: List[str]
    
    # 可选字段
    prerequisites: List[str] = field(default_factory=list)
    learning_objectives: List[str] = field(default_factory=list)
    hints: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

@dataclass
class ComprehensionTask(Task):
    """理解检查任务"""
    questions: List[Dict[str, Any]]  # [{"question": str, "type": "multiple_choice|short_answer", "options": [...], "answer": str}]
    
    def __post_init__(self):
        self.task_type = TaskType.COMPREHENSION

@dataclass
class CodingTask(Task):
    """编程实验任务"""
    objective: str
    data_requirements: List[str]
    implementation_steps: List[str]
    expected_output: str
    starter_code: Optional[str] = None
    test_cases: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        self.task_type = TaskType.CODING

@dataclass
class ThinkingTask(Task):
    """拓展思考任务"""
    prompts: List[str]  # 思考提示
    discussion_points: List[str]
    
    def __post_init__(self):
        self.task_type = TaskType.THINKING

@dataclass
class FillBlankTask(Task):
    """填空任务"""
    code_template: str
    blanks: List[Dict[str, Any]]  # [{"position": int, "hint": str, "answer": str, "type": "expression|statement|variable"}]
    
    def __post_init__(self):
        self.task_type = TaskType.FILL_BLANK

@dataclass
class TaskSheet:
    """任务表 - 包含一篇论文的所有相关任务"""
    paper_id: str
    paper_title: str
    tasks: List[Task]
    
    # 元信息
    total_estimated_time: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        # 自动计算总预估时间
        self.total_estimated_time = sum(task.estimated_time for task in self.tasks)
    
    def get_tasks_by_type(self, task_type: TaskType) -> List[Task]:
        """根据类型获取任务"""
        return [task for task in self.tasks if task.task_type == task_type]
    
    def get_tasks_by_difficulty(self, difficulty: DifficultyLevel) -> List[Task]:
        """根据难度获取任务"""
        return [task for task in self.tasks if task.difficulty == difficulty]

@dataclass
class CodeSkeleton:
    """代码骨架"""
    task_id: str
    language: str  # "python", "javascript", etc.
    template_code: str
    todos: List[Dict[str, Any]]  # [{"line": int, "description": str, "hint": str, "difficulty": str}]
    imports: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    
    def get_skeleton_with_todos(self) -> str:
        """获取带TODO标记的代码骨架"""
        lines = self.template_code.split('\n')
        result = []
        
        for i, line in enumerate(lines, 1):
            result.append(line)
            # 检查是否有TODO需要插入到这一行后面
            for todo in self.todos:
                if todo.get("line") == i:
                    result.append(f"    # TODO: {todo['description']}")
                    if todo.get("hint"):
                        result.append(f"    # Hint: {todo['hint']}")
        
        return '\n'.join(result)

@dataclass
class LearningPlan:
    """学习计划"""
    plan_id: str
    user_id: str
    papers: List[str]  # paper_ids in recommended order
    schedule: List[Dict[str, Any]]  # [{"day": int, "paper": str, "tasks": [...], "estimated_hours": float}]
    
    # 配置参数
    total_duration_days: int
    daily_time_budget: int  # 分钟
    user_level: str  # "beginner", "intermediate", "advanced"
    
    # 元信息
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def get_daily_schedule(self, day: int) -> Optional[Dict[str, Any]]:
        """获取指定日期的学习安排"""
        for item in self.schedule:
            if item.get("day") == day:
                return item
        return None
    
    def get_total_estimated_hours(self) -> float:
        """获取总预估学习时长"""
        return sum(item.get("estimated_hours", 0) for item in self.schedule)
