#!/usr/bin/env python3
"""
Configuration settings for the Calendar Sync Tool
"""

import os
from typing import Optional

class Config:
    """Configuration class for calendar sync settings"""
    
    # Outlook ICS URL (can be overridden via environment variable)
    ICS_URL = os.getenv(
        'OUTLOOK_ICS_URL',
        'https://outlook.office365.com/owa/calendar/e7563bb4bc2f4976a6955567aa926d05@bolo.ai/4bab9c42ea854b718a456d1af5aadb499351152313796004667/calendar.ics'
    )

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    GOOGLE_REFRESH_TOKEN = os.getenv("GOOGLE_REFRESH_TOKEN")

    # Optional: Use a specific Google Calendar (default is 'primary')
    GOOGLE_CALENDAR_ID="learn4lyfpathak@gmail.com"

    # Optional: Sync configuration
    DUPLICATE_CHECK_TOLERANCE_SECONDS=60
    SYNC_DAYS_BACK=30
    SYNC_DAYS_FORWARD=365
    REQUEST_TIMEOUT=30
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_FILE = os.getenv('LOG_FILE', 'sync.log')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required configuration is present"""
        required_vars = [
            'GOOGLE_CLIENT_ID',
            'GOOGLE_CLIENT_SECRET', 
            'GOOGLE_REFRESH_TOKEN'
        ]
        
        missing_vars = []
        for var in required_vars:
            if not getattr(cls, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"Missing required environment variables: {', '.join(missing_vars)}")
            return False
        
        return True
    
    @classmethod
    def print_config(cls) -> None:
        """Print current configuration (excluding sensitive data)"""
        print("Current Configuration:")
        print(f"  ICS URL: {cls.ICS_URL[:50]}...")
        print(f"  Google Calendar ID: {cls.GOOGLE_CALENDAR_ID}")
        print(f"  Duplicate Check Tolerance: {cls.DUPLICATE_CHECK_TOLERANCE_SECONDS}s")
        print(f"  Sync Range: {cls.SYNC_DAYS_BACK} days back, {cls.SYNC_DAYS_FORWARD} days forward")
        print(f"  Request Timeout: {cls.REQUEST_TIMEOUT}s")
        print(f"  Log Level: {cls.LOG_LEVEL}")
        print(f"  Log File: {cls.LOG_FILE}")
        print(f"  Google Client ID: {'✓ Set' if cls.GOOGLE_CLIENT_ID else '✗ Missing'}")
        print(f"  Google Client Secret: {'✓ Set' if cls.GOOGLE_CLIENT_SECRET else '✗ Missing'}")
        print(f"  Google Refresh Token: {'✓ Set' if cls.GOOGLE_REFRESH_TOKEN else '✗ Missing'}")
