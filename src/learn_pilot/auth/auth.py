"""
Authentication and Authorization Module
Simple JWT-based authentication for LearnPilot
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
import hashlib
import secrets
from pydantic import BaseModel

try:
    from ..database import db_service, get_db
    from ..database.models import User, UserStatus
    # from ..services.notification_service import notification_service
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.learn_pilot.database import db_service, get_db
    from src.learn_pilot.database.models import User, UserStatus
    # from src.learn_pilot.services.notification_service import notification_service

# Configuration
SECRET_KEY = secrets.token_urlsafe(32)  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days

# Security scheme
security = HTTPBearer()

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    username: str
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    name: str
    email: str  # Make email required for notifications
    password: str
    level: str = "intermediate"
    interests: list = []
    daily_hours: float = 2.0
    language: str = "Chinese"
    registration_notes: Optional[str] = None  # Optional notes during registration

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    level: Optional[str] = None
    interests: Optional[list] = None
    daily_hours: Optional[float] = None
    language: Optional[str] = None

class AuthenticationError(Exception):
    """Custom authentication error"""
    pass

def hash_password(password: str) -> str:
    """Hash password with salt"""
    salt = secrets.token_urlsafe(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}:{pwd_hash.hex()}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        salt, pwd_hash = hashed_password.split(':')
        return pwd_hash == hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    except ValueError:
        return False

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """Verify JWT token and extract user data"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        
        if user_id is None or username is None:
            raise AuthenticationError("Invalid token")
        
        return TokenData(user_id=user_id, username=username)
    except jwt.PyJWTError:
        raise AuthenticationError("Invalid token")

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate user credentials"""
    user = db_service.users.get_user_by_username(db, username)
    if not user or not hasattr(user, 'password_hash'):
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), 
                    db: Session = Depends(get_db)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token_data = verify_token(credentials.credentials)
    except AuthenticationError:
        raise credentials_exception
    
    user = db_service.users.get_user_by_id(db, token_data.user_id)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(current_user = Depends(get_current_user)):
    """Get current active user with approval status check"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    # Check approval status
    if current_user.status == UserStatus.PENDING:
        raise HTTPException(
            status_code=403, 
            detail="Account pending approval. Please wait for admin approval."
        )
    elif current_user.status == UserStatus.REJECTED:
        raise HTTPException(
            status_code=403,
            detail="Account registration was rejected. Please contact support."
        )
    elif current_user.status == UserStatus.SUSPENDED:
        raise HTTPException(
            status_code=403,
            detail="Account has been suspended. Please contact support."
        )
    
    return current_user

class AuthService:
    """Authentication service class"""
    
    @staticmethod
    async def register_user(db: Session, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user with approval workflow"""
        # Check if username already exists
        existing_user = db_service.users.get_user_by_username(db, user_data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already exists"
            )
        
        # Check if email already exists
        existing_email = db.query(User).filter(User.email == user_data.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        
        # Hash password
        password_hash = hash_password(user_data.password)
        
        # Create user in database with PENDING status
        user = db_service.users.create_user(
            db=db,
            username=user_data.username,
            name=user_data.name,
            email=user_data.email,
            level=user_data.level,
            interests=user_data.interests,
            daily_hours=user_data.daily_hours,
            language=user_data.language
        )
        
        # Set user status to pending and add registration notes
        user.status = UserStatus.PENDING
        user.password_hash = password_hash
        user.registration_notes = user_data.registration_notes
        db.commit()
        db.refresh(user)
        
        # Notify admins about new registration (disabled for now)
        # try:
        #     await notification_service.notify_admins_new_registration(db, user)
        # except Exception as e:
        #     # Don't fail registration if notification fails
        #     print(f"Warning: Failed to notify admins about new registration: {e}")
        print(f"Info: New user registered: {user.username} (email: {user.email})")
        
        # Don't generate access token for pending users
        return {
            "status": "registration_pending",
            "message": "Registration successful! Your account is pending approval. You will receive an email once your account is reviewed.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "name": user.name,
                "status": user.status.value,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        }
    
    @staticmethod
    def login_user(db: Session, credentials: UserLogin) -> Dict[str, Any]:
        """Authenticate and login user with approval status check"""
        user = authenticate_user(db, credentials.username, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Check approval status before allowing login
        if user.status == UserStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account pending approval. Please wait for admin approval before logging in."
            )
        elif user.status == UserStatus.REJECTED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account registration was rejected. Please contact support."
            )
        elif user.status == UserStatus.SUSPENDED:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account has been suspended. Please contact support."
            )
        
        # Update last login timestamp
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Generate access token only for approved users
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": user.id, "username": user.username},
            expires_delta=access_token_expires
        )
        
        return {
            "user": user.to_dict(),
            "token": Token(
                access_token=access_token,
                user_id=user.id,
                username=user.username,
                expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60
            )
        }
    
    @staticmethod
    def update_user_profile(db: Session, user_id: int, updates: UserUpdate) -> Dict[str, Any]:
        """Update user profile"""
        user = db_service.users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Filter out None values
        update_data = {k: v for k, v in updates.dict().items() if v is not None}
        
        updated_user = db_service.users.update_user_profile(db, user_id, update_data)
        return {"user": updated_user.to_dict()}
    
    @staticmethod
    def get_user_sessions(db: Session, user_id: int, skip: int = 0, limit: int = 20) -> Dict[str, Any]:
        """Get user's analysis sessions"""
        user = db_service.users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        sessions = db_service.sessions.get_user_sessions(db, user_id, skip, limit)
        return {
            "sessions": [session.to_dict() for session in sessions],
            "total": len(sessions)
        }
    
    @staticmethod
    def get_user_learning_plans(db: Session, user_id: int) -> Dict[str, Any]:
        """Get user's learning plans"""
        user = db_service.users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        plans = db_service.plans.get_user_plans(db, user_id)
        return {
            "learning_plans": [plan.to_dict() for plan in plans],
            "total": len(plans)
        }
    
    @staticmethod
    def get_user_progress(db: Session, user_id: int, days: int = 7) -> Dict[str, Any]:
        """Get user's recent learning progress"""
        user = db_service.users.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        progress = db_service.progress.get_recent_activity(db, user_id, days)
        
        # Calculate stats
        total_time = sum(p.time_spent for p in progress)
        avg_completion = sum(p.completion_rate for p in progress) / len(progress) if progress else 0
        
        return {
            "recent_activity": [p.to_dict() for p in progress],
            "stats": {
                "total_time_spent": total_time,
                "average_completion_rate": round(avg_completion, 2),
                "active_plans": len(progress)
            }
        }

# Global auth service instance
auth_service = AuthService()