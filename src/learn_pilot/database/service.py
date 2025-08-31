"""
Database Service Layer
CRUD operations and business logic for database models
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, and_, or_
from typing import List, Optional, Dict, Any
import hashlib
import json
from datetime import datetime, timedelta

from .models import (
    User, Paper, AnalysisSession, PaperAnalysis, 
    ConceptExtraction, LearningPlan, LearningProgress, TaskSheet
)

class UserService:
    """User management service"""
    
    @staticmethod
    def create_user(db: Session, username: str, name: str, email: Optional[str] = None, 
                   level: str = "intermediate", interests: List[str] = None, 
                   daily_hours: float = 2.0, language: str = "Chinese") -> User:
        """Create a new user"""
        user = User(
            username=username,
            name=name,
            email=email,
            level=level,
            interests=interests or [],
            daily_hours=daily_hours,
            language=language
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username"""
        return db.query(User).filter(User.username == username, User.is_active == True).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.id == user_id, User.is_active == True).first()
    
    @staticmethod
    def update_user_profile(db: Session, user_id: int, updates: Dict[str, Any]) -> Optional[User]:
        """Update user profile"""
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            for key, value in updates.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            user.updated_at = datetime.now()
            db.commit()
            db.refresh(user)
        return user
    
    @staticmethod
    def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination"""
        return db.query(User).filter(User.is_active == True).offset(skip).limit(limit).all()

class PaperService:
    """Paper management service"""
    
    @staticmethod
    def create_paper(db: Session, title: str, content: str, authors: List[str] = None,
                    venue: str = None, year: str = None, abstract: str = None,
                    file_path: str = None, file_type: str = "markdown") -> Paper:
        """Create a new paper with duplicate detection"""
        
        # Calculate checksum for duplicate detection
        checksum = hashlib.md5(content.encode()).hexdigest()
        
        # Check for duplicates
        existing_paper = db.query(Paper).filter(Paper.checksum == checksum).first()
        if existing_paper:
            return existing_paper
        
        paper = Paper(
            title=title,
            authors=authors or [],
            venue=venue,
            year=year,
            abstract=abstract,
            content=content,
            file_path=file_path,
            file_type=file_type,
            checksum=checksum
        )
        db.add(paper)
        db.commit()
        db.refresh(paper)
        return paper
    
    @staticmethod
    def get_paper_by_id(db: Session, paper_id: int) -> Optional[Paper]:
        """Get paper by ID"""
        return db.query(Paper).filter(Paper.id == paper_id).first()
    
    @staticmethod
    def search_papers(db: Session, query: str, skip: int = 0, limit: int = 20) -> List[Paper]:
        """Search papers by title or content"""
        return db.query(Paper).filter(
            or_(
                Paper.title.contains(query),
                Paper.abstract.contains(query),
                Paper.content.contains(query)
            )
        ).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_papers_by_session(db: Session, session_id: int) -> List[Paper]:
        """Get papers associated with an analysis session"""
        return db.query(Paper).join(PaperAnalysis).filter(
            PaperAnalysis.session_id == session_id
        ).all()

class AnalysisSessionService:
    """Analysis session management service"""
    
    @staticmethod
    def create_session(db: Session, user_id: int, session_name: str = None,
                      description: str = None) -> AnalysisSession:
        """Create a new analysis session"""
        session = AnalysisSession(
            user_id=user_id,
            session_name=session_name or f"Session {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            description=description,
            status="pending"
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        return session
    
    @staticmethod
    def get_session_by_id(db: Session, session_id: int) -> Optional[AnalysisSession]:
        """Get session by ID"""
        return db.query(AnalysisSession).filter(AnalysisSession.id == session_id).first()
    
    @staticmethod
    def get_user_sessions(db: Session, user_id: int, skip: int = 0, limit: int = 20) -> List[AnalysisSession]:
        """Get user's analysis sessions"""
        return db.query(AnalysisSession).filter(
            AnalysisSession.user_id == user_id
        ).order_by(desc(AnalysisSession.created_at)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update_session_status(db: Session, session_id: int, status: str) -> Optional[AnalysisSession]:
        """Update session status"""
        session = db.query(AnalysisSession).filter(AnalysisSession.id == session_id).first()
        if session:
            session.status = status
            if status == "completed":
                session.completed_at = datetime.now()
            db.commit()
            db.refresh(session)
        return session

class PaperAnalysisService:
    """Paper analysis results service"""
    
    @staticmethod
    def create_analysis(db: Session, session_id: int, paper_id: int, 
                       analysis_data: Dict[str, Any]) -> PaperAnalysis:
        """Save paper analysis results"""
        analysis = PaperAnalysis(
            session_id=session_id,
            paper_id=paper_id,
            research_problem=analysis_data.get("research_problem"),
            main_method=analysis_data.get("main_method"),
            key_contributions=analysis_data.get("key_contributions", []),
            core_concepts=analysis_data.get("core_concepts", []),
            difficulty_level=analysis_data.get("difficulty_level", "intermediate"),
            reading_time_estimate=analysis_data.get("reading_time_estimate"),
            section_summary=analysis_data.get("section_summary", []),
            technical_complexity=analysis_data.get("technical_complexity"),
            prerequisites=analysis_data.get("prerequisites", [])
        )
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        return analysis
    
    @staticmethod
    def get_session_analyses(db: Session, session_id: int) -> List[PaperAnalysis]:
        """Get all analyses for a session"""
        return db.query(PaperAnalysis).filter(PaperAnalysis.session_id == session_id).all()
    
    @staticmethod
    def get_paper_analysis(db: Session, session_id: int, paper_id: int) -> Optional[PaperAnalysis]:
        """Get analysis for a specific paper in a session"""
        return db.query(PaperAnalysis).filter(
            PaperAnalysis.session_id == session_id,
            PaperAnalysis.paper_id == paper_id
        ).first()

class ConceptExtractionService:
    """Concept extraction service"""
    
    @staticmethod
    def create_extraction(db: Session, session_id: int, paper_id: int,
                         extraction_data: Dict[str, Any]) -> ConceptExtraction:
        """Save concept extraction results"""
        extraction = ConceptExtraction(
            session_id=session_id,
            paper_id=paper_id,
            core_concepts=extraction_data.get("core_concepts", []),
            supporting_concepts=extraction_data.get("supporting_concepts", []),
            prerequisites=extraction_data.get("prerequisites", []),
            concept_relationships=extraction_data.get("concept_relationships", []),
            knowledge_domains=extraction_data.get("knowledge_domains", []),
            difficulty_assessment=extraction_data.get("difficulty_assessment"),
            conceptual_complexity=extraction_data.get("conceptual_complexity"),
            estimated_learning_time=extraction_data.get("estimated_learning_time")
        )
        db.add(extraction)
        db.commit()
        db.refresh(extraction)
        return extraction
    
    @staticmethod
    def get_session_extractions(db: Session, session_id: int) -> List[ConceptExtraction]:
        """Get all extractions for a session"""
        return db.query(ConceptExtraction).filter(ConceptExtraction.session_id == session_id).all()

class LearningPlanService:
    """Learning plan service"""
    
    @staticmethod
    def create_plan(db: Session, user_id: int, session_id: int,
                   plan_data: Dict[str, Any]) -> LearningPlan:
        """Create a learning plan"""
        plan = LearningPlan(
            user_id=user_id,
            session_id=session_id,
            plan_name=plan_data.get("plan_name"),
            plan_overview=plan_data.get("plan_overview"),
            total_duration_days=plan_data.get("total_duration_days"),
            weekly_plans=plan_data.get("weekly_plans", []),
            learning_milestones=plan_data.get("learning_milestones", []),
            assessment_schedule=plan_data.get("assessment_schedule", []),
            resource_requirements=plan_data.get("resource_requirements", []),
            success_metrics=plan_data.get("success_metrics", []),
            contingency_plans=plan_data.get("contingency_plans", [])
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)
        return plan
    
    @staticmethod
    def get_user_plans(db: Session, user_id: int) -> List[LearningPlan]:
        """Get user's learning plans"""
        return db.query(LearningPlan).filter(
            LearningPlan.user_id == user_id,
            LearningPlan.status == "active"
        ).order_by(desc(LearningPlan.created_at)).all()
    
    @staticmethod
    def get_plan_by_session(db: Session, session_id: int) -> Optional[LearningPlan]:
        """Get learning plan by session ID"""
        return db.query(LearningPlan).filter(LearningPlan.session_id == session_id).first()
    
    @staticmethod
    def update_plan_status(db: Session, plan_id: int, status: str) -> Optional[LearningPlan]:
        """Update learning plan status"""
        plan = db.query(LearningPlan).filter(LearningPlan.id == plan_id).first()
        if plan:
            plan.status = status
            plan.updated_at = datetime.now()
            db.commit()
            db.refresh(plan)
        return plan

class LearningProgressService:
    """Learning progress tracking service"""
    
    @staticmethod
    def create_progress(db: Session, user_id: int, learning_plan_id: int) -> LearningProgress:
        """Initialize learning progress tracking"""
        progress = LearningProgress(
            user_id=user_id,
            learning_plan_id=learning_plan_id,
            completion_rate=0.0,
            time_spent=0,
            completed_papers=[],
            difficulties=[],
            achievements=[]
        )
        db.add(progress)
        db.commit()
        db.refresh(progress)
        return progress
    
    @staticmethod
    def update_progress(db: Session, progress_id: int, updates: Dict[str, Any]) -> Optional[LearningProgress]:
        """Update learning progress"""
        progress = db.query(LearningProgress).filter(LearningProgress.id == progress_id).first()
        if progress:
            for key, value in updates.items():
                if hasattr(progress, key):
                    setattr(progress, key, value)
            progress.updated_at = datetime.now()
            progress.last_activity = datetime.now()
            db.commit()
            db.refresh(progress)
        return progress
    
    @staticmethod
    def get_user_progress(db: Session, user_id: int, learning_plan_id: int) -> Optional[LearningProgress]:
        """Get progress for a specific learning plan"""
        return db.query(LearningProgress).filter(
            LearningProgress.user_id == user_id,
            LearningProgress.learning_plan_id == learning_plan_id
        ).first()
    
    @staticmethod
    def get_recent_activity(db: Session, user_id: int, days: int = 7) -> List[LearningProgress]:
        """Get recent learning activity"""
        since_date = datetime.now() - timedelta(days=days)
        return db.query(LearningProgress).filter(
            LearningProgress.user_id == user_id,
            LearningProgress.last_activity >= since_date
        ).order_by(desc(LearningProgress.last_activity)).all()

class TaskSheetService:
    """Task sheet service"""
    
    @staticmethod
    def create_task_sheet(db: Session, session_id: int, paper_id: int,
                         task_data: Dict[str, Any]) -> TaskSheet:
        """Create a task sheet"""
        task_sheet = TaskSheet(
            session_id=session_id,
            paper_id=paper_id,
            learning_objectives=task_data.get("learning_objectives", []),
            comprehension_questions=task_data.get("comprehension_questions", []),
            application_questions=task_data.get("application_questions", []),
            coding_tasks=task_data.get("coding_tasks", []),
            study_activities=task_data.get("study_activities", []),
            assessment_rubric=task_data.get("assessment_rubric", {}),
            additional_resources=task_data.get("additional_resources", [])
        )
        db.add(task_sheet)
        db.commit()
        db.refresh(task_sheet)
        return task_sheet
    
    @staticmethod
    def get_session_task_sheets(db: Session, session_id: int) -> List[TaskSheet]:
        """Get task sheets for a session"""
        return db.query(TaskSheet).filter(TaskSheet.session_id == session_id).all()
    
    @staticmethod
    def get_paper_task_sheet(db: Session, paper_id: int) -> Optional[TaskSheet]:
        """Get task sheet for a specific paper"""
        return db.query(TaskSheet).filter(TaskSheet.paper_id == paper_id).first()

# Consolidated service class
class DatabaseService:
    """Main database service class"""
    
    def __init__(self):
        self.users = UserService()
        self.papers = PaperService()
        self.sessions = AnalysisSessionService()
        self.analyses = PaperAnalysisService()
        self.extractions = ConceptExtractionService()
        self.plans = LearningPlanService()
        self.progress = LearningProgressService()
        self.tasks = TaskSheetService()
    
    def get_session_summary(self, db: Session, session_id: int) -> Dict[str, Any]:
        """Get comprehensive session summary"""
        session = self.sessions.get_session_by_id(db, session_id)
        if not session:
            return {}
        
        analyses = self.analyses.get_session_analyses(db, session_id)
        extractions = self.extractions.get_session_extractions(db, session_id)
        task_sheets = self.tasks.get_session_task_sheets(db, session_id)
        learning_plan = self.plans.get_plan_by_session(db, session_id)
        
        return {
            "session": session.to_dict(),
            "analyses": [a.to_dict() for a in analyses],
            "extractions": [e.to_dict() for e in extractions],
            "task_sheets": [t.to_dict() for t in task_sheets],
            "learning_plan": learning_plan.to_dict() if learning_plan else None,
            "summary": {
                "total_papers": len(analyses),
                "total_concepts": sum(len(e.core_concepts or []) for e in extractions),
                "avg_difficulty": self._calculate_avg_difficulty(analyses)
            }
        }
    
    def _calculate_avg_difficulty(self, analyses: List[PaperAnalysis]) -> str:
        """Calculate average difficulty level"""
        if not analyses:
            return "intermediate"
        
        difficulty_scores = {
            "beginner": 1,
            "intermediate": 2,
            "advanced": 3
        }
        
        total_score = sum(difficulty_scores.get(a.difficulty_level, 2) for a in analyses)
        avg_score = total_score / len(analyses)
        
        if avg_score <= 1.5:
            return "beginner"
        elif avg_score <= 2.5:
            return "intermediate"
        else:
            return "advanced"

# Global service instance
db_service = DatabaseService()