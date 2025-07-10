#!/usr/bin/env python3
"""
Configuration management for YouTube Playlist Monitor
"""

import os
from dotenv import load_dotenv
from typing import Optional

class Config:
    def __init__(self, env_file: str = ".env"):
        """Load configuration from environment variables"""
        load_dotenv(env_file)
        
        # Required settings
        self.resend_api_key = os.getenv('RESEND_API_KEY')
        self.to_email = os.getenv('TO_EMAIL')
        self.from_email = os.getenv('FROM_EMAIL')
        
        # Optional settings with defaults
        self.playlist_url = os.getenv(
            'PLAYLIST_URL', 
            'https://www.youtube.com/playlist?list=PLO_DkCSmTKMNMgr-JKMDV2Sw2HW59LMvc'
        )
        self.monitor_interval_minutes = int(os.getenv('MONITOR_INTERVAL_MINUTES', '30'))
        self.state_file = os.getenv('STATE_FILE', 'playlist_state.json')
        
        # Validate required settings
        self._validate()
    
    def _validate(self):
        """Validate that required configuration is present"""
        required_fields = {
            'RESEND_API_KEY': self.resend_api_key,
            'TO_EMAIL': self.to_email,
            'FROM_EMAIL': self.from_email,
        }
        
        missing_fields = [field for field, value in required_fields.items() if not value]
        
        if missing_fields:
            raise ValueError(
                f"Missing required configuration: {', '.join(missing_fields)}\n"
                f"Please set these in your .env file or environment variables."
            )
    
    def is_valid(self) -> bool:
        """Check if configuration is valid"""
        try:
            self._validate()
            return True
        except ValueError:
            return False
    
    def __str__(self) -> str:
        """String representation of config (safe - no secrets)"""
        return f"""Configuration:
  Playlist URL: {self.playlist_url}
  Monitor Interval: {self.monitor_interval_minutes} minutes
  State File: {self.state_file}
  To Email: {self.to_email}
  From Email: {self.from_email}
  API Key: {'✅ Set' if self.resend_api_key else '❌ Missing'}
"""

if __name__ == "__main__":
    try:
        config = Config()
        print("✅ Configuration loaded successfully!")
        print(config)
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nExample .env file:")
        print("RESEND_API_KEY=your_resend_api_key_here")
        print("TO_EMAIL=your-email@example.com")
        print("FROM_EMAIL=noreply@yourdomain.com")