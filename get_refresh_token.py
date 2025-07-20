#!/usr/bin/env python3
"""
Helper script to obtain Google OAuth2 refresh token for calendar sync.
Run this script once to get the refresh token needed for authentication.
"""

import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes required for Google Calendar access
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_refresh_token():
    """
    Get refresh token for Google Calendar API access.
    Requires credentials.json file downloaded from Google Cloud Console.
    """
    
    # Check if credentials.json exists
    if not os.path.exists('credentials.json'):
        print("Error: credentials.json file not found!")
        print("\nPlease follow these steps:")
        print("1. Go to Google Cloud Console (https://console.cloud.google.com/)")
        print("2. Create a project and enable Google Calendar API")
        print("3. Go to 'APIs & Services' > 'Credentials'")
        print("4. Create OAuth2 credentials (Desktop application)")
        print("5. Download the credentials JSON file and save it as 'credentials.json'")
        print("6. Run this script again")
        sys.exit(1)
    
    try:
        # Create the flow using the client secrets file
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        
        # Run the OAuth flow
        print("Opening browser for Google OAuth authentication...")
        print("Please authorize the application in your browser.")
        
        creds = flow.run_local_server(port=0)
        
        # Display the credentials
        print("\n" + "="*60)
        print("SUCCESS! Here are your OAuth2 credentials:")
        print("="*60)
        print(f"Client ID: {creds.client_id}")
        print(f"Client Secret: {creds.client_secret}")
        print(f"Refresh Token: {creds.refresh_token}")
        print("="*60)
        
        print("\nNext steps:")
        print("1. Copy these values to your environment variables or GitHub Secrets:")
        print("   - GOOGLE_CLIENT_ID")
        print("   - GOOGLE_CLIENT_SECRET") 
        print("   - GOOGLE_REFRESH_TOKEN")
        print("\n2. For local development, you can set them like this:")
        print(f'   export GOOGLE_CLIENT_ID="{creds.client_id}"')
        print(f'   export GOOGLE_CLIENT_SECRET="{creds.client_secret}"')
        print(f'   export GOOGLE_REFRESH_TOKEN="{creds.refresh_token}"')
        
        print("\n3. For GitHub Actions, add them as repository secrets in:")
        print("   Settings > Secrets and variables > Actions")
        
        return True
        
    except Exception as e:
        print(f"Error during OAuth flow: {e}")
        return False

def main():
    """Main entry point"""
    print("Google Calendar OAuth2 Refresh Token Generator")
    print("=" * 50)
    
    # Check if required packages are installed
    try:
        import google_auth_oauthlib
    except ImportError:
        print("Error: Required package not installed!")
        print("Please install it with: pip install google-auth-oauthlib")
        sys.exit(1)
    
    # Get the refresh token
    success = get_refresh_token()
    
    if success:
        print("\n✅ Refresh token generated successfully!")
        print("You can now run the calendar sync with: python sync.py")
    else:
        print("\n❌ Failed to generate refresh token.")
        print("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
