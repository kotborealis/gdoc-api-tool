from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']


def load_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if creds and creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        return creds
    else:
        return False


def save_credentials(creds):
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)


def refresh_credentials(creds):
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())


def auth_url():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    return flow.authorization_url()[0]


def auth_code(code):
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
    flow.redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'

    flow.fetch_token(code=code)

    return flow.credentials


def create_file(creds, name, mime_type=None, parents=None):
    service = build('drive', 'v3', credentials=creds)

    return service.files().create(
        body={
            'name': name,
            'mimeType': mime_type,
            'parents:': parents,
        },
        fields='id,name,webViewLink'
    ).execute()


def create_document(creds, name, parents=None):
    return create_file(creds, name, mime_type='application/vnd.google-apps.document', parents=parents)


def share_file(creds, fileId):
    service = build('drive', 'v3', credentials=creds)

    return service.permissions().create(
        fileId=fileId,
        body={
            'type': 'anyone',
            'role': 'writer'
        }
    ).execute()
