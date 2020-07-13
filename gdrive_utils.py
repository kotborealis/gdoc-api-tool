import typing
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import logging
import os

LOGLEVEL = os.environ.get('LOGLEVEL', 'WARNING').upper()
logging.basicConfig(level=LOGLEVEL)

# Requires drive.file scope to read/write files
SCOPES = ['https://www.googleapis.com/auth/drive.file']


# Mapping of supported file types to google MIME types
mime_types = {
    'document': 'application/vnd.google-apps.document',
    'spreadsheet': 'application/vnd.google-apps.spreadsheet'
}


def load_credentials():
    """Loads credentials from file named `token.pickle`"""

    logging.debug("Loading credentials from ./token.pickle")

    creds = None
    if os.path.exists('./token.pickle'):
        with open('./token.pickle', 'rb') as token:
            creds = pickle.load(token)
    else:
        logging.debug("./token.pickle does not exist!")

    if not creds:
        logging.debug("Pickle returned false while loading ./token.pickle")
    else:
        logging.debug("Loaded token.pickle: %s", creds.to_json())
        logging.debug("Valid=%s, Expired=%s", creds.valid, creds.expired)

    return creds


def save_credentials(creds):
    """Save credentials to file named `token.pickle`"""

    logging.debug("Saving credentials to ./token.pickle: %s", creds.to_json())

    with open('./token.pickle', 'wb') as token:
        pickle.dump(creds, token)


def refresh_credentials(creds):
    """Refresh credentials using refresh token"""

    logging.debug("Refreshing credentials: %s", creds.to_json())

    creds.refresh(Request())

    logging.debug("Refreshed credentials: %s", creds.to_json())


def auth_url():
    """Call Google OAuth and return authentication URL"""

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    # Use hardcoded redirect_uri to show auth code in browser
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    return flow.authorization_url()[0]


def auth_code(code):
    """Call Google OAuth with specified authentication code to obtain credentials"""

    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    # Use hardcoded redirect_uri to show auth code in browser
    # Note: redirect_uri is not used in this case, but still required
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    flow.fetch_token(code=code)

    return flow.credentials


def create_file_with_mime_type(creds, name: str, mime_type: str = None, parents: typing.List[str] = None):
    """Create file with specified name, mime_type and parent list"""

    # Create service to call Google Drive API
    service = build('drive', 'v3', credentials=creds, cache_discovery=False)

    return service.files().create(
        body={
            'name': name,
            'mimeType': mime_type,
            'parents:': parents,
        },
        # Ask API to return id, name and webViewLink, which is essentially sharing link
        fields='id,name,webViewLink'
    ).execute()


def create_file(creds, name: str, type: str, parents: typing.List[str] = None):
    """Create file with specified name, type and parent list"""
    return create_file_with_mime_type(creds, name, mime_types[type], parents)


def share_file(creds, file_id: any):
    """Share edit access to anyone with link to the document"""

    service = build('drive', 'v3', credentials=creds, cache_discovery=False)

    return service.permissions().create(
        fileId=file_id,
        body={
            'type': 'anyone',
            'role': 'writer'
        }
    ).execute()
