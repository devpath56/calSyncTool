#!/usr/bin/env python3
"""
Calendar Sync Tool
Syncs events from Outlook ICS feed to Google Calendar
"""

import os
import sys
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Optional
import requests
from google.oauth2.credentials import Credentials
from icalendar import Calendar, Event as ICalEvent
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from config import Config
from config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(Config.LOG_FILE)
    ]
)
logger = logging.getLogger(__name__)

class CalendarSyncError(Exception):
    """Custom exception for calendar sync errors"""
    pass

class OutlookICSFetcher:
    """Handles fetching and parsing ICS data from Outlook"""
    
    def __init__(self, ics_url: str):
        self.ics_url = ics_url
    
    def fetch_ics_data(self) -> str:
        """Fetch ICS data from the URL"""
        try:
            logger.info(f"Fetching ICS data from {self.ics_url}")
            response = requests.get(self.ics_url, timeout=Config.REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise CalendarSyncError(f"Failed to fetch ICS data: {e}")
    
    def parse_events(self, ics_data: str) -> List[Dict]:
        """Parse ICS data and extract event details"""
        try:
            calendar = Calendar.from_ical(ics_data)
            events = []
            
            for component in calendar.walk():
                if component.name == "VEVENT":
                    event = self._extract_event_details(component)
                    if event:
                        events.append(event)
            
            logger.info(f"Parsed {len(events)} events from ICS data")
            return events
        except Exception as e:
            raise CalendarSyncError(f"Failed to parse ICS data: {e}")
    
    def _extract_event_details(self, vevent: ICalEvent) -> Optional[Dict]:
        """Extract event details from a VEVENT component"""
        try:
            # Extract basic event information
            summary = str(vevent.get('summary', ''))
            description = str(vevent.get('description', ''))
            location = str(vevent.get('location', ''))
            
            # Handle start and end times
            dtstart = vevent.get('dtstart')
            dtend = vevent.get('dtend')
            
            if not dtstart or not dtend:
                logger.warning(f"Event missing start/end time: {summary}")
                return None
            
            # Convert to datetime objects
            start_dt = dtstart.dt
            end_dt = dtend.dt
            
            # Ensure timezone awareness
            if hasattr(start_dt, 'tzinfo') and start_dt.tzinfo is None:
                start_dt = start_dt.replace(tzinfo=timezone.utc)
            if hasattr(end_dt, 'tzinfo') and end_dt.tzinfo is None:
                end_dt = end_dt.replace(tzinfo=timezone.utc)
            
            # Get UID for duplicate checking
            uid = str(vevent.get('uid', ''))
            
            return {
                'summary': summary,
                'description': description,
                'location': location,
                'start': start_dt,
                'end': end_dt,
                'uid': uid
            }
        except Exception as e:
            logger.error(f"Error extracting event details: {e}")
            return None

class GoogleCalendarManager:
    """Handles Google Calendar API operations"""
    
    def __init__(self):
        self.service = self._build_service()
        self.calendar_id = Config.GOOGLE_CALENDAR_ID
    
    def _build_service(self):
        """Build Google Calendar service using OAuth2 credentials"""
        try:
            # Validate configuration
            if not Config.validate():
                raise CalendarSyncError("Invalid configuration")
            
            # Create credentials object
            credentials = Credentials(
                token=None,
                refresh_token=Config.GOOGLE_REFRESH_TOKEN,
                token_uri='https://oauth2.googleapis.com/token',
                client_id=Config.GOOGLE_CLIENT_ID,
                client_secret=Config.GOOGLE_CLIENT_SECRET
            )
            
            # Build and return the service
            service = build('calendar', 'v3', credentials=credentials)
            logger.info("Successfully authenticated with Google Calendar API")
            return service
            
        except Exception as e:
            raise CalendarSyncError(f"Failed to authenticate with Google Calendar: {e}")
    
    def get_existing_events(self, time_min: datetime, time_max: datetime) -> List[Dict]:
        """Get existing events from Google Calendar within a time range"""
        try:
            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=time_min.isoformat(),
                timeMax=time_max.isoformat(),
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            
            events = events_result.get('items', [])
            logger.info(f"Retrieved {len(events)} existing events from Google Calendar")
            return events
            
        except HttpError as e:
            raise CalendarSyncError(f"Failed to retrieve existing events: {e}")
    
    def event_exists(self, event: Dict, existing_events: List[Dict]) -> bool:
        """Check if an event already exists in Google Calendar"""
        event_summary = event['summary']
        event_start = event['start']
        
        for existing_event in existing_events:
            existing_summary = existing_event.get('summary', '')
            existing_start_str = existing_event.get('start', {}).get('dateTime', '')
            
            if not existing_start_str:
                continue
            
            try:
                # Parse existing event start time
                existing_start = datetime.fromisoformat(existing_start_str.replace('Z', '+00:00'))
                
                # Check if summary and start time match
                if (event_summary == existing_summary and 
                    abs((event_start - existing_start).total_seconds()) < Config.DUPLICATE_CHECK_TOLERANCE_SECONDS):
                    return True
            except Exception as e:
                logger.warning(f"Error comparing event times: {e}")
                continue
        
        return False
    
    def create_event(self, event: Dict) -> bool:
        """Create a new event in Google Calendar"""
        try:
            # Format event for Google Calendar API
            google_event = {
                'summary': event['summary'],
                'description': event['description'],
                'location': event['location'],
                'start': {
                    'dateTime': event['start'].isoformat(),
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': event['end'].isoformat(),
                    'timeZone': 'UTC',
                }
            }
            
            # Create the event
            created_event = self.service.events().insert(
                calendarId=self.calendar_id,
                body=google_event
            ).execute()
            
            logger.info(f"Created event: {event['summary']} at {event['start']}")
            return True
            
        except HttpError as e:
            logger.error(f"Failed to create event '{event['summary']}': {e}")
            return False

class CalendarSync:
    """Main calendar synchronization class"""
    
    def __init__(self, ics_url: str = None):
        self.ics_fetcher = OutlookICSFetcher(ics_url or Config.ICS_URL)
        self.google_calendar = GoogleCalendarManager()
    
    def sync(self) -> Dict[str, int]:
        """Perform the calendar synchronization"""
        try:
            logger.info("Starting calendar synchronization")
            
            # Fetch and parse ICS data
            ics_data = self.ics_fetcher.fetch_ics_data()
            outlook_events = self.ics_fetcher.parse_events(ics_data)
            
            if not outlook_events:
                logger.info("No events found in ICS feed")
                return {'processed': 0, 'created': 0, 'skipped': 0}
            
            # Get time range for existing events
            now = datetime.now(timezone.utc)
            time_min = now - timedelta(days=Config.SYNC_DAYS_BACK)
            time_max = now + timedelta(days=Config.SYNC_DAYS_FORWARD)
            
            # Get existing Google Calendar events
            existing_events = self.google_calendar.get_existing_events(time_min, time_max)
            
            # Process each Outlook event
            stats = {'processed': 0, 'created': 0, 'skipped': 0}
            
            for event in outlook_events:
                stats['processed'] += 1
                
                # Check if event already exists
                if self.google_calendar.event_exists(event, existing_events):
                    logger.info(f"Event already exists, skipping: {event['summary']}")
                    stats['skipped'] += 1
                    continue
                
                # Create new event
                if self.google_calendar.create_event(event):
                    stats['created'] += 1
                else:
                    logger.error(f"Failed to create event: {event['summary']}")
            
            logger.info(f"Sync completed. Processed: {stats['processed']}, "
                       f"Created: {stats['created']}, Skipped: {stats['skipped']}")
            
            return stats
            
        except Exception as e:
            logger.error(f"Calendar sync failed: {e}")
            raise

def main():
    """Main entry point"""
    try:
        # Print configuration for debugging
        Config.print_config()
        print()
        
        # Initialize and run sync
        sync = CalendarSync()
        stats = sync.sync()
        
        print(f"Calendar sync completed successfully!")
        print(f"Events processed: {stats['processed']}")
        print(f"Events created: {stats['created']}")
        print(f"Events skipped: {stats['skipped']}")
        
    except CalendarSyncError as e:
        logger.error(f"Sync error: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
