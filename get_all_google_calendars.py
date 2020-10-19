"""
05-Oct-2017: Scratch script for blog post about Google Calendar API
This script is a sample and NOT indicative of Qxf2's programming habits.

This script will:
a) Connect to Google Calendar
b) Get calendar ids for all Qxf2 employees
c) Execute a search in a given hardcoded timeframe for all employees
d) List any event with the word PTO in the summary

To setup, I followed this reference:
https://developers.google.com/google-apps/calendar/quickstart/python

References:
1. https://developers.google.com/google-apps/calendar/quickstart/python
2. https://developers.google.com/google-apps/calendar/v3/reference/events/list
3. https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
"""


from __future__ import print_function
import httplib2
import os
from termcolor import colored

# from apiclient import discovery
# Commented above import statement and replaced it below because of
# reader Vishnukumar's comment
# Src: https://stackoverflow.com/a/30811628

import googleapiclient.discovery as discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = 'https://www.googleapis.com/auth/calendar.events.readonly'
CLIENT_SECRET_FILE = 'credentials.json'#'client_secret_google_calendar.json'
APPLICATION_NAME = 'Python Calendars'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_calendar_human_name(calendar_list_entry):
    try:
        _name=calendar_list_entry['summaryOverride']
    except KeyError:
        _name=calendar_list_entry['summary']
    return _name

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    print('credentials',credentials)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    # This code is to fetch the calendar ids shared with me
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list
    page_token = None
    calendar_ids = []
    encountered_calendars={}
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            #print(calendar_list_entry.items())
            _id=calendar_list_entry['id']
            _name=get_calendar_human_name(calendar_list_entry)
            if _name not in ['Compleanni','Festività in Italia']:
                print(_name, _id)
                calendar_ids.append(calendar_list_entry['id'])
                encountered_calendars[_id]=calendar_list_entry
        page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

    # This code is to look for all-day events in each calendar for the month of September
    # Src: https://developers.google.com/google-apps/calendar/v3/reference/events/list
    # You need to get this from command line
    # Bother about it later!
    start_date = datetime.datetime(
        2020, 10, 10, 00, 00, 00, 0).isoformat() + 'Z'
    end_date = datetime.datetime(2020, 10, 30, 23, 59, 59, 0).isoformat() + 'Z'

    for calendar_id in calendar_ids:
        count = 0
        print('\n','----',colored(
         get_calendar_human_name(encountered_calendars[calendar_id]),'red'))
        eventsResult = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            print('No upcoming events found.')
        for event in events:
            #print(event)
            if 'summary' in event:
                count += 1
                start = event['start'].get(
                        'dateTime', event['start'].get('date'))
                print(colored(start,'green'), event['summary'])


if __name__ == '__main__':
    main()
