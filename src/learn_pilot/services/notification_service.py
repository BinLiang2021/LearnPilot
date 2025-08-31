"""
Notification Service
Handles email notifications and system messages for user approval workflow
"""

import smtplib
import logging
try:
    from email.mime.text import MimeText
    from email.mime.multipart import MimeMultipart
except ImportError:
    # Fallback for systems without email modules
    MimeText = None
    MimeMultipart = None
    print("Warning: Email functionality not available")
from typing import Optional, Dict, Any, List
from datetime import datetime
import asyncio
import os
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session

try:
    from ..database import get_db
    from ..database.models import (
        UserNotification, User, Admin, UserApprovalRecord,
        NotificationType, UserStatus
    )
except ImportError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from src.learn_pilot.database import get_db
    from src.learn_pilot.database.models import (
        UserNotification, User, Admin, UserApprovalRecord,
        NotificationType, UserStatus
    )

# Configure logging
logger = logging.getLogger(__name__)

class EmailConfig:
    """Email configuration"""
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'localhost')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.smtp_use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
        self.from_email = os.getenv('FROM_EMAIL', 'noreply@learnpilot.com')
        self.from_name = os.getenv('FROM_NAME', 'LearnPilot')

class NotificationTemplates:
    """Email and notification templates"""
    
    # HTML email templates
    USER_APPROVED_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Account Approved - LearnPilot</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #2c3e50; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f8f9fa; }
            .footer { padding: 20px; text-align: center; color: #666; }
            .button { display: inline-block; padding: 12px 24px; background-color: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            .success { color: #27ae60; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Welcome to LearnPilot!</h1>
            </div>
            <div class="content">
                <h2 class="success">Your Account Has Been Approved!</h2>
                <p>Dear {{ user_name }},</p>
                <p>Congratulations! Your LearnPilot account has been approved by our admin team. You can now access all features of our AI-powered research paper learning platform.</p>
                
                <p><strong>Account Details:</strong></p>
                <ul>
                    <li>Username: {{ username }}</li>
                    <li>Email: {{ email }}</li>
                    <li>Approved on: {{ approved_date }}</li>
                    <li>Approved by: {{ approver_name }}</li>
                </ul>
                
                <p>You can now:</p>
                <ul>
                    <li>Upload and analyze research papers</li>
                    <li>Generate personalized learning plans</li>
                    <li>Access AI-powered learning guidance</li>
                    <li>Track your learning progress</li>
                </ul>
                
                <p style="text-align: center; margin: 30px 0;">
                    <a href="{{ login_url }}" class="button">Start Learning Now</a>
                </p>
                
                <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
                
                <p>Happy learning!</p>
                <p>The LearnPilot Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 LearnPilot. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    USER_REJECTED_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Registration Update - LearnPilot</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #e74c3c; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f8f9fa; }
            .footer { padding: 20px; text-align: center; color: #666; }
            .warning { color: #e74c3c; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Registration Update</h1>
            </div>
            <div class="content">
                <h2 class="warning">Registration Not Approved</h2>
                <p>Dear {{ user_name }},</p>
                <p>We regret to inform you that your LearnPilot account registration has not been approved at this time.</p>
                
                {% if reason %}
                <p><strong>Reason:</strong></p>
                <p>{{ reason }}</p>
                {% endif %}
                
                <p>If you believe this decision was made in error or if you have additional information to provide, please contact our support team at support@learnpilot.com.</p>
                
                <p>Thank you for your interest in LearnPilot.</p>
                <p>The LearnPilot Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 LearnPilot. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    ADMIN_NEW_REGISTRATION_HTML = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>New User Registration - LearnPilot Admin</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #3498db; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f8f9fa; }
            .footer { padding: 20px; text-align: center; color: #666; }
            .button { display: inline-block; padding: 12px 24px; background-color: #2c3e50; color: white; text-decoration: none; border-radius: 5px; margin: 5px; }
            .user-info { background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📝 New User Registration</h1>
            </div>
            <div class="content">
                <p>Dear Admin,</p>
                <p>A new user has registered on LearnPilot and requires approval.</p>
                
                <div class="user-info">
                    <h3>User Information:</h3>
                    <ul>
                        <li><strong>Name:</strong> {{ user_name }}</li>
                        <li><strong>Username:</strong> {{ username }}</li>
                        <li><strong>Email:</strong> {{ email }}</li>
                        <li><strong>Registration Date:</strong> {{ registration_date }}</li>
                        <li><strong>Learning Level:</strong> {{ level }}</li>
                        <li><strong>Interests:</strong> {{ interests }}</li>
                    </ul>
                    {% if registration_notes %}
                    <p><strong>Registration Notes:</strong></p>
                    <p>{{ registration_notes }}</p>
                    {% endif %}
                </div>
                
                <p style="text-align: center;">
                    <a href="{{ admin_panel_url }}" class="button">Review in Admin Panel</a>
                </p>
                
                <p>Please review and approve/reject this registration at your earliest convenience.</p>
                
                <p>Best regards,<br>LearnPilot System</p>
            </div>
            <div class="footer">
                <p>&copy; 2024 LearnPilot Admin System. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

class NotificationService:
    """Service for handling notifications"""
    
    def __init__(self):
        self.email_config = EmailConfig()
        self.templates = NotificationTemplates()
        
    async def send_email(self, to_email: str, subject: str, html_content: str, 
                        text_content: Optional[str] = None) -> bool:
        """Send email notification"""
        try:
            # Create message
            msg = MimeMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.email_config.from_name} <{self.email_config.from_email}>"
            msg['To'] = to_email
            
            # Add text part if provided
            if text_content:
                text_part = MimeText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML part
            html_part = MimeText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            server = smtplib.SMTP(self.email_config.smtp_server, self.email_config.smtp_port)
            if self.email_config.smtp_use_tls:
                server.starttls()
            
            if self.email_config.smtp_username and self.email_config.smtp_password:
                server.login(self.email_config.smtp_username, self.email_config.smtp_password)
            
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def render_template(self, template_html: str, **kwargs) -> str:
        """Render email template with variables"""
        try:
            # Simple template rendering using string replacement
            # In production, consider using Jinja2 for more complex templating
            rendered = template_html
            for key, value in kwargs.items():
                placeholder = f"{{{{ {key} }}}}"
                rendered = rendered.replace(placeholder, str(value or ''))
            return rendered
        except Exception as e:
            logger.error(f"Template rendering failed: {str(e)}")
            return template_html
    
    async def send_user_approved_email(self, user: User, approver: Admin) -> bool:
        """Send approval notification email to user"""
        try:
            subject = "🎉 Your LearnPilot Account Has Been Approved!"
            
            html_content = self.render_template(
                self.templates.USER_APPROVED_HTML,
                user_name=user.name,
                username=user.username,
                email=user.email,
                approved_date=user.approved_at.strftime("%B %d, %Y at %I:%M %p") if user.approved_at else "",
                approver_name=approver.name if approver else "Admin",
                login_url="https://learnpilot.com/login"  # Replace with actual URL
            )
            
            return await self.send_email(user.email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Failed to send approval email to user {user.id}: {str(e)}")
            return False
    
    async def send_user_rejected_email(self, user: User, reason: Optional[str] = None) -> bool:
        """Send rejection notification email to user"""
        try:
            subject = "LearnPilot Registration Update"
            
            html_content = self.render_template(
                self.templates.USER_REJECTED_HTML,
                user_name=user.name,
                reason=reason or "Not specified"
            )
            
            return await self.send_email(user.email, subject, html_content)
            
        except Exception as e:
            logger.error(f"Failed to send rejection email to user {user.id}: {str(e)}")
            return False
    
    async def send_admin_new_registration_email(self, user: User, admin_emails: List[str]) -> bool:
        """Send new registration notification to admins"""
        try:
            subject = f"New User Registration: {user.name}"
            
            html_content = self.render_template(
                self.templates.ADMIN_NEW_REGISTRATION_HTML,
                user_name=user.name,
                username=user.username,
                email=user.email,
                registration_date=user.created_at.strftime("%B %d, %Y at %I:%M %p") if user.created_at else "",
                level=user.level,
                interests=", ".join(user.interests) if user.interests else "None specified",
                registration_notes=user.registration_notes or "",
                admin_panel_url="https://learnpilot.com/admin"  # Replace with actual URL
            )
            
            # Send to all admin emails
            success_count = 0
            for email in admin_emails:
                if await self.send_email(email, subject, html_content):
                    success_count += 1
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to send admin notification for user {user.id}: {str(e)}")
            return False
    
    async def create_system_notification(self, db: Session, user_id: int, title: str, 
                                       message: str, related_record_type: Optional[str] = None,
                                       related_record_id: Optional[int] = None) -> UserNotification:
        """Create a system notification in the database"""
        try:
            notification = UserNotification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=NotificationType.SYSTEM,
                related_record_type=related_record_type,
                related_record_id=related_record_id,
                is_read=False,
                is_sent=True,  # System notifications are immediately "sent"
                sent_at=datetime.now()
            )
            
            db.add(notification)
            db.commit()
            db.refresh(notification)
            
            logger.info(f"Created system notification {notification.id} for user {user_id}")
            return notification
            
        except Exception as e:
            logger.error(f"Failed to create system notification for user {user_id}: {str(e)}")
            db.rollback()
            raise
    
    async def process_approval_notifications(self, db: Session, user: User, 
                                           approval_record: UserApprovalRecord, 
                                           admin: Admin) -> Dict[str, Any]:
        """Process all notifications for a user approval action"""
        results = {
            "email_sent": False,
            "system_notification_created": False,
            "admin_notification_sent": False
        }
        
        try:
            # Send email notification to user
            if user.email:
                if approval_record.action.value == 'approve':
                    results["email_sent"] = await self.send_user_approved_email(user, admin)
                elif approval_record.action.value == 'reject':
                    results["email_sent"] = await self.send_user_rejected_email(
                        user, approval_record.reason
                    )
            
            # Create system notification
            if approval_record.action.value == 'approve':
                title = "🎉 Account Approved!"
                message = f"Welcome to LearnPilot! Your account has been approved by {admin.name}. You can now access all platform features."
            elif approval_record.action.value == 'reject':
                title = "Registration Update"
                message = f"Your registration has been reviewed. Reason: {approval_record.reason or 'Not specified'}"
            elif approval_record.action.value == 'suspend':
                title = "Account Suspended"
                message = f"Your account has been suspended. Reason: {approval_record.reason or 'Not specified'}"
            elif approval_record.action.value == 'reactivate':
                title = "Account Reactivated"
                message = "Your account has been reactivated. Welcome back to LearnPilot!"
            else:
                title = "Account Update"
                message = f"Your account status has been updated by {admin.name}."
            
            notification = await self.create_system_notification(
                db, user.id, title, message, 'approval', approval_record.id
            )
            results["system_notification_created"] = notification is not None
            
            # Send notification to other admins if it's a new registration
            if approval_record.action.value in ['approve', 'reject'] and user.status == UserStatus.PENDING:
                admin_emails = db.query(Admin.email).filter(
                    Admin.is_active == True,
                    Admin.can_approve_users == True,
                    Admin.id != admin.id  # Don't notify the admin who performed the action
                ).all()
                
                if admin_emails:
                    email_list = [email[0] for email in admin_emails]
                    results["admin_notification_sent"] = await self.send_admin_new_registration_email(
                        user, email_list
                    )
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to process approval notifications: {str(e)}")
            return results
    
    async def notify_admins_new_registration(self, db: Session, user: User) -> bool:
        """Notify all admins about a new user registration"""
        try:
            # Get all active admins who can approve users
            admin_emails = db.query(Admin.email).filter(
                Admin.is_active == True,
                Admin.can_approve_users == True
            ).all()
            
            if not admin_emails:
                logger.warning("No active admins found to notify about new registration")
                return False
            
            email_list = [email[0] for email in admin_emails]
            return await self.send_admin_new_registration_email(user, email_list)
            
        except Exception as e:
            logger.error(f"Failed to notify admins about new registration: {str(e)}")
            return False
    
    async def get_user_notifications(self, db: Session, user_id: int, 
                                   unread_only: bool = False, skip: int = 0, 
                                   limit: int = 20) -> List[UserNotification]:
        """Get notifications for a user"""
        query = db.query(UserNotification).filter(UserNotification.user_id == user_id)
        
        if unread_only:
            query = query.filter(UserNotification.is_read == False)
        
        return query.order_by(UserNotification.created_at.desc()).offset(skip).limit(limit).all()
    
    async def mark_notification_read(self, db: Session, notification_id: int, 
                                   user_id: int) -> bool:
        """Mark a notification as read"""
        try:
            notification = db.query(UserNotification).filter(
                UserNotification.id == notification_id,
                UserNotification.user_id == user_id
            ).first()
            
            if not notification:
                return False
            
            notification.is_read = True
            notification.read_at = datetime.now()
            db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to mark notification {notification_id} as read: {str(e)}")
            db.rollback()
            return False
    
    async def get_unread_notification_count(self, db: Session, user_id: int) -> int:
        """Get count of unread notifications for a user"""
        return db.query(UserNotification).filter(
            UserNotification.user_id == user_id,
            UserNotification.is_read == False
        ).count()

# Global notification service instance
notification_service = NotificationService()