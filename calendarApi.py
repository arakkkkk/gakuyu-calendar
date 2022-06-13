import re
import json
import datetime
from google.auth import load_credentials_from_file
from googleapiclient.discovery import build
import calendarData

class CalendarApi():
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.load(f)
            self.__calendarId = config.get('id')

        # Preparation for Google API
        SCOPES = [config.get('calendar')]
        gapi_creds = load_credentials_from_file('credentials.json', SCOPES)[0]
        self.__service = build('calendar', 'v3', credentials=gapi_creds)

    @property
    def calendarUrl(self):
        return self.__calendarUrl

    @property
    def calendarId(self):
        return self.__calendarId

    @property
    def service(self):
        return self.__service

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, val):
        self.__body = val

    @property
    def eventId(self):
        return self.__eventId

    @eventId.setter
    def eventId(self, val):
        self.__eventId = val

    def get(self):
        results = []
        now = datetime.datetime.now(datetime.timezone.utc)

        nextWeek = now + datetime.timedelta(days=7)
        timeMax = datetime.datetime(nextWeek.year, nextWeek.month, nextWeek.day, 23, 59, tzinfo=datetime.timezone.utc)

        events_result = self.service.events().list(
            calendarId="im2guap9ivnn1t2ace16av5qi8@group.calendar.google.com", 
            timeMin=now.isoformat(),
            timeMax=timeMax.isoformat(),
            maxResults=1,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return events

    def insert(self, body):
        result = self.service.events().insert(calendarId=self.calendarId, body=body).execute()
        return result

    def delete(self, eventId):
        result = self.service.events().delete(calendarId=self.calendarId, eventId=eventId).execute()
        return result
