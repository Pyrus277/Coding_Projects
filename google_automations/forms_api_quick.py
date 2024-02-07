# This is a program to quickly investiage an individual Google Form's metadata.

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# OUATH2 things for Gmail API
# Setup a list of strings that determines app permissions (scope). Here, we're just sending
SCOPES = ["https://www.googleapis.com/auth/drive"]
# Setup OAUTH2 flow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
# Build local web server to handle oauth2 flow and return oauth2 credentials
creds = flow.run_local_server(port=0)
# Build the Gmail service
service_forms = build('forms', 'v1', credentials=creds)

form_id = "1y3kFnsRD7ql_qNQfaYCvUDToZohrgFcgplzMFPOqzNg"
result = service_forms.forms().get(formId=form_id).execute()

print(result)

