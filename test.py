from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file

class CalendarApi:
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        # SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.creds = load_credentials_from_file(
          'credentials.json', SCOPES
        )[0]
        self.calenderId = "im2guap9ivnn1t2ace16av5qi8@group.calendar.google.com"

    def get(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        # Load credential file for service account
        service = build('calendar', 'v3', credentials=self.creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(
                calendarId=self.calenderId,
                timeMin=now,
                maxResults=100,
                singleEvents=True,
                orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])
        return events

    def insert(self, title, description_json, start, end):


if __name__ == '__main__':
    api = CalendarApi()
    api.get()
