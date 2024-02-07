# This file collects responses from Goolge Forms, processes them
# and fills in the spreadsheet to the appropriate row.

import pygsheets
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pprint

# OUATH2 things for Gmail API
# Setup a list of strings that determines app permissions (scope). Here, we're just sending
SCOPES = ["https://www.googleapis.com/auth/drive"]
# Setup OAUTH2 flow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
# Build local web server to handle oauth2 flow and return oauth2 credentials
creds = flow.run_local_server(port=0)

# Build the Forms service
service_forms = build('forms', 'v1', credentials=creds)

# Connect to Google Sheets
client = pygsheets.authorize(service_account_file="automated-email-412501-1d063b0b2fe9.json")
sheet = client.open("email_automation_test") # file
wks = sheet.worksheet_by_title("ht_people") # tab

# Grab all the Form IDs
form_ids = wks.get_col(col=5, include_tailing_empty=False)
form_ids = [id for id in form_ids if id != ''][1:] # remove blanks and header
# print(form_ids) # sfsg

# pull form data
form_id = '187nghvg4PUI0U59lLpb8Y5u-uW7H1CS4yN1PjYIcDC8'
# grab the form questions and answer object
structure = service_forms.forms().get(formId=form_id).execute()
responses = service_forms.forms().responses().list(formId=form_id).execute()

# Grab the response from responses that has the most recent lastSubmittedTime
response = max(responses['responses'], key=lambda x: x['lastSubmittedTime'] )

# Collect question responses. **This section is tailor made to the specific
# set of questions and their structures in the template**

# Coffee, questionId = '2cb5a13a'
coffee = response['answers']['2cb5a13a']['textAnswers']['answers'][0]['value']
if coffee == 'Yes': coffee = 1 # binarize
else: coffee = 0

# Programming languages, questionId = '670b3b7b'
#   This returns a list of dicts, each with a single item, key is 'value', value is response: 
languages = response['answers']['670b3b7b']['textAnswers']['answers']
languages = [list(x.values())[0] for x in languages] # just the strings
#   We want binary values depending on the items in languages
langs_bin = [0,0,0,0,0] # (would be more dynamic to generate the len of this list based on corresponding structure object)
mapping = {'Javascript': 0, 'Python': 1, 'SQL': 2, 'C/C++': 3, 'R': 4}
for language in languages:
    index = mapping.get(language)
    if index is not None: # i.e. if it's present in languages, pull the index, switch to 1 
        langs_bin[index] = 1

#   book, questionId = '1cb3384f'  
book = response['answers']['1cb3384f']['textAnswers']['answers'][0]['value']

print(coffee, langs_bin, book)


# TODO - Line 32 is generating an empty dictionary-- investigate,
# run the id thru forms_api_quick.py, see if same problem, compare codes.

# TODO update the Sheets file with coffee, langs_bin, and book.
# Match to correct row with iteration's form_id.
# Probably want to use .find() + .update_values() from pygsheets   

