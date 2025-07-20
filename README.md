# Calendar Sync Tool

A Python application that automatically syncs events from an Outlook ICS calendar feed to Google Calendar using the Google Calendar API.

## Features

- ✅ Fetches events directly from Outlook ICS URL
- ✅ Parses ICS data and extracts event details (title, start, end, description, location)
- ✅ Adds new events to Google Calendar using OAuth2 authentication
- ✅ Prevents duplicate event creation by checking existing events
- ✅ Automated GitHub Actions workflow for scheduled syncing
- ✅ Comprehensive logging and error handling
- ✅ Modular and configurable code structure

## Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account
- GitHub account (for automated syncing)

## Setup Instructions

### 1. Google Calendar API Setup

#### Step 1: Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click on it and press "Enable"

#### Step 2: Create OAuth2 Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure the OAuth consent screen:
   - Choose "External" user type
   - Fill in the required fields (App name, User support email, Developer contact)
   - Add your email to test users
4. For Application type, choose "Desktop application"
5. Give it a name (e.g., "Calendar Sync Tool")
6. Click "Create"
7. Download the credentials JSON file

#### Step 3: Get Refresh Token

You need to obtain a refresh token for OAuth2 authentication. Here's a Python script to help you get it:

```python
# get_refresh_token.py
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_refresh_token():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    
    print(f"Refresh Token: {creds.refresh_token}")
    print(f"Client ID: {creds.client_id}")
    print(f"Client Secret: {creds.client_secret}")

if __name__ == '__main__':
    get_refresh_token()
```

Run this script after placing your `credentials.json` file in the same directory:

```bash
pip install google-auth-oauthlib
python get_refresh_token.py
```

### 2. Local Development Setup

#### Step 1: Clone and Install Dependencies

```bash
git clone <your-repo-url>
cd calendarSync
pip install -r requirements.txt
```

#### Step 2: Set Environment Variables

Create a `.env` file or set environment variables:

```bash
export GOOGLE_CLIENT_ID="your-client-id"
export GOOGLE_CLIENT_SECRET="your-client-secret"
export GOOGLE_REFRESH_TOKEN="your-refresh-token"
```

#### Step 3: Test the Sync

```bash
python sync.py
```

### 3. GitHub Actions Setup (Automated Syncing)

#### Step 1: Fork/Create Repository

1. Fork this repository or create a new one with these files
2. Push your code to GitHub

#### Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Navigate to "Settings" > "Secrets and variables" > "Actions"
3. Add the following repository secrets:
   - `GOOGLE_CLIENT_ID`: Your Google OAuth2 client ID
   - `GOOGLE_CLIENT_SECRET`: Your Google OAuth2 client secret
   - `GOOGLE_REFRESH_TOKEN`: Your Google OAuth2 refresh token

#### Step 3: Enable GitHub Actions

1. Go to the "Actions" tab in your repository
2. Enable workflows if prompted
3. The sync will now run automatically every 10 minutes between 6am-6pm on weekdays

#### Step 4: Manual Trigger (Optional)

You can manually trigger the sync:
1. Go to "Actions" tab
2. Select "Calendar Sync" workflow
3. Click "Run workflow"

## Configuration

### ICS URL

The Outlook ICS URL is hardcoded in `sync.py`. To change it, modify the `ICS_URL` variable in the `main()` function:

```python
ICS_URL = "your-outlook-ics-url-here"
```

### Schedule Customization

To modify the sync schedule, edit the cron expressions in `.github/workflows/sync.yml`:

```yaml
schedule:
  - cron: '*/10 13-23 * * 1-5'  # Every 10 minutes, 1-11 PM UTC, Mon-Fri
  - cron: '*/10 0-1 * * 2-6'    # Every 10 minutes, 12-1 AM UTC, Tue-Sat
```

### Calendar Selection

By default, events are added to your primary Google Calendar. To use a different calendar, modify the `calendar_id` in the `GoogleCalendarManager` class:

```python
self.calendar_id = 'your-calendar-id@gmail.com'  # Replace with specific calendar ID
```

## File Structure

```
calendarSync/
├── sync.py                    # Main synchronization script
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── .github/
│   └── workflows/
│       └── sync.yml          # GitHub Actions workflow
└── sync.log                  # Log file (created after first run)
```

## How It Works

1. **Fetch ICS Data**: Downloads the ICS calendar feed from the Outlook URL
2. **Parse Events**: Extracts event details (title, start/end times, description, location)
3. **Check Duplicates**: Compares with existing Google Calendar events to prevent duplicates
4. **Create Events**: Adds new events to Google Calendar using the API
5. **Logging**: Records all operations and errors for debugging

## Duplicate Prevention

The tool prevents duplicate events by comparing:
- Event title/summary
- Start time (with 1-minute tolerance for minor differences)

Events are considered duplicates if both the title and start time match existing Google Calendar events.

## Logging

- Console output shows sync progress and results
- Detailed logs are written to `sync.log`
- GitHub Actions uploads log files as artifacts for 7 days

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your Google OAuth2 credentials
   - Ensure the refresh token is valid and not expired
   - Check that the Google Calendar API is enabled

2. **ICS Fetch Errors**
   - Verify the ICS URL is accessible
   - Check network connectivity
   - Ensure the URL returns valid ICS data

3. **Permission Errors**
   - Verify OAuth2 scopes include calendar access
   - Check that your Google account has calendar permissions

### Debug Mode

To enable more detailed logging, modify the logging level in `sync.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Security Notes

- Never commit your OAuth2 credentials to version control
- Use GitHub Secrets for storing sensitive information
- Regularly rotate your OAuth2 refresh tokens
- Monitor your Google Cloud Console for unusual API usage

## Support

If you encounter issues:
1. Check the logs for error messages
2. Verify your setup against this README
3. Create an issue in the GitHub repository with:
   - Error messages
   - Steps to reproduce
   - Your environment details (Python version, OS, etc.)
