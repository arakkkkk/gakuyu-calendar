from __future__ import print_function
from datetime import datetime, timezone, timedelta
import os.path
from googleapiclient.discovery import build
from google.auth import load_credentials_from_file
import json

def createInsertData(title, description, start, end):
    body = {
        'summary':title,
        'description': json.dumps(description, indent=2, ensure_ascii=False),
        'start':{
            'dateTime': start,
            'timeZone': 'Japan'
        },
        'end': {
            'dateTime': end,
            'timeZone': 'Japan'
        },
    }
    return body

class CalendarApi:
    def __init__(self):
        # If modifying these scopes, delete the file token.json.
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        # SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        self.creds = load_credentials_from_file(
          'api/credentials.json', SCOPES
        )[0]
        self.calenderId = "im2guap9ivnn1t2ace16av5qi8@group.calendar.google.com"
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get(self, start, end):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        # Call the Calendar API
        now = datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = self.service.events().list(
                calendarId=self.calenderId,
                timeMin=start+"Z",
                timeMax=end+"Z",
                timeZone="Asia/Tokyo",
                maxResults=999,
                singleEvents=True,
                orderBy='startTime').execute()
        events = events_result.get('items', [])

        for i, event in enumerate(events):
            events[i]["created"] = datetime.strptime(event["created"], '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(hours=+9)
            events[i]["created"] = event["created"].strftime('%Y/%m/%d %H:%M')
            events[i]["start"]["dateTime"] = datetime.strptime(event["start"]["dateTime"], '%Y-%m-%dT%H:%M:%S+09:00')
            events[i]["start"]["dateTime"] = event["start"]["dateTime"].strftime('%Y/%m/%d %H:%M')
            events[i]["end"]["dateTime"] = datetime.strptime(event["end"]["dateTime"], '%Y-%m-%dT%H:%M:%S+09:00')
            events[i]["end"]["dateTime"] = event["end"]["dateTime"].strftime('%Y/%m/%d %H:%M')
            events[i]["description"] = json.loads(event["description"])
                
        return events

    def insert(self, title, description_json, start, end):
        body = createInsertData(
                title=title,
                description = description_json,
                start=start,
                end=end
                )
        print(body)
        events_result = self.service.events().insert(
                calendarId=self.calenderId,
                body=body).execute()

    def delete(self, event_id):
        result = self.service.events().delete(
                calendarId=self.calenderId, eventId=event_id
                ).execute()
        return result

    def update(self, event_id, update_json):
        event = self.service.events().get(
                calendarId=self.calenderId,
                eventId=event_id).execute()
        for key, val in update_json.items():
            desc_json = json.loads(event["description"])
            desc_json[key] = val
        event["description"] = json.dumps(desc_json, indent=2, ensure_ascii=False)
        response = self.service.events().update(
                calendarId=self.calenderId,
                eventId=event_id,
                body=event).execute()
        return response


if __name__ == '__main__':
    api = CalendarApi()
    # api.get()
    api.insert(
            "test1",
            "aaaaaaaaa",
            datetime.now().isoformat(),
            datetime.now().isoformat()
            )
