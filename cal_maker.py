#!/usr/bin/env python3
from urllib.parse import quote
import json
import ijson # should be able to read only the values you need
#import os

calendar_json = "calendars.json"

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

title=quote('Rome Physics Seminars (Theoretical Physics)')
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
