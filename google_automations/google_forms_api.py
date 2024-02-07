# This program copies an existing file in Google Drive, a Forms file, 
# in this case, renames it, and also updates the content of the Form.

from google_auth_oauthlib.flow import InstalledAppFlow # same
from googleapiclient.discovery import build # same
from requests import HTTPError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]
flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
creds = flow.run_local_server(port=0)
service_drive = build('drive', 'v3', credentials=creds)
service_forms = build('forms', 'v1', credentials=creds)

def generate_form():
    """
    This function copies an existing Google Form file,
    Updates the form name, and updates the form's header text
    to be personalized to the recipient.
    """
    try:
        # copy the base file
        origin_file_id = "17PHV9vRT_NOdoNl2sb1J_q_lyR9sFgPDzRuSwZSZfSE" 
        results = service_drive.files().copy(fileId=origin_file_id).execute()
        print(f'file that was copied: {results}') # output details
        
        # Update the form name
        #   get the file
        new_file_id = results['id']
        new_file_name = 'HT_test_form_ID_7690'
        file = service_drive.files().get(fileId=new_file_id, fields='name').execute()
        #   Update metadata
        file['name'] = new_file_name
        #   Send request to API with update method
        updated_file = service_drive.files().update(
            fileId=new_file_id,
            body = file).execute()
        print(f"File '{file['name']}' renamed successfully.")
    
    except HTTPError as error:
        print('An error occurred: {error}')
        
    # Update the form body
    #     Write out the specific updates
    update = {
        "requests": [
            {
                "updateFormInfo": {
                    "info": {
                        "title": "HT Test form, ID 7690",
                        "description": (
                            "This is a survey for Perry Fox, ID 7690."
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

if __name__ == "__main__":
   generate_form()

