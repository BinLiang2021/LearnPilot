"""
LearnPilot Web API
FastAPI-based web interface for LearnPilot
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
import logging
import asyncio
import os
import json
import tempfile
import shutil
from datetime import datetime

# Import LearnPilot components
try:
    # Try relative imports first
    from ..agents.paper_analysisor import PaperAnalysisor
    from ..agents.knowledge_extractor import KnowledgeExtractor
    from ..agents.knowledge_graph_agent import KnowledgeGraphAgent
    from ..agents.learning_planer import LearningPlaner
    from ..agents.guidance_teacher import GuidanceTeacher
    from ..agents.task_sheet_generator import TaskSheetGenerator
    from ..literature_utils.markdown_parser import parse_papers_from_directory
    from ..database import db_service, get_db, init_database
    from ..auth.auth import (
        auth_service, UserCreate, UserLogin, UserUpdate, 
        get_current_user, get_current_active_user
    )
    from .admin_api import router as admin_router
    from ..services.notification_service import notification_service
except ImportError:
    # Fallback to absolute imports
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    from src.learn_pilot.agents.paper_analysisor import PaperAnalysisor
    from src.learn_pilot.agents.knowledge_extractor import KnowledgeExtractor
    from src.learn_pilot.agents.knowledge_graph_agent import KnowledgeGraphAgent
    from src.learn_pilot.agents.learning_planer import LearningPlaner
    from src.learn_pilot.agents.guidance_teacher import GuidanceTeacher
    from src.learn_pilot.agents.task_sheet_generator import TaskSheetGenerator
    from src.learn_pilot.literature_utils.markdown_parser import parse_papers_from_directory
    from src.learn_pilot.database import db_service, get_db, init_database
    from src.learn_pilot.auth.auth import (
        auth_service, UserCreate, UserLogin, UserUpdate, 
        get_current_user, get_current_active_user
    )
    from src.learn_pilot.web.admin_api import router as admin_router
    from src.learn_pilot.services.notification_service import notification_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="LearnPilot API",
    description="AI-driven research paper learning assistant",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_database()

# Include admin router
app.include_router(admin_router)

# Serve static files
if os.path.exists("src/learn_pilot/web/static"):
    app.mount("/static", StaticFiles(directory="src/learn_pilot/web/static"), name="static")

# Data models
class UserProfile(BaseModel):
    name: str
    level: str = "intermediate"  # beginner, intermediate, advanced
    interests: List[str] = []
    daily_hours: float = 2.0
    language: str = "Chinese"

class PaperUpload(BaseModel):
    filename: str
    content: str
    file_type: str = "markdown"  # markdown, pdf

class AnalysisRequest(BaseModel):
    user_profile: UserProfile
    paper_files: List[str]  # File paths or IDs

class LearningPlanRequest(BaseModel):
    user_profile: UserProfile
    analysis_results: Dict[str, Any]

# Global state (in production, use database)
user_sessions = {}
analysis_results = {}
learning_plans = {}

# API Routes

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "LearnPilot API",
        "version": "1.0.0",
        "docs": "/docs",
        "frontend": "http://localhost:3000"
    }

@app.post("/api/analyze")
async def analyze_papers(request: Dict[str, Any], db: Session = Depends(get_db)):
    """Analyze uploaded papers"""
    try:
        logger.info("Starting paper analysis")
        
        user_profile = request.get("user_profile", {})
        papers_data = request.get("papers", [])
        
        # Create or get user
        username = user_profile.get("name", "anonymous").replace(" ", "_").lower()
        user = db_service.users.get_user_by_username(db, username)
        if not user:
            user = db_service.users.create_user(
                db=db,
                username=username,
                name=user_profile.get("name", "Anonymous User"),
                level=user_profile.get("level", "intermediate"),
                interests=user_profile.get("interests", []),
                daily_hours=user_profile.get("daily_hours", 2.0),
                language=user_profile.get("language", "Chinese")
            )
        
        # Create analysis session
        session = db_service.sessions.create_session(
            db=db,
            user_id=user.id,
            session_name=f"Analysis {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        )
        
        # Update session status to processing
        db_service.sessions.update_session_status(db, session.id, "processing")
        
        # Create temporary directory for papers
        temp_dir = tempfile.mkdtemp()
        saved_papers = []
        
        try:
            # Save papers to database and temporary files
            for paper_data in papers_data:
                filename = paper_data["filename"]
                content = paper_data["content"]
                
                # Save to database
                paper = db_service.papers.create_paper(
                    db=db,
                    title=filename,
                    content=content,
                    file_type=paper_data.get("file_type", "markdown")
                )
                saved_papers.append(paper)
                
                # Save to temporary file for processing
                file_path = os.path.join(temp_dir, filename)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            # Initialize agents
            paper_analysisor = PaperAnalysisor()
            knowledge_extractor = KnowledgeExtractor()
            knowledge_graph_agent = KnowledgeGraphAgent()
            
            # Analyze papers
            analysis_result = await paper_analysisor.analyze_papers(temp_dir)
            
            # Extract knowledge
            papers = parse_papers_from_directory(temp_dir)
            extraction_result = await knowledge_extractor.extract_concepts_from_papers(papers)
            
            # Save analysis results to database
            for i, paper in enumerate(saved_papers):
                # Find matching analysis result
                paper_analysis = None
                for paper_id, analysis in analysis_result.get("papers", {}).items():
                    if paper.title in paper_id or paper_id in paper.title:
                        paper_analysis = analysis
                        break
                
                if paper_analysis:
                    db_service.analyses.create_analysis(
                        db=db,
                        session_id=session.id,
                        paper_id=paper.id,
                        analysis_data=paper_analysis
                    )
                
                # Save extraction results
                paper_extraction = None
                for paper_id, extraction in extraction_result.get("concepts", {}).items():
                    if paper.title in paper_id or paper_id in paper.title:
                        paper_extraction = extraction
                        break
                
                if paper_extraction:
                    db_service.extractions.create_extraction(
                        db=db,
                        session_id=session.id,
                        paper_id=paper.id,
                        extraction_data=paper_extraction
                    )
            
            # Build knowledge graph
            papers_concepts = {}
            for paper in saved_papers:
                analysis = db_service.analyses.get_paper_analysis(db, session.id, paper.id)
                extraction = db_service.extractions.get_session_extractions(db, session.id)
                
                paper_concepts = []
                paper_prerequisites = []
                paper_difficulty = "intermediate"
                
                if analysis:
                    paper_concepts = analysis.core_concepts or []
                    paper_prerequisites = analysis.prerequisites or []
                    paper_difficulty = analysis.difficulty_level
                
                papers_concepts[paper.title] = {
                    "concepts": paper_concepts,
                    "prerequisites": paper_prerequisites,
                    "difficulty_level": paper_difficulty
                }
            
            dependency_graph = knowledge_graph_agent.build_dependency_graph(papers_concepts)
            reading_order = knowledge_graph_agent.get_reading_order()
            
            # Update session status to completed
            db_service.sessions.update_session_status(db, session.id, "completed")
            
            logger.info("Paper analysis completed successfully")
            return {
                "status": "success",
                "session_id": session.id,
                "user_id": user.id,
                "results": {
                    "total_papers": len(saved_papers),
                    "concepts_extracted": len(extraction_result.get("concepts", {})),
                    "reading_order": reading_order,
                    "graph_stats": {
                        "nodes": len(dependency_graph.nodes()),
                        "edges": len(dependency_graph.edges())
                    }
                }
            }
            
        finally:
            # Cleanup temporary directory
            shutil.rmtree(temp_dir, ignore_errors=True)
            
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        # Update session status to failed if session was created
        if 'session' in locals():
            db_service.sessions.update_session_status(db, session.id, "failed")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/api/learning-plan")
async def generate_learning_plan(request: Dict[str, Any], db: Session = Depends(get_db)):
    """Generate personalized learning plan"""
    try:
        logger.info("Generating learning plan")
        
        session_id = request.get("session_id")
        user_id = request.get("user_id")
        
        if not session_id or not user_id:
            raise HTTPException(status_code=400, detail="session_id and user_id required")
        
        # Get session data from database
        session_summary = db_service.get_session_summary(db, session_id)
        if not session_summary:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Get user profile
        user = db_service.users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_profile = user.to_dict()
        
        # Initialize learning planer
        learning_planer = LearningPlaner()
        
        # Prepare data for plan generation
        paper_analysis = {"papers": {}}
        knowledge_extraction = {"concepts": {}}
        
        for analysis in session_summary["analyses"]:
            paper_id = str(analysis["paper_id"])
            paper_analysis["papers"][paper_id] = analysis
        
        for extraction in session_summary["extractions"]:
            paper_id = str(extraction["paper_id"])
            knowledge_extraction["concepts"][paper_id] = extraction
        
        # Generate learning plan
        plan_result = await learning_planer.create_learning_plan(
            user_profile=user_profile,
            paper_analysis=paper_analysis,
            knowledge_extraction=knowledge_extraction,
            dependency_graph=session_summary.get("graph_data", {})
        )
        
        # Save learning plan to database
        saved_plan = db_service.plans.create_plan(
            db=db,
            user_id=user_id,
            session_id=session_id,
            plan_data=plan_result.get("learning_plan", {})
        )
        
        # Initialize progress tracking
        db_service.progress.create_progress(
            db=db,
            user_id=user_id,
            learning_plan_id=saved_plan.id
        )
        
        logger.info("Learning plan generated successfully")
        return {
            "status": "success",
            "learning_plan": plan_result,
            "plan_id": saved_plan.id,
            "session_id": session_id
        }
        
    except Exception as e:
        logger.error(f"Learning plan generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")

@app.post("/api/guidance")
async def get_guidance(user_profile: UserProfile, learning_progress: Dict[str, Any], paper_analysis: Dict[str, Any]):
    """Get personalized learning guidance"""
    try:
        logger.info("Providing learning guidance")
        
        guidance_teacher = GuidanceTeacher()
        
        guidance_result = await guidance_teacher.provide_guidance(
            user_profile=user_profile.dict(),
            learning_progress=learning_progress,
            paper_analysis=paper_analysis
        )
        
        logger.info("Learning guidance provided successfully")
        return guidance_result
        
    except Exception as e:
        logger.error(f"Guidance generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Guidance failed: {str(e)}")

@app.post("/api/tasks")
async def generate_tasks(paper_analysis: Dict[str, Any], knowledge_extraction: Dict[str, Any], user_profile: UserProfile):
    """Generate learning tasks and exercises"""
    try:
        logger.info("Generating learning tasks")
        
        task_generator = TaskSheetGenerator()
        
        task_result = await task_generator.generate_task_sheet(
            paper_analysis=paper_analysis,
            knowledge_extraction=knowledge_extraction,
            user_profile=user_profile.dict()
        )
        
        logger.info("Learning tasks generated successfully")
        return task_result
        
    except Exception as e:
        logger.error(f"Task generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Task generation failed: {str(e)}")

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Get analysis session data"""
    if session_id not in analysis_results:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_data": analysis_results[session_id],
        "learning_plan": learning_plans.get(session_id),
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

# Authentication endpoints
@app.post("/api/auth/register")
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (now requires approval)"""
    try:
        result = await auth_service.register_user(db, user_data)
        return result
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
async def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user"""
    try:
        result = auth_service.login_user(db, credentials)
        return {
            "status": "success",
            "message": "Login successful",
            **result
        }
    except Exception as e:
        logger.error(f"Login failed: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

@app.get("/api/auth/me")
async def get_current_user_info(current_user = Depends(get_current_active_user)):
    """Get current user information"""
    return {
        "status": "success",
        "user": current_user.to_dict()
    }

@app.put("/api/auth/profile")
async def update_user_profile(updates: UserUpdate, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update user profile"""
    try:
        result = auth_service.update_user_profile(db, current_user.id, updates)
        return {
            "status": "success",
            "message": "Profile updated successfully",
            **result
        }
    except Exception as e:
        logger.error(f"Profile update failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/sessions")
async def get_user_sessions(skip: int = 0, limit: int = 20, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get user's analysis sessions"""
    try:
        result = auth_service.get_user_sessions(db, current_user.id, skip, limit)
        return {
            "status": "success",
            **result
        }
    except Exception as e:
        logger.error(f"Failed to get sessions: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/learning-plans")
async def get_user_learning_plans(current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get user's learning plans"""
    try:
        result = auth_service.get_user_learning_plans(db, current_user.id)
        return {
            "status": "success",
            **result
        }
    except Exception as e:
        logger.error(f"Failed to get learning plans: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/progress")
async def get_user_progress(days: int = 7, current_user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get user's learning progress"""
    try:
        result = auth_service.get_user_progress(db, current_user.id, days)
        return {
            "status": "success",
            **result
        }
    except Exception as e:
        logger.error(f"Failed to get progress: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# User notification endpoints
@app.get("/api/user/notifications")
async def get_user_notifications(
    unread_only: bool = False,
    skip: int = 0,
    limit: int = 20,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    try:
        notifications = await notification_service.get_user_notifications(
            db, current_user.id, unread_only, skip, limit
        )
        unread_count = await notification_service.get_unread_notification_count(
            db, current_user.id
        )
        
        return {
            "status": "success",
            "notifications": [notif.to_dict() for notif in notifications],
            "unread_count": unread_count,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        logger.error(f"Failed to get notifications: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/user/notifications/{notification_id}/read")
async def mark_notification_read(
    notification_id: int,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a notification as read"""
    try:
        success = await notification_service.mark_notification_read(
            db, notification_id, current_user.id
        )
        
        if not success:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        return {
            "status": "success",
            "message": "Notification marked as read"
        }
    except Exception as e:
        logger.error(f"Failed to mark notification as read: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/user/notifications/unread-count")
async def get_unread_notification_count(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get count of unread notifications"""
    try:
        count = await notification_service.get_unread_notification_count(db, current_user.id)
        return {
            "status": "success",
            "unread_count": count
        }
    except Exception as e:
        logger.error(f"Failed to get unread count: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

# User status check endpoint
@app.get("/api/user/status")
async def get_user_status(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get current user status (including pending approval)"""
    return {
        "status": "success",
        "user": current_user.to_dict(),
        "account_status": current_user.status.value if current_user.status else "unknown",
        "is_approved": current_user.status.value == "approved" if current_user.status else False,
        "can_access_features": current_user.status.value == "approved" and current_user.is_active
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)