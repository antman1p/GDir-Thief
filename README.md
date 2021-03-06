<h1 align="center">
  <img src="static/g-directory-thief-logo.png" alt="gdir-thief" width="400px"></a>
  <br>
</h1>
<p align="center">
<a href="https://twitter.com/antman1p"><img src="https://img.shields.io/twitter/follow/antman1p.svg?logo=twitter"></a>
</p>

# GDir-Thief
Red Team tool for exfiltrating the target organization's Google People Directory that you have access to, via Google's People API.
## HOW TO
### Create a new Google Cloud Platform (GCP) project
Steps to get the Google API Access Token needed for connecting to the API
1.  Create a burner gmail/google account
2.  Login to said account
3.  Navigate to the Google [Cloud Console](https://console.cloud.google.com/)
4.  Next to "Google Cloud Platform," click the `Down arrow`. A dialog listing current projects appears.
5.  Click `New Project`. The New Project screen appears.
6.  In the `Project Name field`, enter a descriptive name for your project.
7.  (Optional) To edit the `Project ID`, click `Edit`. The project ID can't be
  changed after the project is created, so choose an ID that meets your needs for
  the lifetime of the project.
8.  Click `Create`. The console navigates to the Dashboard page and your project is created within a few minutes.
### Enable a Google Workspace API
1.  Next to "Google Cloud Platform," click the `Down arrow` and select the project
  you just created from the dropdown list.
2.  In the top-left corner, click `Menu` > `APIs & Services`.
3.  Click `Enable APIs and Services`. The `Welcome to API Library` page appears.
4.  In the `search field`, enter "People".
5.  Click the API to enable. The API page appears.
6.  Click `Enable`. The Overview page appears.
###  Configure OAuth Consent screen
1.  On the left side of the Overview page click `Credentials`. The credential
page for your project appears.
2.  Click `Configure Consent Screen`. The "OAuth consent screen" screen appears.
3.  Click the `External` user type for your app.
4.  Click `Create`. A second "OAuth consent screen" screen appears.
5.  Fill out the form:
    - Enter an Application Name in the `App name` field
    - Enter your burner email address in the `User support email` field.
    - Enter your burner email address in the `Developer contact information` field.
6.  Click `Save and Continue`. The "Scopes" page appears.
7.  Click `Add or Remove Scopes`. The "Update selected scopes" page appears.
8.  Check all of the `Google People` scopes to use in the app.
9.  Click `Update`. A list of scopes for your app appears.
10. Click `Save and Continue`. The "Edit app registration" page appears.
11. Click `Save and Continue`. The "OAuth consent screen" appears.
### Create a credential
1.  Click `Create Credentials` and select `OAuth client ID`. The "Create OAuth
  client ID" page appears.
2.  Click the Application type drop-down list and select `Desktop Application`.
3.  In the `name` field, type a name for the credential. This name is only shown
  in the Cloud Console.
4.  Click `Create`. The OAuth client created screen appears. This screen shows
  the `Client ID` and `Client secret`.
5.  Click `OK`. The newly created credential appears under "OAuth 2.0 Client IDs."
6.  Click the `download` button to the right of the newly-created OAuth 2.0
  Client ID. This copies a client secret JSON file to your desktop. Note the
  location of this file.
7.  Rename the client secret JSON file to "credentials.json" and move it to the
  `gdir_thief/credentials` directory.
### Add the victim's Google account to the Application's Test Users
In order to be able to run this script against the victim, you will need to add
their Google account to the Test Users list for the App you just created
1.  On the Left side of the screen click `OAuth consent screen`.  You "OAuth
  Consent Screen" page appears.
2.  Under `Test Users` click the `Add Users` button.
3.  Enter the vicim's Gmail address in the `email address` field.
4.  Click the `save` button.
### First Time running gdir_thief
Upon gaining access to a Target's Google account, you can run gdir_thief
1.  The first time running gdir_thief, the script opens a new window prompting you
to authorize access to your data:
    1.  If you are not already signed in to your Google account, you are
      prompted to sign in. If you are signed in to multiple Google accounts, you
      are asked to select one account to use for the authorization.  Make sure
      you select the victim's Google account
## Dependencies
Google API Libraries: `pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib`
## Usage:
```
usage:
python3 gdir_thief.py [-h]

help:

This Module will connect to Google's People API using an access token and exfiltrate the organization's
People directory.  It will output a CSV file to ./loot/directory.csv
```
