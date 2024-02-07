# This script accesses a Google Sheets file, goes down the rows,
# and for each with the "email" contact type, generates a Forms survey, 
# a personalized email with a link to the form, and updates the sheets file
# with details on what was done, also linking the Form on the approprate row.

import pygsheets
import time
from datetime import date 
import base64
from requests import HTTPError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def generate_form(origin_file_id, place_id, recip_name):
    """
    This function copies an existing Google Form file (a template),
    updates the copied form name, and updates the form's header text
    to be personalized to the recipient.
    
    origin_file_id: string, the id of the base template Form we want to use. Operations
        here will take place in the directory where this file exists. 
    place_id: string, unique identifier of the business represented by the recipient
    recip_name: string, the name of the recipient
    """
    try:
        # Copy the base file
        results = service_drive.files().copy(fileId=origin_file_id).execute()
        print(f'file that was copied: {results}\n') # output details
        # Update the form name
        #   get the file
        new_file_id = results['id']
        file = service_drive.files().get(fileId=new_file_id, fields='name').execute()
        #   Update metadata
        file['name'] = f'HT test form, ID: {str(place_id)}'
        #   Send request to API using update method
        updated_file = service_drive.files().update(
            fileId=new_file_id,
            body = file).execute()  
        
        # Call forms metadata to return the responder link (returned below) and other itmes:
        form = service_forms.forms().get(formId=new_file_id).execute()
        print(f"File {form['formId']} renamed successfully to {form['info']['title']}.\n") 
    except HTTPError as error:
        print(f'An error occurred: {error}\n')
        
    # Update the form body
    #     Write out the specific updates in JSON
    update = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "title": f"HT Test form, ID {place_id}",
                        "description": (
                            f"This is a survey for {recip_name}, ID {place_id}."
                        )
                    },
                    "updateMask": "description,title",
                }
            }
        ]
    }
    #     Apply the change to the newly generated form
    new_file_id = results['id']
    applied_updates = (
        service_forms.forms()
        .batchUpdate(formId=new_file_id, body=update)
        .execute()
    )

    return [form['responderUri'], form['formId']]

def send_email(recip_email, place_id, recip_name, form_url):
    '''
    Sends off an email using the Gmail API. 
    recip_email - a valid email string,
    place_id, recip_name - details for personalizing the emails. 
    '''
    # Construct the actual email  
    #     attach an image
    with open('ht_logo.jpg', 'rb') as fhand:
        image_part = MIMEImage(fhand.read())
    #     build out the rest of the email details
    message = MIMEMultipart() # multipart to have both text and image
    message['subject'] = 'HollowTree email automation test'
    message['to'] = recip_email
    body = f"""
    <html>
      <body>
      <p>Hello!</p>
      <p>Here's another automated test email. We're playing with different data gather concepts, so bear with us.</p>
      
      <p>Your <b>name</b> is <b>{recip_name}</b>, and your fake <b>place_id</b> is: <b>{place_id}</b></p>
      
      <p>This time, in addition to activity auto-logged in the Sheets file, a personalized Google Form is generated:</p>
      <p>{form_url}</p>
      <p>Please take ~15s to fill it out so I can see if the responses are landing correctly, or if we get any strange hiccups.</p>

      <p>Thanks!</p>

      <p>Perry</p>

      </body>
    </html>    
    """
    text_part = MIMEText(body, 'html')
    message.attach(text_part)
    message.attach(image_part)
    
    # Encode our message as base64
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    # Send out the email with send() method and set up error catching
    try:
        message = (service_gmail.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}\n')
    except HTTPError as error:
        print(f'An error occurred: {error}\n')
        message = None

# Do the things!:
if __name__ == "__main__":
    # OUATH2 things for Gmail API
    # Setup a list of strings that determines app permissions (scope). Here, we're just sending
    SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/drive"]
    # Setup OAUTH2 flow
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    # Build local web server to handle oauth2 flow and return oauth2 credentials
    creds = flow.run_local_server(port=0)
    # Build the Google services
    service_gmail = build('gmail', 'v1', credentials=creds) # this gonna trigger a browser window, click thru
    service_drive = build('drive', 'v3', credentials=creds)
    service_forms = build('forms', 'v1', credentials=creds)
    
    # Connect to Google sheets
    client = pygsheets.authorize(service_account_file="automated-email-412501-1d063b0b2fe9.json")
    sheet = client.open("email_automation_test") # file
    wks = sheet.worksheet_by_title("ht_people") # tab
    # Pull Sheets data
    rownum = 2 # first row of data; skip col headers
    row = wks.get_row(rownum, include_tailing_empty=False) # python list
    
    origin_file_id = "17PHV9vRT_NOdoNl2sb1J_q_lyR9sFgPDzRuSwZSZfSE" # Forms survey template id
    
    while row:
        if row[7] == 'email':
            # Generate and personalize a new survey
            new_file_id = generate_form(origin_file_id, row[9], row[10])
            form_url = new_file_id[0]
            form_id = new_file_id[1]  
            # Send out automated email
            send_email(row[6], row[9], row[10], form_url)
            
            # Update status cells in the sheet
            wks.update_values( ("A"+str(rownum)+":"+"E"+str(rownum)) ,[
                ["sent automated email", # most recent status update
                 str(date.today()), # YYY-mm-dd of this correspondence
                 int(row[2]) + 1, # Increment count of reach-outs
                 form_url, # link to Form
                 form_id
                ]
            ])

        # prep the next iteration
        rownum += 1
        row = wks.get_row(rownum, include_tailing_empty=False)
        
        # sleepy time--not sure if necessary, but I don't like to spam apis too fast
        time.sleep(1)


