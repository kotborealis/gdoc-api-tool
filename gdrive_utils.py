import typing
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Requires drive.file scope to read/write files
SCOPES = ['https://www.googleapis.com/auth/drive.file']


def load_credentials():
    """Loads credentials from file named `token.pickle`"""

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if creds and creds.valid:
        return creds
    else:
        return False


def save_credentials(creds):
    """Save credentials to file named `token.pickle`"""

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


def refresh_credentials(creds):
    """Refresh credentials using refresh token"""

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())


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


def create_file(creds, name: str, mime_type: str = None, parents: typing.List[str] = None):
    """Create file with specified name, mime_type with specified parent list"""

    # Create service to call Google Drive API
    service = build('drive', 'v3', credentials=creds)

    return service.files().create(
        body={
            'name': name,
            'mimeType': mime_type,
            'parents:': parents,
        },
        # Ask API to return id, name and webViewLink, which is essentially sharing link
        fields='id,name,webViewLink'
    ).execute()


def create_document(creds, name: str, parents: typing.List[str] = None):
    """Create Google Document (file with mime-type `application/vnd.google-apps.document`"""

    return create_file(creds, name, mime_type='application/vnd.google-apps.document', parents=parents)


def share_file(creds, file_id: any):
    """Share edit access to anyone with link to the document"""

    service = build('drive', 'v3', credentials=creds)

    return service.permissions().create(
        fileId=file_id,
        body={
            'type': 'anyone',
            'role': 'writer'
        }
    ).execute()
