"""
Database Models for LearnPilot
SQLAlchemy models for persistent data storage
"""

from sqlalchemy import create_engine, Column, Integer, String, Text, Float, DateTime, Boolean, JSON, ForeignKey, UniqueConstraint, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime
import json
import enum

Base = declarative_base()

# Enum definitions for user status and approval
class UserStatus(enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

class AdminRole(enum.Enum):
    SUPER_ADMIN = "super_admin"
    MODERATOR = "moderator"
    REVIEWER = "reviewer"

class NotificationType(enum.Enum):
    EMAIL = "email"
    SYSTEM = "system"
    SMS = "sms"

class ApprovalAction(enum.Enum):
    APPROVE = "approve"
    REJECT = "reject"
    SUSPEND = "suspend"
    REACTIVATE = "reactivate"

class User(Base):
    """User model for storing user profiles with approval system"""
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    name = Column(String(200), nullable=False)
    password_hash = Column(String(500), nullable=True)  # For authenticated users
    level = Column(String(50), default='intermediate')  # beginner, intermediate, advanced
    interests = Column(JSON, default=list)  # List of interest areas
    daily_hours = Column(Float, default=2.0)
    language = Column(String(50), default='Chinese')
    
    # Approval system fields
    status = Column(Enum(UserStatus), default=UserStatus.PENDING, nullable=False, index=True)
    approved_at = Column(DateTime, nullable=True)
    approved_by = Column(Integer, ForeignKey('admins.id'), nullable=True)
    rejection_reason = Column(Text, nullable=True)
    registration_notes = Column(Text, nullable=True)  # Notes provided during registration
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    sessions = relationship("AnalysisSession", back_populates="user")
    learning_plans = relationship("LearningPlan", back_populates="user")
    progress_records = relationship("LearningProgress", back_populates="user")
    approver = relationship("Admin", foreign_keys=[approved_by], back_populates="approved_users")
    approval_records = relationship("UserApprovalRecord", back_populates="user")
    notifications = relationship("UserNotification", back_populates="user")
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'level': self.level,
            'interests': self.interests or [],
            'daily_hours': self.daily_hours,
            'language': self.language,
            'status': self.status.value if self.status else None,
            'approved_at': self.approved_at.isoformat() if self.approved_at else None,
            'approved_by': self.approved_by,
            'rejection_reason': self.rejection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }

class Admin(Base):
    """Admin model for managing system administration"""
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    password_hash = Column(String(500), nullable=False)
    role = Column(Enum(AdminRole), default=AdminRole.REVIEWER, nullable=False)
    
    # Admin permissions and settings
    is_active = Column(Boolean, default=True)
    can_approve_users = Column(Boolean, default=True)
    can_manage_admins = Column(Boolean, default=False)  # Only for super_admin
    can_view_logs = Column(Boolean, default=True)
    can_send_notifications = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    last_login = Column(DateTime, nullable=True)
    created_by = Column(Integer, ForeignKey('admins.id'), nullable=True)  # Self-reference
    
    # Relationships
    approved_users = relationship("User", foreign_keys="User.approved_by", back_populates="approver")
    approval_records = relationship("UserApprovalRecord", back_populates="admin")
    audit_logs = relationship("AuditLog", back_populates="admin")
    creator = relationship("Admin", remote_side=[id], back_populates="created_admins")
    created_admins = relationship("Admin", remote_side=[created_by], back_populates="creator")
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'name': self.name,
            'role': self.role.value if self.role else None,
            'is_active': self.is_active,
            'can_approve_users': self.can_approve_users,
            'can_manage_admins': self.can_manage_admins,
            'can_view_logs': self.can_view_logs,
            'can_send_notifications': self.can_send_notifications,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_by': self.created_by
        }

class UserApprovalRecord(Base):
    """Record of user approval/rejection actions"""
    __tablename__ = 'user_approval_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey('admins.id'), nullable=False, index=True)
    action = Column(Enum(ApprovalAction), nullable=False)
    
    # Action details
    reason = Column(Text, nullable=True)  # Reason for rejection or notes
    notes = Column(Text, nullable=True)  # Additional notes from admin
    previous_status = Column(String(50), nullable=True)
    new_status = Column(String(50), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="approval_records")
    admin = relationship("Admin", back_populates="approval_records")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'admin_id': self.admin_id,
            'action': self.action.value if self.action else None,
            'reason': self.reason,
            'notes': self.notes,
            'previous_status': self.previous_status,
            'new_status': self.new_status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserNotification(Base):
    """User notifications for approval status and system messages"""
    __tablename__ = 'user_notifications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    
    # Notification content
    title = Column(String(200), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(Enum(NotificationType), default=NotificationType.SYSTEM, nullable=False)
    
    # Status and tracking
    is_read = Column(Boolean, default=False)
    is_sent = Column(Boolean, default=False)  # For email notifications
    sent_at = Column(DateTime, nullable=True)
    read_at = Column(DateTime, nullable=True)
    
    # Metadata
    related_record_type = Column(String(50), nullable=True)  # 'approval', 'general', etc.
    related_record_id = Column(Integer, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="notifications")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type.value if self.notification_type else None,
            'is_read': self.is_read,
            'is_sent': self.is_sent,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'related_record_type': self.related_record_type,
            'related_record_id': self.related_record_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AuditLog(Base):
    """Audit log for tracking system actions and security events"""
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    admin_id = Column(Integer, ForeignKey('admins.id'), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)  # For user-related actions
    
    # Action details
    action = Column(String(100), nullable=False, index=True)  # 'user_approved', 'user_rejected', 'login_attempt', etc.
    resource_type = Column(String(50), nullable=True)  # 'user', 'admin', 'system'
    resource_id = Column(Integer, nullable=True)
    
    # Context and metadata
    ip_address = Column(String(45), nullable=True)  # IPv4 or IPv6
    user_agent = Column(String(500), nullable=True)
    details = Column(JSON, default=dict)  # Additional context data
    success = Column(Boolean, default=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    admin = relationship("Admin", back_populates="audit_logs")
    
    def to_dict(self):
        return {
            'id': self.id,
            'admin_id': self.admin_id,
            'user_id': self.user_id,
            'action': self.action,
            'resource_type': self.resource_type,
            'resource_id': self.resource_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'details': self.details or {},
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Paper(Base):
    """Paper model for storing paper information"""
    __tablename__ = 'papers'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)
    authors = Column(JSON, default=list)  # List of authors
    venue = Column(String(200))
    year = Column(String(10))
    abstract = Column(Text)
    content = Column(Text)  # Full paper content (markdown)
    file_path = Column(String(500))
    file_type = Column(String(50), default='markdown')  # markdown, pdf
    checksum = Column(String(64), index=True)  # MD5 hash for duplicate detection
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    analyses = relationship("PaperAnalysis", back_populates="paper")
    concepts = relationship("ConceptExtraction", back_populates="paper")
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'authors': self.authors or [],
            'venue': self.venue,
            'year': self.year,
            'abstract': self.abstract,
            'file_type': self.file_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AnalysisSession(Base):
    """Analysis session for grouping related papers and results"""
    __tablename__ = 'analysis_sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    session_name = Column(String(200))
    description = Column(Text)
    status = Column(String(50), default='pending')  # pending, processing, completed, failed
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime)
    
    # Relationships
    user = relationship("User", back_populates="sessions")
    paper_analyses = relationship("PaperAnalysis", back_populates="session")
    learning_plans = relationship("LearningPlan", back_populates="session")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_name': self.session_name,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

class PaperAnalysis(Base):
    """Paper analysis results"""
    __tablename__ = 'paper_analyses'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('analysis_sessions.id'), nullable=False, index=True)
    paper_id = Column(Integer, ForeignKey('papers.id'), nullable=False, index=True)
    
    # Analysis results (JSON fields)
    research_problem = Column(Text)
    main_method = Column(Text)
    key_contributions = Column(JSON, default=list)
    core_concepts = Column(JSON, default=list)
    difficulty_level = Column(String(50), default='intermediate')
    reading_time_estimate = Column(Integer)  # minutes
    section_summary = Column(JSON, default=list)
    technical_complexity = Column(String(50))
    prerequisites = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    session = relationship("AnalysisSession", back_populates="paper_analyses")
    paper = relationship("Paper", back_populates="analyses")
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'paper_id': self.paper_id,
            'research_problem': self.research_problem,
            'main_method': self.main_method,
            'key_contributions': self.key_contributions or [],
            'core_concepts': self.core_concepts or [],
            'difficulty_level': self.difficulty_level,
            'reading_time_estimate': self.reading_time_estimate,
            'section_summary': self.section_summary or [],
            'technical_complexity': self.technical_complexity,
            'prerequisites': self.prerequisites or [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ConceptExtraction(Base):
    """Concept extraction results"""
    __tablename__ = 'concept_extractions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('analysis_sessions.id'), nullable=False, index=True)
    paper_id = Column(Integer, ForeignKey('papers.id'), nullable=False, index=True)
    
    # Extracted concepts
    core_concepts = Column(JSON, default=list)
    supporting_concepts = Column(JSON, default=list)
    prerequisites = Column(JSON, default=list)
    concept_relationships = Column(JSON, default=list)
    knowledge_domains = Column(JSON, default=list)
    
    difficulty_assessment = Column(String(50))
    conceptual_complexity = Column(String(50))
    estimated_learning_time = Column(Integer)  # minutes
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    paper = relationship("Paper", back_populates="concepts")
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'paper_id': self.paper_id,
            'core_concepts': self.core_concepts or [],
            'supporting_concepts': self.supporting_concepts or [],
            'prerequisites': self.prerequisites or [],
            'concept_relationships': self.concept_relationships or [],
            'knowledge_domains': self.knowledge_domains or [],
            'difficulty_assessment': self.difficulty_assessment,
            'conceptual_complexity': self.conceptual_complexity,
            'estimated_learning_time': self.estimated_learning_time,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class LearningPlan(Base):
    """Learning plan storage"""
    __tablename__ = 'learning_plans'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    session_id = Column(Integer, ForeignKey('analysis_sessions.id'), nullable=False, index=True)
    
    plan_name = Column(String(200))
    plan_overview = Column(Text)
    total_duration_days = Column(Integer)
    weekly_plans = Column(JSON, default=list)
    learning_milestones = Column(JSON, default=list)
    assessment_schedule = Column(JSON, default=list)
    resource_requirements = Column(JSON, default=list)
    success_metrics = Column(JSON, default=list)
    contingency_plans = Column(JSON, default=list)
    
    status = Column(String(50), default='active')  # active, paused, completed, archived
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="learning_plans")
    session = relationship("AnalysisSession", back_populates="learning_plans")
    progress_records = relationship("LearningProgress", back_populates="learning_plan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'plan_name': self.plan_name,
            'plan_overview': self.plan_overview,
            'total_duration_days': self.total_duration_days,
            'weekly_plans': self.weekly_plans or [],
            'learning_milestones': self.learning_milestones or [],
            'assessment_schedule': self.assessment_schedule or [],
            'resource_requirements': self.resource_requirements or [],
            'success_metrics': self.success_metrics or [],
            'contingency_plans': self.contingency_plans or [],
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class LearningProgress(Base):
    """Learning progress tracking"""
    __tablename__ = 'learning_progress'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    learning_plan_id = Column(Integer, ForeignKey('learning_plans.id'), nullable=False, index=True)
    
    # Progress data
    completion_rate = Column(Float, default=0.0)  # 0.0 to 1.0
    time_spent = Column(Integer, default=0)  # minutes
    completed_papers = Column(JSON, default=list)
    current_paper = Column(String(200))
    difficulties = Column(JSON, default=list)
    achievements = Column(JSON, default=list)
    notes = Column(Text)
    
    # Session tracking
    last_activity = Column(DateTime, default=func.now())
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    learning_plan = relationship("LearningPlan", back_populates="progress_records")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'learning_plan_id': self.learning_plan_id,
            'completion_rate': self.completion_rate,
            'time_spent': self.time_spent,
            'completed_papers': self.completed_papers or [],
            'current_paper': self.current_paper,
            'difficulties': self.difficulties or [],
            'achievements': self.achievements or [],
            'notes': self.notes,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class TaskSheet(Base):
    """Generated task sheets and exercises"""
    __tablename__ = 'task_sheets'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('analysis_sessions.id'), nullable=False, index=True)
    paper_id = Column(Integer, ForeignKey('papers.id'), nullable=False, index=True)
    
    # Task content
    learning_objectives = Column(JSON, default=list)
    comprehension_questions = Column(JSON, default=list)
    application_questions = Column(JSON, default=list)
    coding_tasks = Column(JSON, default=list)
    study_activities = Column(JSON, default=list)
    assessment_rubric = Column(JSON, default=dict)
    additional_resources = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'paper_id': self.paper_id,
            'learning_objectives': self.learning_objectives or [],
            'comprehension_questions': self.comprehension_questions or [],
            'application_questions': self.application_questions or [],
            'coding_tasks': self.coding_tasks or [],
            'study_activities': self.study_activities or [],
            'assessment_rubric': self.assessment_rubric or {},
            'additional_resources': self.additional_resources or [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Database session management
class DatabaseManager:
    """Database management utilities"""
    
    def __init__(self, database_url: str = "sqlite:///learnpilot.db"):
        self.database_url = database_url
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)
        
    def create_tables(self):
        """Create all database tables"""
        Base.metadata.create_all(bind=self.engine)
        
    def get_session(self):
        """Get database session"""
        return self.SessionLocal()
    
    def close_session(self, db_session):
        """Close database session"""
        db_session.close()

# Global database manager instance
db_manager = DatabaseManager()

# Dependency for FastAPI
def get_db():
    """FastAPI dependency for database session"""
    db = db_manager.get_session()
    try:
        yield db
    finally:
        db.close()