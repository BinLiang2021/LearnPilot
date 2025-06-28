"""
论文相关数据模型
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from datetime import datetime

@dataclass
class Section:
    """论文章节"""
    title: str
    content: str
    level: int  # 章节层级
    concepts: List[str] = None
    keywords: List[str] = None
    
    def __post_init__(self):
        if self.concepts is None:
            self.concepts = []
        if self.keywords is None:
            self.keywords = []

@dataclass
class Author:
    """作者信息"""
    name: str
    affiliation: Optional[str] = None
    email: Optional[str] = None

@dataclass
class Paper:
    """论文数据模型"""
    title: str
    authors: List[Author]
    abstract: str
    sections: List[Section]
    metadata: Dict[str, Any]
    
    # 可选字段
    year: Optional[int] = None
    venue: Optional[str] = None
    arxiv_id: Optional[str] = None
    doi: Optional[str] = None
    keywords: List[str] = None
    created_at: datetime = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def get_all_concepts(self) -> List[str]:
        """获取论文中的所有概念"""
        concepts = []
        for section in self.sections:
            concepts.extend(section.concepts)
        return list(set(concepts))  # 去重
    
    def get_section_by_title(self, title: str) -> Optional[Section]:
        """根据标题获取章节"""
        for section in self.sections:
            if section.title.lower() == title.lower():
                return section
        return None

@dataclass
class ConceptExtraction:
    """概念提取结果"""
    paper_id: str
    concepts: List[str]
    prerequisites: List[Dict[str, str]]  # [{"name": "concept", "level": "basic|intermediate|advanced"}]
    difficulty_level: str  # "beginner", "intermediate", "advanced"
    estimated_reading_time: int  # 分钟
    
@dataclass
class PaperRelationship:
    """论文关系"""
    source_paper: str
    target_paper: str
    relationship_type: str  # "prerequisite", "extends", "applies", "compares"
    strength: float  # 0.0 - 1.0
    description: str = ""
