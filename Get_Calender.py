from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import auth_info
import pickle, os.path, datetime
from datetime import timedelta

scope = ['https://www.googleapis.com/auth/calendar.readonly']


def prompt_login():
    creds = None
    # The file token.pickle stores the  user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret.json', scope)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    service = build('calendar', 'v3', credentials=creds)
    return service


def get_calender_events(service):
    event_dict = {}
    now = datetime.datetime.utcnow()
    now = now.replace(hour=0, minute=0, second=0)
    tmr = now + timedelta(days=50)
    now = now.isoformat() + 'Z'  # 'Z' indicates UTC time
    tmr = tmr.isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Gathering your events...')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          timeMax=tmr,
                                          maxResults=1000, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'), )
        event_dict[event['summary']] = start
    return event_dict
