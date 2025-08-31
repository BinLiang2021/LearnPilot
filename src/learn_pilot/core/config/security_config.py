"""
Security Configuration Module
Centralized security settings and environment variable management
"""

import os
import secrets
from typing import List, Optional
from pydantic import BaseSettings, validator
import logging

logger = logging.getLogger(__name__)

class SecurityConfig(BaseSettings):
    """Security configuration settings"""
    
    # JWT Settings
    jwt_secret_key: str = secrets.token_urlsafe(32)
    admin_jwt_secret_key: str = secrets.token_urlsafe(32)
    access_token_expire_minutes: int = 43200  # 30 days
    admin_token_expire_minutes: int = 480     # 8 hours
    
    # Password Security
    bcrypt_rounds: int = 12
    
    # Rate Limiting
    api_rate_limit: int = 100  # requests per minute per IP
    
    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # File Upload Security
    max_file_size: int = 10485760  # 10MB
    allowed_file_types: List[str] = [".pdf", ".md", ".txt"]
    
    # Session Security
    secure_cookies: bool = True
    session_timeout_minutes: int = 120
    
    @validator('allowed_origins', pre=True)
    def parse_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    @validator('allowed_file_types', pre=True)
    def parse_file_types(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(',') if ext.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class EmailConfig(BaseSettings):
    """Email configuration settings"""
    
    # SMTP Settings
    smtp_server: str = "localhost"
    smtp_port: int = 587
    smtp_use_tls: bool = True
    smtp_username: Optional[str] = None
    smtp_password: Optional[str] = None
    
    # Email Display
    from_email: str = "noreply@learnpilot.com"
    from_name: str = "LearnPilot"
    
    # Development/Testing
    mock_email: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class DatabaseConfig(BaseSettings):
    """Database configuration settings"""
    
    database_url: str = "sqlite:///user_data/papers.db"
    
    # Connection Pool Settings
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600
    
    # Query Settings
    echo_sql: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class ApplicationConfig(BaseSettings):
    """Main application configuration"""
    
    # Application URLs
    app_url: str = "http://localhost:8000"
    admin_panel_url: str = "http://localhost:8000/admin"
    login_url: str = "http://localhost:8000/login"
    
    # Development Settings
    debug: bool = False
    reload: bool = False
    
    # Storage Paths
    upload_dir: str = "user_data/uploads"
    temp_dir: str = "user_data/temp"
    
    # Logging
    log_level: str = "INFO"
    log_file_path: str = "logs/learnpilot.log"
    log_max_size: int = 10485760  # 10MB
    log_backup_count: int = 5
    
    # Monitoring
    enable_metrics: bool = False
    sentry_dsn: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class ApprovalConfig(BaseSettings):
    """User approval workflow configuration"""
    
    # Auto-approval settings
    auto_approve_enabled: bool = False
    auto_approve_domains: List[str] = []
    
    # Notification settings
    notify_admins_new_registration: bool = True
    notify_user_approval: bool = True
    send_welcome_email: bool = True
    
    # Approval timeout
    approval_timeout_days: int = 30
    
    # Default admin settings
    default_admin_username: str = "admin"
    default_admin_password: str = "admin123"
    default_admin_email: str = "admin@learnpilot.com"
    default_admin_name: str = "System Administrator"
    
    @validator('auto_approve_domains', pre=True)
    def parse_domains(cls, v):
        if isinstance(v, str):
            return [domain.strip().lower() for domain in v.split(',') if domain.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class AIConfig(BaseSettings):
    """AI/ML service configuration"""
    
    # OpenAI Settings
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    openai_max_tokens: int = 2048
    
    # Perplexity Settings
    perplexity_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

class Config:
    """Main configuration class that aggregates all settings"""
    
    def __init__(self):
        self.security = SecurityConfig()
        self.email = EmailConfig()
        self.database = DatabaseConfig()
        self.app = ApplicationConfig()
        self.approval = ApprovalConfig()
        self.ai = AIConfig()
        
        # Log configuration loading
        self._log_config_status()
    
    def _log_config_status(self):
        """Log configuration loading status"""
        try:
            logger.info("Configuration loaded successfully")
            logger.info(f"Debug mode: {self.app.debug}")
            logger.info(f"Database URL: {self.database.database_url}")
            logger.info(f"Email mock mode: {self.email.mock_email}")
            logger.info(f"Auto-approval enabled: {self.approval.auto_approve_enabled}")
        except Exception as e:
            logger.error(f"Error logging configuration status: {e}")
    
    def validate_required_settings(self) -> List[str]:
        """Validate that required settings are present"""
        errors = []
        
        # Check JWT secrets in production
        if not self.app.debug:
            default_jwt = secrets.token_urlsafe(32)
            if (self.security.jwt_secret_key == default_jwt or 
                self.security.admin_jwt_secret_key == default_jwt):
                errors.append("JWT secret keys must be set in production")
        
        # Check email settings if notifications are enabled
        if (self.approval.notify_admins_new_registration or 
            self.approval.notify_user_approval):
            if not self.email.smtp_username or not self.email.smtp_password:
                if not self.email.mock_email:
                    errors.append("SMTP credentials required for email notifications")
        
        # Check OpenAI API key if AI features are used
        if not self.ai.openai_api_key and not self.app.debug:
            errors.append("OpenAI API key is required for AI features")
        
        return errors
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return not self.app.debug and os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    def get_database_url(self) -> str:
        """Get database URL with proper formatting"""
        return self.database.database_url
    
    def should_auto_approve(self, email: str) -> bool:
        """Check if email domain is in auto-approve list"""
        if not self.approval.auto_approve_enabled:
            return False
        
        domain = email.lower().split('@')[-1]
        return domain in self.approval.auto_approve_domains

# Global configuration instance
config = Config()

def get_config() -> Config:
    """Get the global configuration instance"""
    return config

# Validation on import
validation_errors = config.validate_required_settings()
if validation_errors:
    error_msg = "Configuration validation errors:\n" + "\n".join(f"- {error}" for error in validation_errors)
    if config.is_production():
        raise RuntimeError(error_msg)
    else:
        logger.warning(error_msg)