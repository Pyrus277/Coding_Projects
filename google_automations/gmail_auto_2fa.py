# Simple program for automating basic emails. For this to work we need to allow 2-factor
# and then get the 16 digit password. Alternatively, to go the OAUTH2 route, we need
# to make use of the Gmail API. See file 'email_automation_oauth2.py` for that.
# Since the HT account is shared, I don't want to activate 2fa, but if I hit too many hiccups 
# I'll activate it anyway and we'll death with it. The code below in this case is quite neat.  

import smtplib
from email.mime.text import MIMEText

# create message
subject = "Test automated email"
body = "This is the body of the email"
sender = "hollowtree.app@gmail.com"
recipients = ["pyrus22@gmail.com"]
password = "HollowTree1!"

def send_email(subject, body, sender, recipients, password):
    # create message with MIMEText
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)# needs to be a single string, with comma separated items, if multiple recips

    # connect to gmail server with SSL
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
        smtp_server.login(sender, password)
        # actually send out our email
        smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

send_email(subject, body, sender, recipients, password)
