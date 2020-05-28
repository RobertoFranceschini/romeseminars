#!/usr/bin/env python3
from urllib.parse import quote
import urllib.request
import json
import ijson # should be able to read only the values you need
#import os
import argparse
from flask_table import Table, Col
import random
from termcolor import colored
import pandas as pd
import datetime

_usage='''
Read a JSON and extract the Indico address of the categories then obtain information for each listed calendar from the indico_http_api parser
'''


parser = argparse.ArgumentParser(description='Read an INDICO category and print a HTML table with the forthcoming events', usage=_usage)


parser.add_argument('--file',
                    default='',
                    help='the file with JSON data on the calendars (default: \'\'')


# parser.add_argument('--site',
#                     default='',
#                     help='the INDICO server to query (default: \'\'')
#
# parser.add_argument('--category',
#                     default='',
#                     help='The INDICO category to fecth')
#
#
# parser.add_argument('--full_url',
#                     default='',
#                     help='The full url of the category, e.g. https://indico.cern.ch/category/10236/')

parser.add_argument('--debug',
                    default=False,
                    help='Print debug info')


args = parser.parse_args()


calendar_json=args.file
debug=args.debug



def main():
    import indico_json

    with open(calendar_json, 'r') as f:
        lines = [line for line in f]

    seminar_series=[]
    #random.shuffle(lines)
    for line in lines:
        if line[0] != '#':
            calendar_data = json.loads(line) #it is now a dictionary
            if len(calendar_data["indico"])>0:
                print(colored( "Working on "+calendar_data["name"],'red') )
                _seminar_series=indico_json.indico_category_event_url_to_dict(fullurl=calendar_data["indico"],name=calendar_data["name"],debug=debug)#['--fullurl',calendar_data["indico"]])
                #print(_seminar_series)
                seminar_series+=_seminar_series

    df=pd.DataFrame(seminar_series)

    df['date']=pd.to_datetime(df['date'])

    future_seminars=df[df['date']>= pd.to_datetime('today').floor('D') ].sort_values(['date','time'])

    print( future_seminars )
    future_seminars.to_csv('future_seminars.csv')

if __name__ == "__main__":
    main()
