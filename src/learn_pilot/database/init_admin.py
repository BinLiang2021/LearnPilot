"""
Initialize Default Admin User
Creates a default super admin user for system initialization
"""

from sqlalchemy.orm import Session
try:
    from .models import Admin, AdminRole
    from ..auth.admin_auth import hash_admin_password
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.learn_pilot.database.models import Admin, AdminRole
    from src.learn_pilot.auth.admin_auth import hash_admin_password
import logging

logger = logging.getLogger(__name__)

def create_default_admin(db: Session):
    """Create default super admin user if none exists"""
    try:
        # Check if any admin users exist
        existing_admin = db.query(Admin).filter(Admin.is_active == True).first()
        
        if not existing_admin:
            logger.info("No admin users found. Creating default super admin...")
            
            # Create default super admin
            default_admin = Admin(
                username="admin",
                email="admin@learnpilot.com",
                name="系统管理员",
                password_hash=hash_admin_password("admin123"),
                role=AdminRole.SUPER_ADMIN,
                is_active=True,
                can_approve_users=True,
                can_manage_admins=True,
                can_view_logs=True,
                can_send_notifications=True
            )
            
            db.add(default_admin)
            db.commit()
            db.refresh(default_admin)
            
            logger.info("✅ Default super admin created successfully!")
            logger.info("   Username: admin")
            logger.info("   Password: admin123")
            logger.info("   ⚠️  Please change the default password after first login!")
            
            return default_admin
        else:
            logger.info("Admin users already exist. Skipping default admin creation.")
            return existing_admin
            
    except Exception as e:
        logger.error(f"Failed to create default admin: {str(e)}")
        db.rollback()
        raise e