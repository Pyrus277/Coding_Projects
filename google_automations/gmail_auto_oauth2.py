# Program for sending emails using the Gmail API. This is useful if an APP is 
# sending out emails, or if we want to use use the HT gmail account, but don't
# want to activate 2FA. The 2FA approach is more straightforward, see 
# email_auto_2fa.py for that approach. 
# Using the Gmail API does seem more robust as it gives you access to more features.
# Also, this approach requires a credentials JSON file to be generated and stored
# in the working dir. 

## IMPORTANT for this to work:##
# On the Google Cloud end - set up a service account with Gmail and Drive APIs enabled
# Generate the associated JSON file and store it in the working dir. Also, don't forget
# to share the "client_email" item from that file with the actual google sheet we want 
# to access

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

# OUATH2 stuff
# setup a list of strings that determines app permissions (scope). Here, we're just sending
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
# setup OAUTH2 flow
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
# build local web server to handle oauth2 flow and return oauth2 credentials
#     This gotta happen outside loopy
creds = flow.run_local_server(port=0)
# build the Gmail service
service = build('gmail', 'v1', credentials=creds)

def send_email(recipient, id, name):
    # construct the actual email
    
    # attach an image
    with open('ht_logo.jpg', 'rb') as fhand:
        image_part = MIMEImage(fhand.read())
    # build out the rest of the email details
    message = MIMEMultipart() # multipart to have both text and image
    message['subject'] = 'HollowTree email automation'
    message['to'] = recipient
    name = "Inserted Name"
    body = f"""
    <html>
      <body>
      <p>Hello!</p>
      <p>This is an automated test email from the HollowTree Gmail account Liana set up.</p>
      <p>Your name is {name}, and your randomly generated ID number is {id}: </p>
      
      <p>This email was created with Python and uses addresses and info from a spreadsheet
      the shared drive to personalize it.
      It also automatically updates the spreadsheet with details about the message, assuming no 
      errors happened. </p>
      
      <p> The idea here is to automate and orgnize our data gathering efforts.</p>
      
      <p> Reply or message me on Slack to confirm you got this message! </p>

      </body>
    </html>    
    """
    text_part = MIMEText(body, 'html')
    message.attach(text_part)
    message.attach(image_part)
    
    # encode our message as base64 and pack it in a variable
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    # send out the email with .send() method. Set up error catching
    # in case our API http request fails
    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None


recipients = ['pyrus277@gmail.com', 'hollowtree.app@gmail.com']
for recipient in recipients:
    send_email(recipient)

# THIS WORKS!
# Note - Running this program will have Google ask you in the web browser
# permission to proceed. Thankfully this only happens once for the local
# web server that gets set up, Generating multiple emails in a loop does not
# require further confrimations. So we're all good!
    