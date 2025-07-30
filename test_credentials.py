#!/usr/bin/env python3
"""
Test script to verify Google Calendar API credentials are working.
Run this after setting up your environment variables.
"""

import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def test_credentials():
    """Test if Google Calendar API credentials are working"""
    
    print("Testing Google Calendar API Credentials")
    print("=" * 50)
    
    # Check environment variables
    client_id = os.getenv('GOOGLE_CLIENT_ID')
    client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
    refresh_token = os.getenv('GOOGLE_REFRESH_TOKEN')
    
    print("Environment Variables:")
    print(f"  GOOGLE_CLIENT_ID: {'✓ Set' if client_id else '✗ Missing'}")
    print(f"  GOOGLE_CLIENT_SECRET: {'✓ Set' if client_secret else '✗ Missing'}")
    print(f"  GOOGLE_REFRESH_TOKEN: {'✓ Set' if refresh_token else '✗ Missing'}")
    print()
    
    if not all([client_id, client_secret, refresh_token]):
        print("❌ Missing required environment variables!")
        print("Please set GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, and GOOGLE_REFRESH_TOKEN")
        print("Run: python get_refresh_token.py to get these values")
        return False
    
    try:
        # Create credentials
        print("Creating OAuth2 credentials...")
        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri='https://oauth2.googleapis.com/token',
            client_id=client_id,
            client_secret=client_secret
        )
        
        # Build service
        print("Building Google Calendar service...")
        service = build('calendar', 'v3', credentials=credentials)
        
        # Test API call - get calendar list
        print("Testing API access...")
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        print(f"✅ Success! Found {len(calendars)} calendars:")
        for calendar in calendars[:5]:  # Show first 5 calendars
            print(f"  - {calendar['summary']} ({calendar['id']})")
        
        if len(calendars) > 5:
            print(f"  ... and {len(calendars) - 5} more")
        
        print()
        print("🎉 Your Google Calendar API credentials are working correctly!")
        print("You can now run: python sync.py")
        
        return True
        
    except HttpError as e:
        print(f"❌ Google API Error: {e}")
        if e.resp.status == 401:
            print("This usually means your credentials are invalid or expired.")
            print("Try running: python get_refresh_token.py")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main entry point"""
    success = test_credentials()
    
    if not success:
        print("\n🔧 Next steps:")
        print("1. Follow the setup guide: cat setup_guide.md")
        print("2. Get credentials.json from Google Cloud Console")
        print("3. Run: python get_refresh_token.py")
        print("4. Set the environment variables")
        print("5. Run this test again: python test_credentials.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
