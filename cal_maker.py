#!/usr/bin/env python3
from urllib.parse import quote
import json
import ijson # should be able to read only the values you need
#import os
import argparse

'''
Output gives two outputs, one above and one below the \%\%\%\%\%\%\%\% (for best results is advisable to redirect its output to file to no mess up newlines, that is.
cal_maker.py > topaste. Then you can open `topaste` in a text editor and copy the text)
copy the output above the \%\%\%\%\% in the webpage editor. You have to edit the raw HTML and replace the old code for the calendar widget. Beware that the code you paste does not look like the one you are going to paste in, because google process what you paste and transforms it in the actual widget.
copy the output below the \%\%\%\%\% to redefine the cals_json array in the google script (you can find it from https://script.google.com/home/ pay attention that calendars ID must use @ and not \%40, cal_maker.py should make the change automatically but please check
'''


parser = argparse.ArgumentParser(description='Process a JSON file to produce a valid Google Calendar widget and AppScript variables for the automatic generation of a PDF calendar.', usage='Copy')


parser.add_argument('--file',
                    default='calendars.json',
                    help='the JSON file to process (default: calendars.json)')

parser.add_argument('--title',
                    default='Rome Physics Seminars (Theoretical Physics)',
                    help='The title displayed in the web page')

args = parser.parse_args()

#calendar_json = "calendars.json"
calendar_json=args.file
title=args.title

color_map={}
#
color_map['rm1']='BE6D00'
color_map['rm2']='528800'
color_map['rm3']='2952A3'
color_map['lnf']='AB8B00'

others=''
with open(calendar_json, 'r') as f:
    for line in f:
        if line[0] != '#':
            calendar_data = json.loads(line) #it is now a dictionary
            others+='src='+calendar_data['id']+'&amp;color=%23'+color_map[calendar_data['color']]+'&amp;'

#title=quote('Rome Physics Seminars (Theoretical Physics)')
#print(title)
#print('\n')

srcstring="https://calendar.google.com/calendar/embed?title="+title+"&amp;mode=AGENDA&amp;height=600&amp;wkst=2&amp;hl=en&amp;bgcolor=%23FFFFFF&amp;"+others+'ctz=Europe%2FRome"'

iframe='<iframe src="'+srcstring+' style="border-width:0" width="100%" height="600" frameborder="0" scrolling="no"></iframe>'

print(iframe)
print('%%%%%%% the part above must be pasted in the web page editor to make a calendar widget %%%%%%%%%')

print('%%%%%%% the part below must be pasted in the cals_json list in the script on google %%%%%%%%%')

with open(calendar_json, 'r') as f:
    for line in f:
        if line[0] != '#':
            _line= line.replace('%40', '@')
            print('cals_json.push(\''+_line.rstrip()+'\');')
