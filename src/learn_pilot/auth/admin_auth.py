"""
Admin Authentication and Authorization Module
Handles admin-specific authentication, permissions, and access control
"""

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import jwt
import hashlib
import secrets
from functools import wraps
from pydantic import BaseModel

try:
    from ..database import get_db
    from ..database.models import (
        Admin, User, AuditLog, UserApprovalRecord, UserNotification,
        AdminRole, UserStatus, ApprovalAction, NotificationType
    )
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.learn_pilot.database import get_db
    from src.learn_pilot.database.models import (
        Admin, User, AuditLog, UserApprovalRecord, UserNotification,
        AdminRole, UserStatus, ApprovalAction, NotificationType
    )

# Configuration - these should be moved to environment variables
ADMIN_SECRET_KEY = secrets.token_urlsafe(32)
ADMIN_TOKEN_EXPIRE_MINUTES = 8 * 60  # 8 hours

security = HTTPBearer()

class AdminToken(BaseModel):
    access_token: str
    token_type: str = "bearer"
    admin_id: int
    username: str
    role: str
    expires_in: int

class AdminTokenData(BaseModel):
    admin_id: Optional[int] = None
    username: Optional[str] = None
    role: Optional[str] = None

class AdminCreate(BaseModel):
    username: str
    name: str
    email: str
    password: str
    role: AdminRole = AdminRole.REVIEWER

class AdminLogin(BaseModel):
    username: str
    password: str

class AdminUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    role: Optional[AdminRole] = None
    can_approve_users: Optional[bool] = None
    can_manage_admins: Optional[bool] = None
    can_view_logs: Optional[bool] = None
    can_send_notifications: Optional[bool] = None

class UserApprovalRequest(BaseModel):
    user_id: int
    action: ApprovalAction
    reason: Optional[str] = None
    notes: Optional[str] = None

class AuthenticationError(Exception):
    """Custom authentication error for admins"""
    pass

class AuthorizationError(Exception):
    """Custom authorization error for admins"""
    pass

def hash_admin_password(password: str) -> str:
    """Hash admin password with salt (more secure than user passwords)"""
    salt = secrets.token_urlsafe(32)  # Longer salt for admins
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 200000)  # More iterations
    return f"{salt}:{pwd_hash.hex()}"

def verify_admin_password(password: str, hashed_password: str) -> bool:
    """Verify admin password against hash"""
    try:
        salt, pwd_hash = hashed_password.split(':')
        return pwd_hash == hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 200000).hex()
    except ValueError:
        return False

def create_admin_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token for admin"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ADMIN_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ADMIN_SECRET_KEY, algorithm="HS256")
    return encoded_jwt

def verify_admin_token(token: str) -> AdminTokenData:
    """Verify JWT token and extract admin data"""
    try:
        payload = jwt.decode(token, ADMIN_SECRET_KEY, algorithms=["HS256"])
        admin_id: int = payload.get("admin_id")
        username: str = payload.get("username")
        role: str = payload.get("role")
        
        if admin_id is None or username is None or role is None:
            raise AuthenticationError("Invalid admin token")
        
        return AdminTokenData(admin_id=admin_id, username=username, role=role)
    except jwt.PyJWTError:
        raise AuthenticationError("Invalid admin token")

def authenticate_admin(db: Session, username: str, password: str) -> Optional[Admin]:
    """Authenticate admin credentials"""
    admin = db.query(Admin).filter(Admin.username == username, Admin.is_active == True).first()
    if not admin or not verify_admin_password(password, admin.password_hash):
        return None
    return admin

def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security), 
    db: Session = Depends(get_db)
) -> Admin:
    """Get current authenticated admin"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = verify_admin_token(credentials.credentials)
    except AuthenticationError:
        raise credentials_exception
    
    admin = db.query(Admin).filter(Admin.id == token_data.admin_id).first()
    if admin is None or not admin.is_active:
        raise credentials_exception
    
    return admin

def get_current_active_admin(current_admin: Admin = Depends(get_current_admin)) -> Admin:
    """Get current active admin"""
    if not current_admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive admin")
    return current_admin

# Permission decorators and checks
def require_permission(permission: str):
    """Decorator to require specific admin permission"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get current admin from kwargs (injected by FastAPI)
            current_admin = None
            for key, value in kwargs.items():
                if isinstance(value, Admin):
                    current_admin = value
                    break
            
            if not current_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Admin authentication required"
                )
            
            # Check specific permission
            if not has_permission(current_admin, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Insufficient permissions: {permission} required"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def has_permission(admin: Admin, permission: str) -> bool:
    """Check if admin has specific permission"""
    if not admin.is_active:
        return False
    
    permission_map = {
        'approve_users': admin.can_approve_users,
        'manage_admins': admin.can_manage_admins,
        'view_logs': admin.can_view_logs,
        'send_notifications': admin.can_send_notifications,
        'super_admin': admin.role == AdminRole.SUPER_ADMIN
    }
    
    return permission_map.get(permission, False)

def require_super_admin(admin: Admin = Depends(get_current_active_admin)) -> Admin:
    """Dependency that requires super admin role"""
    if admin.role != AdminRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return admin

def require_user_approval_permission(admin: Admin = Depends(get_current_active_admin)) -> Admin:
    """Dependency that requires user approval permission"""
    if not admin.can_approve_users:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User approval permission required"
        )
    return admin

def require_admin_management_permission(admin: Admin = Depends(get_current_active_admin)) -> Admin:
    """Dependency that requires admin management permission"""
    if not admin.can_manage_admins:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin management permission required"
        )
    return admin

class AdminService:
    """Service class for admin operations"""
    
    @staticmethod
    def create_admin(db: Session, admin_data: AdminCreate, creator_id: Optional[int] = None) -> Admin:
        """Create a new admin"""
        # Check if username/email already exists
        existing_admin = db.query(Admin).filter(
            (Admin.username == admin_data.username) | 
            (Admin.email == admin_data.email)
        ).first()
        
        if existing_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )
        
        # Hash password
        password_hash = hash_admin_password(admin_data.password)
        
        # Create admin
        admin = Admin(
            username=admin_data.username,
            email=admin_data.email,
            name=admin_data.name,
            password_hash=password_hash,
            role=admin_data.role,
            created_by=creator_id,
            # Set permissions based on role
            can_approve_users=True,
            can_manage_admins=(admin_data.role == AdminRole.SUPER_ADMIN),
            can_view_logs=True,
            can_send_notifications=True
        )
        
        db.add(admin)
        db.commit()
        db.refresh(admin)
        
        return admin
    
    @staticmethod
    def login_admin(db: Session, credentials: AdminLogin, request: Optional[Request] = None) -> Dict[str, Any]:
        """Authenticate and login admin"""
        admin = authenticate_admin(db, credentials.username, credentials.password)
        if not admin:
            # Log failed login attempt
            AdminService.log_audit_event(
                db=db,
                action="admin_login_failed",
                admin_id=None,
                details={"username": credentials.username},
                success=False,
                ip_address=request.client.host if request and hasattr(request, 'client') else None,
                user_agent=request.headers.get('user-agent') if request and hasattr(request, 'headers') else None
            )
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Update last login
        admin.last_login = datetime.now()
        db.commit()
        
        # Generate access token
        access_token_expires = timedelta(minutes=ADMIN_TOKEN_EXPIRE_MINUTES)
        access_token = create_admin_token(
            data={
                "admin_id": admin.id, 
                "username": admin.username, 
                "role": admin.role.value
            },
            expires_delta=access_token_expires
        )
        
        # Log successful login
        AdminService.log_audit_event(
            db=db,
            action="admin_login_success",
            admin_id=admin.id,
            details={"role": admin.role.value},
            success=True,
            ip_address=request.client.host if request and hasattr(request, 'client') else None,
            user_agent=request.headers.get('user-agent') if request and hasattr(request, 'headers') else None
        )
        
        return {
            "admin": admin.to_dict(),
            "token": AdminToken(
                access_token=access_token,
                admin_id=admin.id,
                username=admin.username,
                role=admin.role.value,
                expires_in=ADMIN_TOKEN_EXPIRE_MINUTES * 60
            )
        }
    
    @staticmethod
    def approve_user(db: Session, admin_id: int, request: UserApprovalRequest) -> Dict[str, Any]:
        """Approve or reject user registration"""
        # Get user
        user = db.query(User).filter(User.id == request.user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Get admin
        admin = db.query(Admin).filter(Admin.id == admin_id).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        
        previous_status = user.status.value if user.status else None
        
        # Update user status based on action
        if request.action == ApprovalAction.APPROVE:
            user.status = UserStatus.APPROVED
            user.approved_at = datetime.now()
            user.approved_by = admin_id
            user.rejection_reason = None
            
            # Create approval notification
            notification = UserNotification(
                user_id=user.id,
                title="Account Approved!",
                message=f"Congratulations! Your LearnPilot account has been approved by {admin.name}. You can now access all features of the platform.",
                notification_type=NotificationType.SYSTEM,
                related_record_type='approval',
                related_record_id=request.user_id
            )
            
        elif request.action == ApprovalAction.REJECT:
            user.status = UserStatus.REJECTED
            user.rejection_reason = request.reason
            
            # Create rejection notification
            notification = UserNotification(
                user_id=user.id,
                title="Account Registration Rejected",
                message=f"Unfortunately, your LearnPilot account registration has been rejected. Reason: {request.reason or 'Not specified'}. Please contact support if you have questions.",
                notification_type=NotificationType.SYSTEM,
                related_record_type='approval',
                related_record_id=request.user_id
            )
            
        elif request.action == ApprovalAction.SUSPEND:
            user.status = UserStatus.SUSPENDED
            user.is_active = False
            
            notification = UserNotification(
                user_id=user.id,
                title="Account Suspended",
                message=f"Your LearnPilot account has been suspended. Reason: {request.reason or 'Not specified'}. Please contact support for assistance.",
                notification_type=NotificationType.SYSTEM,
                related_record_type='approval',
                related_record_id=request.user_id
            )
            
        elif request.action == ApprovalAction.REACTIVATE:
            user.status = UserStatus.APPROVED
            user.is_active = True
            
            notification = UserNotification(
                user_id=user.id,
                title="Account Reactivated",
                message="Your LearnPilot account has been reactivated. Welcome back!",
                notification_type=NotificationType.SYSTEM,
                related_record_type='approval',
                related_record_id=request.user_id
            )
        
        # Create approval record
        approval_record = UserApprovalRecord(
            user_id=request.user_id,
            admin_id=admin_id,
            action=request.action,
            reason=request.reason,
            notes=request.notes,
            previous_status=previous_status,
            new_status=user.status.value
        )
        
        # Add to database
        db.add(notification)
        db.add(approval_record)
        db.commit()
        
        # Log audit event
        AdminService.log_audit_event(
            db=db,
            action=f"user_{request.action.value}",
            admin_id=admin_id,
            user_id=request.user_id,
            resource_type="user",
            resource_id=request.user_id,
            details={
                "previous_status": previous_status,
                "new_status": user.status.value,
                "reason": request.reason,
                "notes": request.notes
            },
            success=True
        )
        
        return {
            "status": "success",
            "user": user.to_dict(),
            "approval_record": approval_record.to_dict(),
            "notification_created": True
        }
    
    @staticmethod
    def get_pending_users(db: Session, skip: int = 0, limit: int = 50) -> List[User]:
        """Get users pending approval"""
        return db.query(User).filter(
            User.status == UserStatus.PENDING
        ).order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_user_approval_history(db: Session, user_id: int) -> List[UserApprovalRecord]:
        """Get approval history for a specific user"""
        return db.query(UserApprovalRecord).filter(
            UserApprovalRecord.user_id == user_id
        ).order_by(UserApprovalRecord.created_at.desc()).all()
    
    @staticmethod
    def log_audit_event(db: Session, action: str, admin_id: Optional[int] = None, 
                       user_id: Optional[int] = None, resource_type: Optional[str] = None,
                       resource_id: Optional[int] = None, details: Optional[Dict] = None,
                       success: bool = True, error_message: Optional[str] = None,
                       ip_address: Optional[str] = None, user_agent: Optional[str] = None):
        """Create an audit log entry"""
        audit_log = AuditLog(
            admin_id=admin_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            success=success,
            error_message=error_message,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        db.add(audit_log)
        db.commit()
    
    @staticmethod
    def get_audit_logs(db: Session, admin_id: Optional[int] = None, 
                      action: Optional[str] = None, days: int = 30,
                      skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """Get audit logs with filtering"""
        query = db.query(AuditLog)
        
        # Filter by date
        since_date = datetime.now() - timedelta(days=days)
        query = query.filter(AuditLog.created_at >= since_date)
        
        # Filter by admin
        if admin_id:
            query = query.filter(AuditLog.admin_id == admin_id)
        
        # Filter by action
        if action:
            query = query.filter(AuditLog.action == action)
        
        return query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit).all()

# Global admin service instance
admin_service = AdminService()