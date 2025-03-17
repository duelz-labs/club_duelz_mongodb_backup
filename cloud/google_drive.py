from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging
import os
from dotenv import load_dotenv


load_dotenv()
GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

class GoogleDriveUploader:
    def __init__(self, drive=None):
        """Initialize with an authenticated GoogleDrive instance."""
        if drive is None:
            logging.error("GoogleDrive instance is required but not provided!")
            raise ValueError("GoogleDrive instance is required.")
        self.drive = drive

    def file_exists_in_drive(self, file_name):
        """Check if a file with the same name exists in Google Drive folder."""
        try:
            file_list = self.drive.ListFile({
                'q': f"'{GOOGLE_DRIVE_FOLDER_ID}' in parents and trashed=false and title='{file_name}'"
            }).GetList()
            return len(file_list) > 0
        except Exception as e:
            logging.error(f"❌ Failed to check existing files: {e}")
            return False

    def upload_file(self, file_path):
        """Uploads a file to a specific Google Drive folder, avoiding duplicates."""
        try:
            file_name = os.path.basename(file_path)

           
            if self.file_exists_in_drive(file_name):
                logging.warning(f"⚠ Skipping upload, file already exists in Google Drive: {file_name}")
                return

            gfile = self.drive.CreateFile({
                'title': file_name,
                'parents': [{'id': GOOGLE_DRIVE_FOLDER_ID}]
            })
            gfile.SetContentFile(file_path)
            gfile.Upload()
            logging.info(f"✅ Successfully uploaded {file_name} to Google Drive folder {GOOGLE_DRIVE_FOLDER_ID}.")

        except Exception as e:
            logging.error(f"❌ Upload failed: {e}")
