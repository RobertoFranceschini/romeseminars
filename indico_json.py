#!/usr/bin/env python3
from urllib.parse import quote
import urllib.request
import json
import ijson # should be able to read only the values you need
#import os
import argparse
from flask_table import Table, Col
import random

_usage='''
Read an Indico category and construct a Table for the HTML output of the forthcoming seminars.

Indico is queried through the HTTP API
https://docs.getindico.io/en/stable/http_api/access/#url-structure
and its JSON response
https://indico.cern.ch/export/categ/2387.json?from=-31d
https://indico.in2p3.fr/export/categ/870.json?from=-31d
https://indico.desy.de/indico/export/categ/266.json?from=-7d
is manipulated.
'''


# parser = argparse.ArgumentParser(description='Read an INDICO category and print a HTML table with the forthcoming events', usage=_usage)
#
# # parser.add_argument('--file',
# #                     default='',
# #                     help='the INDICO server to query (default: \'\'')
#
#
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
#
#
# parser.add_argument('--debug',
#                     default=False,
#                     help='Print debug info')
#
#
# args = parser.parse_args()
#
#
# site=args.site
# category=args.category
# fullurl=args.full_url
# debug=args.debug
#
# color_map={}
# #
# color_map['rm1']='BE6D00'
# color_map['rm2']='528800'
# color_map['rm3']='2952A3'
# color_map['lnf']='AB8B00'


def indico_category_event_url_to_dict(json_url=None,site=None,category=None,event=None,fullurl=None,debug=False,name=None):
    categ_event=''

    #deal with the case a full URL is passed
    if len(fullurl)>0:
        if debug:
            print(fullurl.split("/"))
        site=fullurl.split("/")[:-3]

        if "category" in fullurl:
            category=fullurl.split("/")[-2]
            categ_event="categ"
            id=category
            if debug:
                print("the full URL belongs to a category:",id)
        if "event" in fullurl:
            event=fullurl.split("/")[-2]
            categ_event="event"
            id=event
            if debug:
                print("the full URL belongs to an event:",id)

        if debug:
            print("/".join(site))
        if debug:
            print(category)
            print(event)

    #deal with the case a category ID is passed
    if category is not None:
        categ_event="categ"
        id=category

    #deal with the case an event ID is passed
    if event is not  None:
        categ_event="event"
        id=event

    # reconstruct the URL of the JSON of the requested resource
    json_url="/".join(site)+"/export/"+categ_event+"/"+id+".json"
    if event is not None:
        json_url=json_url+"?detail=contributions&"
    json_url+="?from=-7d&?to=+365d&?order=start"
    print("Fetching:",json_url)

    # RESULTS
    print('Results:')
    results=[]
    with urllib.request.urlopen(json_url) as url:
        data = json.loads(url.read().decode())
        if debug:
            print(type(data["results"]))

        if categ_event=="categ":
            container = data["results"]
            if debug:
                print( 'searching in data["results"] as it is a category')

        if categ_event=="event":
            if debug:
                print( 'searching in data["results"] as it is an event')
                print(type(data["results"] ) )
                print( data["results"] )
            container = data["results"][0]["contributions"]
        for seminar in container:
            _seminar={}
            print('-------------------------------------')
            print(seminar["title"],' from ',seminar['startDate']['date'],seminar['startDate']['time'],' to ',seminar['endDate']['time'],seminar['startDate']['tz'],\
            #seminar['description']
            )


            # GUESS THE SPEAKERS
            guessed_speaker=None

            def guess_speaker_from_indico(seminar):
                guessed_speaker=None

                def get_name(seminar):
                    for chair in seminar:#["chairs"]:
                        try:
                            print('guessed speaker from Indico:',chair['first_name'],chair["last_name"])
                            guessed_speaker=chair['first_name']+" "+chair["last_name"]
                            return guessed_speaker
                        except KeyError:
                            try:
                                guessed_speaker=chair['fullName']
                                return guessed_speaker
                            except KeyError:
                                guess_speaker='Unknown speaker'

                if "speakers" in seminar:
                    if len(seminar["speakers"])>0:
                        guessed_speaker=get_name(seminar["speakers"])
                        return guessed_speaker
                if "chairs" in seminar:
                    if len(seminar["chairs"])>0:
                        guessed_speaker=get_name(seminar["chairs"])
                        return guessed_speaker

            def guess_speaker_from_title_string(seminar,_divider=':'):
                if len(seminar["title"].split(_divider)) > 1:
                    print("guessed speaker from title:", seminar["title"].split(_divider)[0])
                    guessed_speaker=seminar["title"].split(_divider)[0]
                    return guessed_speaker
                return None

            def guess_speaker_from_description_string(seminar,_divider='peaker:'):
                split_by=seminar["description"].split(_divider)

                if len( split_by ) > 1:

                    first_last_remove_dot=" ".join(split_by[1].split(" ")[:3]).split('.')[0]
                    print("guessed speaker from description:", first_last_remove_dot )
                    guessed_speaker=first_last_remove_dot

                    return guessed_speaker
                return None


            if guessed_speaker is None:
                guessed_speaker=guess_speaker_from_indico(seminar)


            dividers=[':','-']
            for divider in dividers:
                if guessed_speaker is None:
                    guessed_speaker=guess_speaker_from_title_string(seminar,_divider=divider)

            if guessed_speaker is None:
                guessed_speaker=guess_speaker_from_description_string(seminar)

            _seminar["speaker"]=guessed_speaker
            _seminar["title"]=seminar["title"]
            _seminar["date"]=seminar['startDate']['date']
            _seminar["time"]=seminar['startDate']['time']
            _seminar["endtime"]=seminar['endDate']['time']
            _seminar["timezone"]=seminar['startDate']['tz']
            _seminar["link"]=fullurl
            _seminar["name"]=name
            # print(_seminar)
            results+=[_seminar]
    print('-------------------------------------')
    return results



if __name__ == "__main__":
    indico_url_to_dict()
