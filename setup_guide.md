# Quick Setup Guide for Calendar Sync Tool

## Current Issue
Your calendar sync tool is missing Google OAuth2 credentials. You need to set up these environment variables:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET` 
- `GOOGLE_REFRESH_TOKEN`

## Step-by-Step Fix

### 1. Get Google Cloud Credentials

1. **Go to Google Cloud Console**: https://console.cloud.google.com/
2. **Create/Select Project**: Create a new project or select existing one
3. **Enable Google Calendar API**:
   - Go to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click it and press "Enable"

4. **Create OAuth2 Credentials**:
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - If prompted, configure OAuth consent screen:
     - Choose "External" user type
     - Fill required fields (App name, support email)
     - Add your email to test users
   - Choose "Desktop application" as application type
   - Name it "Calendar Sync Tool"
   - Click "Create"
   - **Download the JSON file** and save it as `credentials.json` in this directory

### 2. Generate Refresh Token

Once you have `credentials.json`, run:

```bash
python get_refresh_token.py
```

This will:
- Open your browser for Google authentication
- Generate the required OAuth2 credentials
- Display the CLIENT_ID, CLIENT_SECRET, and REFRESH_TOKEN

### 3. Set Environment Variables

Copy the values from step 2 and set them as environment variables:

**Option A: Temporary (current session only)**
```bash
export GOOGLE_CLIENT_ID="your-client-id-here"
export GOOGLE_CLIENT_SECRET="your-client-secret-here"
export GOOGLE_REFRESH_TOKEN="your-refresh-token-here"
```

**Option B: Permanent (add to ~/.zshrc or ~/.bash_profile)**
```bash
echo 'export GOOGLE_CLIENT_ID="your-client-id-here"' >> ~/.zshrc
echo 'export GOOGLE_CLIENT_SECRET="your-client-secret-here"' >> ~/.zshrc
echo 'export GOOGLE_REFRESH_TOKEN="your-refresh-token-here"' >> ~/.zshrc
source ~/.zshrc
```

**Option C: Create .env file (if you modify the code to load it)**
```bash
GOOGLE_CLIENT_ID=your-client-id-here
GOOGLE_CLIENT_SECRET=your-client-secret-here
GOOGLE_REFRESH_TOKEN=your-refresh-token-here
```

### 4. Test the Setup

Run the sync tool:
```bash
python sync.py
```

You should see:
- ✓ Set for all Google credentials
- Successful authentication message
- Calendar sync process running

## Quick Commands Summary

```bash
# 1. Install dependencies (already done)
pip install -r requirements.txt

# 2. After getting credentials.json, generate tokens
python get_refresh_token.py

# 3. Set environment variables (use values from step 2)
export GOOGLE_CLIENT_ID="..."
export GOOGLE_CLIENT_SECRET="..."
export GOOGLE_REFRESH_TOKEN="..."

# 4. Test the sync
python sync.py
```

## Need Help?

If you get stuck:
1. Make sure you've enabled the Google Calendar API
2. Ensure `credentials.json` is in the calSyncTool directory
3. Check that environment variables are set: `echo $GOOGLE_CLIENT_ID`
4. Verify your Google account has calendar access permissions
