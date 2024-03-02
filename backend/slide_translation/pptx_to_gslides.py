from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

class GDriveUploader:

    upload_file = None

    def __init__(self):
        # OAth2
        SCOPES = ["https://www.googleapis.com/auth/drive"]
        self.script_dir = os.path.dirname(os.getcwd() + "/backend")
        creds = None
        token_path = os.path.join(self.script_dir, "token.json")

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                creds_path = os.path.join(self.script_dir, "credentials.json")
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES
                )
                creds = flow.run_local_server(port=0)
            
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        self.service = build("drive", "v3", credentials=creds)
        self.gdrive_folder = "unihack2024_uploads"

    def upload_ppt(self, path_to_ppt: str):
        try:
            response = self.service.files().list(
                q=f"name='{self.gdrive_folder}' and mimeType='application/vnd.google-apps.folder'"
            ).execute()

            if not response["files"]:
                file_metadata = {
                    "name": self.gdrive_folder,
                    "mimeType": "application/vnd.google-apps.folder"
                }

                file = self.service.files().create(body=file_metadata, fields="id").execute()

                self.service.permissions().create(
                    fileId=file['id'],
                    body={'role': 'writer', 'type': 'anyone', 'value': 'anyone'},
                    fields='id'
                ).execute()

                folder_id = file.get("id")

            else:
                folder_id = response["files"][0]["id"]
                ppt_name = path_to_ppt.split("/").pop()
                file_metadata = {
                    "name": ppt_name,
                    "parents": [folder_id]
                }

                media = MediaFileUpload(path_to_ppt,
                                        mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation',
                                        resumable=True)
                upload_file = self.service.files().create(body=file_metadata,
                                                    media_body=media,
                                                    fields="id").execute()

                print("File ID:", upload_file.get("id"))
                self.upload_file = upload_file
                return upload_file.get("id")

        except HttpError as e:
            print("Error: " + str(e))
            return None

    def get_sharable_link(self):
        """Get the sharable link for the most recent successful upload. None upon error"""
        try:
            # Retrieve the file metadata
            file_id = self.upload_file.get("id")
            self.service.permissions().create(
                    fileId=file_id,
                    body={'role': 'writer', 'type': 'anyone', 'value': 'anyone'}
                ).execute()
            file_metadata = self.service.files().get(fileId=file_id, fields='webViewLink').execute()

            # Extract the webViewLink from the metadata
            webViewLink = file_metadata['webViewLink']
            
            # Construct the sharable link
            sharable_link = f"{webViewLink}&export=download"
            
            return sharable_link
        except Exception as e:
            print("An error occurred:", e)
            return None


if __name__ == "__main__":
    uploader = GDriveUploader()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    rel_path_upload_dir = "../translated_presentations/"
    creds_path = os.path.join(script_dir, rel_path_upload_dir)
    for ppt in os.listdir(creds_path):
        ppt_path = os.path.join(creds_path, ppt)
        fileId = uploader.upload_ppt(ppt_path)
        print(f"{ppt} was uploaded\nId: {fileId}")
        print(uploader.get_sharable_link())
