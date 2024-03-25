from __future__ import print_function

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import os, os.path, threading, traceback
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.youtubeupload as youtubeupload
import re


class Upload:

    # If modifying these scopes, delete the file token.json.
    SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/youtube.upload"
    ]
    twitch_id = ''
    lock = threading.Lock()

    def getCreds(self) -> Credentials:
        """Shows basic usage of the Drive v3 API.
        Prints the names and ids of the first 10 files the user has access to.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        tokens_dir = os.path.dirname(__file__)
        token_path = os.path.join(tokens_dir, 'token.json')
        self.token_path = token_path
        self.credentials_path = os.path.join(tokens_dir, 'credentials.json')
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
        self.creds = creds
        return creds
    def getService(self, creds):
        service = build('drive', 'v3', credentials=creds)
        self.service = service
        return service
    def getItems(self, service):
        items = None
        try:
            # Call the Drive v3 API
            query = "name='" + self.twitch_id + "'and mimeType = 'application/vnd.google-apps.folder'"
            results = service.files().list(q=query,
                                            fields='nextPageToken, '
                                                'files(id, name)').execute()
            items = results.get('files', [])

            if not items:
                print('No files found.')
                return
        except HttpError as error:
            # TODO(developer) - Handle errors from drive API.
            print(f'An error occurred: {error}')
        return items

    def get_folder_id(self, service):
        for item in self.getItems(service):
            if(item['name'] == self.twitch_id):
                return item['id']

    def upload_with_conversion(self, service, parentId):
        """Upload file with conversion
        Returns: ID of the file uploaded

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
        with self.lock:
            file_list = os.listdir(self.downloads_path)
            youtube_service = youtubeupload.get_authenticated_service(self.token_path)
            for file in file_list:
                file_full_path = os.path.join(self.downloads_path, file)
                if not os.path.isfile(file_full_path):
                    continue

                file_metadata = {
                    'name': file,
                    'mimeType': 'video/' + file.split('.')[-1],
                    'parents': [parentId]
                }
                media = MediaFileUpload(file_full_path, mimetype='video/' + file.split('.')[-1],
                                        resumable=True)
                # pylint: disable=maybe-no-member
                try:
                    print(F'File with Name: "{file}" start uploading.')
                    service_result = service.files().create(body=file_metadata, media_body=media, 
                                            fields='id').execute()
                    print(F'File with ID: "{service_result.get("id")}" has been uploaded.')
                    media.stream().close()
                    
                    # title = file
                    # invalid_chars_pattern = re.compile(r'[<>:\"/\\\|\?\*]|\'+')

                    # title = re.sub(invalid_chars_pattern, '', title)
                    # title = file.replace('.mp4', '')
                    # youtubeupload.initialize_upload(youtube_service, file_full_path, title, title, youtubeupload.VALID_PRIVACY_STATUSES[0], '', '20')

                    if os.path.isfile(file_full_path):
                        os.remove(file_full_path)                      
                except HttpError as error:
                    print(F'An error occurred: {error}')
                    traceback.print_exc()
                    continue                      
                except Exception as error:
                    print(F'An Exception occurred: {error}')
                    traceback.print_exc()
                    continue

    def upload(self, id):
        self.twitch_id: str = id
        self.downloads_path = os.path.join(os.path.dirname(__file__), '..', self.twitch_id)
        creds = self.getCreds()
        service = self.getService(creds=creds)
        parentId = self.get_folder_id(service)
        self.upload_with_conversion(service, parentId)

if __name__ == '__main__':
    u = Upload()
    u.upload('')