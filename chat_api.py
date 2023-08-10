from httplib2 import Http
from oauth2client.service_account import ServiceAccountCredentials
from apiclient.discovery import build

scopes = 'https://www.googleapis.com/auth/chat.bot'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credentials_2.json', scopes)

chat_service = build('chat', 'v1', http=credentials.authorize(Http()))

def extract(n):
    return n['name']

spaces_list = chat_service.spaces().list().execute()
all_spaces = map(extract, spaces_list['spaces'])
print(all_spaces)