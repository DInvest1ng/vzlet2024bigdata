from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import datetime
import googleapiclient
from google.oauth2 import service_account
import google_auth_oauthlib.flow
import googleapiclient.discovery
import datetime
import pytz

import pandas as pd
import json

# If modifying these scopes, delete the file token.json.
SERVICE_ACCOUNT_FILE = 'D:/Python/vzlet2024bigdata/eternal-seeker-443011-s8-08f535cc64bd.json'

CREDENTIALS_FILE = 'D:/Python/vzlet2024bigdata/credentials.json'

# Области доступа
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Функция для аутентификации пользователя и получения токенов доступа
def authenticate_user():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return credentials

# Функция для получения ссылки на календарь пользователя
def get_calendar_id(credentials, calendar_name):
    print(credentials)
    service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
    calendar_list = service.calendarList().list().execute()
    for item in calendar_list['items']:
        if (item['summary'] == calendar_name):
            return item['id']

def save_tokens_to_excel(client_id, credentials, filename='D:/Python/vzlet2024bigdata/tokens.xlsx'):
    token_info = json.loads(credentials.to_json())
    file = pd.read_excel(filename)
    df = pd.DataFrame([token_info])
    print(google.oauth2.credentials.Credentials(**df.to_dict()))
    df['id'] = client_id
    file = pd.concat([file, df], ignore_index=True)
    file.to_excel(filename, index=False)

def load_tokens_from_excel(client_index, filename='D:/Python/vzlet2024bigdata/tokens.xlsx'):
    df = pd.read_excel(filename).iloc[client_index, 1:].to_dict()
    token_info = {}
    for item in df:
        token_info[item] = df[item][1]
    token_info['scopes'] = SCOPES
    token_info['account'] = ''
    #token_info['expiry'] = pd.to_datetime(token_info['expiry'])
    return google.oauth2.credentials.Credentials(**token_info)


class GoogleCalendar(object):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        self.service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)

    # создание словаря с информацией о событии
    def create_event_dict(self, name, discription, start_date, end_date):
        event = {
            'summary': name,
            'description': discription,
            'start': {
                'dateTime': start_date,
            },
            'end': {
                'dateTime': end_date,
            }
        }
        return event

    # создание события в календаре
    def create_event(self, event):
        e = self.service.events().insert(calendarId=calendar_id, body=event).execute()
        print('Event created: %s' % (e.get('id')))

    # вывод списка из десяти предстоящих событий
    def get_events_list(self):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = self.service.events().list(calendarId=calendar_id, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])


client_id = int(input())
filename = 'D:/Python/vzlet2024bigdata/tokens.xlsx'
df = pd.read_excel(filename)
if (df['id'] == client_id).any() == False:
    credentials = authenticate_user()
    save_tokens_to_excel(client_id, credentials)
    print(credentials)
client_index = df[df['id'] == client_id].index
credentials = load_tokens_from_excel(client_index, 'D:/Python/vzlet2024bigdata/tokens.xlsx')
calendar_id = str(get_calendar_id(credentials, 'test'))

calendar = GoogleCalendar()
test_name = 'popka'
test_date = datetime.datetime(2024, 12, 4, 18, 0, 0)
timezone = pytz.timezone('Europe/Moscow')
test_date = timezone.localize(test_date)
test_date = test_date.strftime('%Y-%m-%dT%H:%M:%S%z')
test_date = test_date[:-2] + ':' + test_date[-2:]
event = calendar.create_event_dict(test_name, 'aboba', test_date, test_date)
calendar.create_event(event)
calendar.get_events_list()
