"""
Admin API Routes
FastAPI routes for admin operations, user approval, and system management
"""

from fastapi import APIRouter, HTTPException, Depends, Request, Query, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime, timedelta

# Import dependencies
try:
    # Try relative imports first
    from ..database import get_db
    from ..database.models import (
        Admin, User, UserApprovalRecord, UserNotification, AuditLog,
        UserStatus, AdminRole, ApprovalAction
    )
    from ..auth.admin_auth import (
        AdminService, AdminCreate, AdminLogin, AdminUpdate, UserApprovalRequest,
        get_current_admin, get_current_active_admin, require_super_admin,
        require_user_approval_permission, require_admin_management_permission,
        admin_service
    )
except ImportError:
    # Fallback to absolute imports
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
    from src.learn_pilot.database import get_db
    from src.learn_pilot.database.models import (
        Admin, User, UserApprovalRecord, UserNotification, AuditLog,
        UserStatus, AdminRole, ApprovalAction
    )
    from src.learn_pilot.auth.admin_auth import (
        AdminService, AdminCreate, AdminLogin, AdminUpdate, UserApprovalRequest,
        get_current_admin, get_current_active_admin, require_super_admin,
        require_user_approval_permission, require_admin_management_permission,
        admin_service
    )

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/admin", tags=["admin"])

# Security
security = HTTPBearer()

# ==================== ADMIN AUTHENTICATION ====================

@router.post("/login")
async def admin_login(
    credentials: AdminLogin,
    request: Request,
    db: Session = Depends(get_db)
):
    """Admin login endpoint"""
    try:
        result = admin_service.login_admin(db, credentials, request)
        return {
            "status": "success",
            "message": "Admin login successful",
            **result
        }
    except Exception as e:
        logger.error(f"Admin login failed: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me")
async def get_current_admin_info(current_admin: Admin = Depends(get_current_active_admin)):
    """Get current admin information"""
    return {
        "status": "success",
        "admin": current_admin.to_dict()
    }

@router.post("/logout")
async def admin_logout(current_admin: Admin = Depends(get_current_active_admin)):
    """Admin logout (client-side token removal)"""
    return {
        "status": "success",
        "message": "Logged out successfully"
    }

# ==================== ADMIN MANAGEMENT ====================

@router.post("/create")
async def create_admin(
    admin_data: AdminCreate,
    current_admin: Admin = Depends(require_admin_management_permission),
    db: Session = Depends(get_db)
):
    """Create a new admin (requires admin management permission)"""
    try:
        # Only super admins can create other super admins
        if admin_data.role == AdminRole.SUPER_ADMIN and current_admin.role != AdminRole.SUPER_ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Only super admins can create other super admins"
            )
        
        new_admin = admin_service.create_admin(db, admin_data, current_admin.id)
        
        # Log the action
        admin_service.log_audit_event(
            db=db,
            action="admin_created",
            admin_id=current_admin.id,
            resource_type="admin",
            resource_id=new_admin.id,
            details={
                "new_admin_username": new_admin.username,
                "new_admin_role": new_admin.role.value
            },
            success=True
        )
        
        return {
            "status": "success",
            "message": "Admin created successfully",
            "admin": new_admin.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Admin creation failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/list")
async def list_admins(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_admin: Admin = Depends(require_admin_management_permission),
    db: Session = Depends(get_db)
):
    """List all admins (requires admin management permission)"""
    admins = db.query(Admin).offset(skip).limit(limit).all()
    total = db.query(Admin).count()
    
    return {
        "status": "success",
        "admins": [admin.to_dict() for admin in admins],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.put("/{admin_id}")
async def update_admin(
    admin_id: int,
    updates: AdminUpdate,
    current_admin: Admin = Depends(require_admin_management_permission),
    db: Session = Depends(get_db)
):
    """Update admin information (requires admin management permission)"""
    target_admin = db.query(Admin).filter(Admin.id == admin_id).first()
    if not target_admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    
    # Only super admins can modify other super admins
    if target_admin.role == AdminRole.SUPER_ADMIN and current_admin.role != AdminRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can modify other super admins"
        )
    
    # Update fields
    update_data = updates.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(target_admin, field, value)
    
    target_admin.updated_at = datetime.now()
    db.commit()
    db.refresh(target_admin)
    
    # Log the action
    admin_service.log_audit_event(
        db=db,
        action="admin_updated",
        admin_id=current_admin.id,
        resource_type="admin",
        resource_id=admin_id,
        details=update_data,
        success=True
    )
    
    return {
        "status": "success",
        "message": "Admin updated successfully",
        "admin": target_admin.to_dict()
    }

# ==================== USER APPROVAL MANAGEMENT ====================

@router.get("/users/pending")
async def get_pending_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_admin: Admin = Depends(require_user_approval_permission),
    db: Session = Depends(get_db)
):
    """Get users pending approval"""
    pending_users = admin_service.get_pending_users(db, skip, limit)
    total = db.query(User).filter(User.status == UserStatus.PENDING).count()
    
    return {
        "status": "success",
        "pending_users": [user.to_dict() for user in pending_users],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.post("/users/approve")
async def approve_user(
    request: UserApprovalRequest,
    current_admin: Admin = Depends(require_user_approval_permission),
    db: Session = Depends(get_db)
):
    """Approve or reject user registration"""
    try:
        result = admin_service.approve_user(db, current_admin.id, request)
        return result
    except Exception as e:
        logger.error(f"User approval failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}/history")
async def get_user_approval_history(
    user_id: int,
    current_admin: Admin = Depends(require_user_approval_permission),
    db: Session = Depends(get_db)
):
    """Get approval history for a specific user"""
    history = admin_service.get_user_approval_history(db, user_id)
    
    return {
        "status": "success",
        "user_id": user_id,
        "approval_history": [record.to_dict() for record in history]
    }

@router.get("/users/search")
async def search_users(
    query: str = Query(..., min_length=1),
    status: Optional[UserStatus] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Search users by username, email, or name"""
    search_query = db.query(User).filter(
        (User.username.contains(query)) |
        (User.email.contains(query)) |
        (User.name.contains(query))
    )
    
    if status:
        search_query = search_query.filter(User.status == status)
    
    users = search_query.offset(skip).limit(limit).all()
    total = search_query.count()
    
    return {
        "status": "success",
        "users": [user.to_dict() for user in users],
        "total": total,
        "query": query,
        "status_filter": status.value if status else None,
        "skip": skip,
        "limit": limit
    }

@router.get("/users/stats")
async def get_user_stats(
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Get user statistics"""
    stats = {
        "total_users": db.query(User).count(),
        "pending_approval": db.query(User).filter(User.status == UserStatus.PENDING).count(),
        "approved_users": db.query(User).filter(User.status == UserStatus.APPROVED).count(),
        "rejected_users": db.query(User).filter(User.status == UserStatus.REJECTED).count(),
        "suspended_users": db.query(User).filter(User.status == UserStatus.SUSPENDED).count(),
        "active_users": db.query(User).filter(User.is_active == True).count(),
    }
    
    # Recent registrations (last 7 days)
    week_ago = datetime.now() - timedelta(days=7)
    stats["recent_registrations"] = db.query(User).filter(
        User.created_at >= week_ago
    ).count()
    
    return {
        "status": "success",
        "user_stats": stats
    }

# ==================== AUDIT AND LOGGING ====================

@router.get("/logs/audit")
async def get_audit_logs(
    action: Optional[str] = Query(None),
    admin_id: Optional[int] = Query(None),
    days: int = Query(30, ge=1, le=365),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Get audit logs with filtering"""
    # Check if admin can view logs
    if not current_admin.can_view_logs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Log viewing permission required"
        )
    
    logs = admin_service.get_audit_logs(
        db=db,
        admin_id=admin_id,
        action=action,
        days=days,
        skip=skip,
        limit=limit
    )
    
    total = db.query(AuditLog).filter(
        AuditLog.created_at >= (datetime.now() - timedelta(days=days))
    ).count()
    
    return {
        "status": "success",
        "audit_logs": [log.to_dict() for log in logs],
        "total": total,
        "filters": {
            "action": action,
            "admin_id": admin_id,
            "days": days
        },
        "skip": skip,
        "limit": limit
    }

@router.get("/logs/actions")
async def get_available_log_actions(
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Get list of available log actions for filtering"""
    if not current_admin.can_view_logs:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Log viewing permission required"
        )
    
    actions = db.query(AuditLog.action).distinct().all()
    return {
        "status": "success",
        "available_actions": [action[0] for action in actions]
    }

# ==================== NOTIFICATIONS ====================

@router.get("/notifications/pending")
async def get_pending_notifications(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Get notifications that need to be sent"""
    if not current_admin.can_send_notifications:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Notification permission required"
        )
    
    pending_notifications = db.query(UserNotification).filter(
        UserNotification.is_sent == False
    ).offset(skip).limit(limit).all()
    
    total = db.query(UserNotification).filter(
        UserNotification.is_sent == False
    ).count()
    
    return {
        "status": "success",
        "pending_notifications": [notif.to_dict() for notif in pending_notifications],
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.post("/notifications/{notification_id}/mark-sent")
async def mark_notification_sent(
    notification_id: int,
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Mark a notification as sent"""
    if not current_admin.can_send_notifications:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Notification permission required"
        )
    
    notification = db.query(UserNotification).filter(
        UserNotification.id == notification_id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    
    notification.is_sent = True
    notification.sent_at = datetime.now()
    db.commit()
    
    return {
        "status": "success",
        "message": "Notification marked as sent",
        "notification": notification.to_dict()
    }

# ==================== SYSTEM DASHBOARD ====================

@router.get("/dashboard")
async def get_admin_dashboard(
    current_admin: Admin = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    """Get admin dashboard data"""
    # User stats
    user_stats = {
        "total_users": db.query(User).count(),
        "pending_approval": db.query(User).filter(User.status == UserStatus.PENDING).count(),
        "approved_users": db.query(User).filter(User.status == UserStatus.APPROVED).count(),
        "rejected_users": db.query(User).filter(User.status == UserStatus.REJECTED).count(),
        "suspended_users": db.query(User).filter(User.status == UserStatus.SUSPENDED).count(),
    }
    
    # Recent activity (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    recent_activity = {
        "new_registrations": db.query(User).filter(User.created_at >= yesterday).count(),
        "recent_approvals": db.query(UserApprovalRecord).filter(
            UserApprovalRecord.created_at >= yesterday
        ).count(),
        "admin_actions": db.query(AuditLog).filter(
            AuditLog.created_at >= yesterday,
            AuditLog.admin_id.isnot(None)
        ).count()
    }
    
    # Pending items requiring attention
    pending_items = {
        "users_awaiting_approval": user_stats["pending_approval"],
        "unsent_notifications": db.query(UserNotification).filter(
            UserNotification.is_sent == False
        ).count()
    }
    
    # Recent approval actions (for activity feed)
    recent_approvals = db.query(UserApprovalRecord).filter(
        UserApprovalRecord.created_at >= yesterday
    ).order_by(UserApprovalRecord.created_at.desc()).limit(10).all()
    
    return {
        "status": "success",
        "dashboard": {
            "user_stats": user_stats,
            "recent_activity": recent_activity,
            "pending_items": pending_items,
            "recent_approvals": [record.to_dict() for record in recent_approvals],
            "admin_info": {
                "role": current_admin.role.value,
                "permissions": {
                    "can_approve_users": current_admin.can_approve_users,
                    "can_manage_admins": current_admin.can_manage_admins,
                    "can_view_logs": current_admin.can_view_logs,
                    "can_send_notifications": current_admin.can_send_notifications
                }
            }
        }
    }

# ==================== HEALTH CHECK ====================

@router.get("/health")
async def admin_health_check():
    """Admin API health check"""
    return {
        "status": "healthy",
        "service": "admin_api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }