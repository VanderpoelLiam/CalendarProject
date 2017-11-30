import os
from oauth2client import client, tools
from oauth2client.file import Storage

class Parser:
    def getCredentials(self, filename, applicationName, scopes):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Requires:
            filename: string
                filename for created json credential file.
            applicationName: string
                name of program im getting credentials for.
            scopes: string
                what to authorize this program to access.

        Returns:
            Credentials, the obtained credential.
        """
        try:
            import argparse
            flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
        except ImportError:
            flags = None

        CLIENT_SECRET_FILE = 'client_secret.json'
        # filename = 'calendar-python-event-schedueler.json'
        # applicationName = 'Google Calendar Event Schedueler'
        # scopes = 'https://www.googleapis.com/auth/calendar'

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       filename)

        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, scopes)
            flow.user_agent = applicationName
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials
