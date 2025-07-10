#!/usr/bin/env python3
"""
YouTube Playlist Monitor - Main application
"""

import schedule
import time
import signal
import sys
import logging
from datetime import datetime

from src.config import Config
from src.playlist_monitor import PlaylistMonitor
from src.email_notifier import EmailNotifier

class YouTubePlaylistMonitor:
    def __init__(self):
        self.config = Config()
        self.monitor = PlaylistMonitor(self.config.playlist_url, self.config.state_file)
        self.notifier = EmailNotifier(
            self.config.resend_api_key,
            self.config.from_email,
            self.config.to_email
        )
        self.logger = self._setup_logger()
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _setup_logger(self) -> logging.Logger:
        """Set up main application logger"""
        logger = logging.getLogger("youtube_monitor")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
            
            # File handler
            file_handler = logging.FileHandler('monitor.log')
            file_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        self.logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def monitor_and_notify(self):
        """Perform one monitoring cycle with notifications"""
        self.logger.info("🔍 Starting monitoring cycle")
        
        try:
            # Monitor for changes
            changes = self.monitor.monitor_once()
            
            if changes:
                self.logger.info(f"🎉 Found {len(changes)} video(s) that became free!")
                
                # Send notifications
                success = self.notifier.send_notification(changes)
                if success:
                    self.logger.info("📧 Notification sent successfully")
                else:
                    self.logger.error("❌ Failed to send notification")
            else:
                self.logger.info("📊 No changes detected")
                
        except Exception as e:
            self.logger.error(f"❌ Error during monitoring cycle: {e}")
    
    def run_scheduled(self):
        """Run the monitor with scheduling"""
        self.logger.info("🚀 Starting YouTube Playlist Monitor")
        self.logger.info(f"📋 Monitoring playlist every {self.config.monitor_interval_minutes} minutes")
        self.logger.info(f"📧 Notifications will be sent to: {self.config.to_email}")
        
        # Schedule monitoring
        schedule.every(self.config.monitor_interval_minutes).minutes.do(self.monitor_and_notify)
        
        # Run initial check
        self.logger.info("🔍 Running initial monitoring check")
        self.monitor_and_notify()
        
        # Main loop
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(1)
            except KeyboardInterrupt:
                break
            except Exception as e:
                self.logger.error(f"❌ Unexpected error: {e}")
                time.sleep(60)  # Wait a minute before continuing
        
        self.logger.info("👋 Monitor stopped")
    
    def run_once(self):
        """Run the monitor once and exit"""
        self.logger.info("🔍 Running single monitoring check")
        self.monitor_and_notify()
    
    def test_email(self):
        """Test email notification system"""
        self.logger.info("📧 Testing email notification system")
        success = self.notifier.send_test_notification()
        if success:
            self.logger.info("✅ Test email sent successfully!")
            return True
        else:
            self.logger.error("❌ Failed to send test email")
            return False

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="YouTube Playlist Monitor")
    parser.add_argument(
        '--mode', 
        choices=['once', 'monitor', 'test-email'], 
        default='once',
        help='Run mode: once (single check - default), monitor (continuous), test-email (test notifications)'
    )
    
    args = parser.parse_args()
    
    try:
        app = YouTubePlaylistMonitor()
        
        if args.mode == 'once':
            app.run_once()
        elif args.mode == 'monitor':
            app.run_scheduled()
        elif args.mode == 'test-email':
            success = app.test_email()
            sys.exit(0 if success else 1)
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease create a .env file with the required settings.")
        print("See .env.example for reference.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Monitor stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()