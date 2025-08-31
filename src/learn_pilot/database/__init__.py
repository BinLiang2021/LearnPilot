"""
Database package initialization
"""

from .models import db_manager, get_db, Base
from .service import db_service

# Initialize database
def init_database():
    """Initialize the database with all tables"""
    print("🗄️  Initializing database...")
    db_manager.create_tables()
    
    # Create default admin user if none exists
    from .init_admin import create_default_admin
    db = db_manager.get_session()
    try:
        create_default_admin(db)
    finally:
        db.close()
        
    print("✅ Database initialized successfully!")

__all__ = ['db_manager', 'get_db', 'db_service', 'init_database', 'Base']