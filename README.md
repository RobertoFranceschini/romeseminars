# romeseminars

- paste the output of the python executable in the HTML of the webpage.
- pay attention to spurious new lines introduced by cut-paste


## To Add a calendar

- subscribe to this calendar using the "Add Calendar" function in Google calendar (if it is a iCal calendar from a URL use "import URL"; this is how INDICO calendars can be imported)
- read the CalendarID in the settings page of the created calendars
- create an appropriate JSON entry in the json file
- run cal_maker.py, which gives two outputs, one above and one below the %%%%%%%% (for best results is advisable to redirect its output to file to no mess up newlines, that is ./cal_maker.py > topaste. Then you can open topaste in a text editor and copy the text)
- copy the output above the %%%%% in the webpage editor. You have to edit the raw HTML and replace the old code for the calendar widget. Beware that the code you paste does not look like the one you are going to paste in, because google process what you paste and transforms it in the actual widget.
- copy the output below  the %%%%%  to redefine the cals_json array in the google script (you can find it from https://script.google.com/home/ pay attention that calendars ID must use @ and not %40, cal_maker.py should make the change automatically but please check )
