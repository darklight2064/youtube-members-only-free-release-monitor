#!/usr/bin/env python3
"""
Email notification system using Resend API
"""

import resend
import os
from typing import List, Dict
import logging
from datetime import datetime

class EmailNotifier:
    def __init__(self, api_key: str, from_email: str, to_email: str):
        self.api_key = api_key
        self.from_email = from_email
        self.to_email = to_email
        self.logger = self._setup_logger()
        
        # Initialize Resend
        resend.api_key = api_key
        
    def _setup_logger(self) -> logging.Logger:
        """Set up logging for the notifier"""
        logger = logging.getLogger("email_notifier")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def send_notification(self, changes: List[Dict]) -> bool:
        """Send email notification for video changes"""
        if not changes:
            self.logger.info("No changes to notify about")
            return True
        
        try:
            subject = self._generate_subject(changes)
            html_content = self._generate_html_content(changes)
            text_content = self._generate_text_content(changes)
            
            self.logger.info(f"Sending notification for {len(changes)} changes")
            
            params = {
                "from": self.from_email,
                "to": [self.to_email],
                "subject": subject,
                "html": html_content,
                "text": text_content,
            }
            
            email = resend.Emails.send(params)
            
            self.logger.info(f"✅ Email sent successfully: {email}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send email: {e}")
            return False
    
    def _generate_subject(self, changes: List[Dict]) -> str:
        """Generate email subject line"""
        if len(changes) == 1:
            return f"🎉 Member-only video became free: {changes[0]['title'][:50]}..."
        else:
            return f"🎉 {len(changes)} member-only videos became free!"
    
    def _generate_html_content(self, changes: List[Dict]) -> str:
        """Generate HTML email content"""
        html = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .header { background-color: #f4f4f4; padding: 20px; text-align: center; }
                .content { padding: 20px; }
                .video { background-color: #f9f9f9; margin: 15px 0; padding: 15px; border-radius: 5px; }
                .video-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; }
                .video-url { color: #0066cc; text-decoration: none; }
                .status { margin: 5px 0; }
                .timestamp { color: #666; font-size: 12px; }
                .footer { background-color: #f4f4f4; padding: 15px; text-align: center; font-size: 12px; color: #666; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎉 YouTube Member-Only Videos Now Free!</h1>
            </div>
            
            <div class="content">
                <p>Great news! The following member-only videos have become free to watch:</p>
        """
        
        for change in changes:
            html += f"""
                <div class="video">
                    <div class="video-title">{change['title']}</div>
                    <div class="status">
                        <strong>Status Change:</strong> {change['previous_status']} → {change['current_status']}
                    </div>
                    <div>
                        <a href="{change['url']}" class="video-url">Watch Now →</a>
                    </div>
                    <div class="timestamp">Detected: {change['detected_at']}</div>
                </div>
            """
        
        html += """
                <p>Don't miss out - these videos might return to member-only status later!</p>
            </div>
            
            <div class="footer">
                <p>YouTube Playlist Monitor • Automated notification system</p>
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _generate_text_content(self, changes: List[Dict]) -> str:
        """Generate plain text email content"""
        text = "🎉 YouTube Member-Only Videos Now Free!\n\n"
        text += "The following member-only videos have become free to watch:\n\n"
        
        for i, change in enumerate(changes, 1):
            text += f"{i}. {change['title']}\n"
            text += f"   Status: {change['previous_status']} → {change['current_status']}\n"
            text += f"   Watch: {change['url']}\n"
            text += f"   Detected: {change['detected_at']}\n\n"
        
        text += "Don't miss out - these videos might return to member-only status later!\n\n"
        text += "---\nYouTube Playlist Monitor • Automated notification system"
        
        return text
    
    def send_test_notification(self) -> bool:
        """Send a test notification to verify email setup"""
        test_changes = [{
            'type': 'member_to_free',
            'video_id': 'test123',
            'title': 'Test Video - Email Setup Working',
            'url': 'https://youtube.com/watch?v=test123',
            'previous_status': 'member_only',
            'current_status': 'public',
            'detected_at': datetime.now().isoformat()
        }]
        
        self.logger.info("Sending test notification")
        return self.send_notification(test_changes)

if __name__ == "__main__":
    # Test the email notifier
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('RESEND_API_KEY')
    from_email = os.getenv('FROM_EMAIL')
    to_email = os.getenv('TO_EMAIL')
    
    if not all([api_key, from_email, to_email]):
        print("❌ Missing email configuration. Please set up .env file")
        print("Required: RESEND_API_KEY, FROM_EMAIL, TO_EMAIL")
    else:
        notifier = EmailNotifier(api_key, from_email, to_email)
        success = notifier.send_test_notification()
        if success:
            print("✅ Test email sent successfully!")
        else:
            print("❌ Failed to send test email")