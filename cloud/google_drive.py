from io import BytesIO
import logging
import os
from dotenv import load_dotenv
from pydrive.drive import GoogleDrive
import tempfile
import time

# Load environment variables
load_dotenv()

GOOGLE_DRIVE_FOLDER_ID = os.getenv("GOOGLE_DRIVE_FOLDER_ID")

class GoogleDriveUploader:
    def __init__(self, drive=None):
        """Initialize with an authenticated GoogleDrive instance."""
        if drive is None:
            logging.error("❌ GoogleDrive instance is required but not provided!")
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
            gfile.SetContentFile(file_path)  # Upload local file
            gfile.Upload()
            logging.info(f"✅ Successfully uploaded {file_name} to Google Drive folder {GOOGLE_DRIVE_FOLDER_ID}.")

        except Exception as e:
            logging.error(f"❌ Upload failed: {e}")

    def upload_from_memory(self, file_buffer: BytesIO, file_name: str, retries=3, delay=2):
        """Upload a file from an in-memory buffer (BytesIO) to Google Drive."""
        try:
            if self.file_exists_in_drive(file_name):
                logging.warning(f"⚠ Skipping upload, file already exists in Google Drive: {file_name}")
                return

            # Create a temporary file and write the contents of BytesIO into it
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(file_buffer.getvalue())
                temp_file_path = temp_file.name
                logging.info(f"🔹 Temporary file created for upload: {temp_file_path}")

            gfile = self.drive.CreateFile({
                'title': file_name,
                'parents': [{'id': GOOGLE_DRIVE_FOLDER_ID}]
            })

            # Retry the upload a few times in case the file is locked
            for attempt in range(retries):
                try:
                    gfile.SetContentFile(temp_file_path)
                    gfile.Upload()
                    logging.info(f"✅ Successfully uploaded {file_name} to Google Drive folder {GOOGLE_DRIVE_FOLDER_ID}.")
                    break  # Exit the retry loop if upload is successful
                except Exception as e:
                    logging.error(f"❌ Upload failed on attempt {attempt + 1}: {e}")
                    if attempt < retries - 1:
                        logging.info(f"Retrying upload... attempt {attempt + 2}")
                        time.sleep(delay)  # Wait before retrying
                    else:
                        logging.error(f"❌ All retries failed. Unable to upload {file_name}.")
                        raise e

            # Optionally, delete the temporary file after upload
            os.remove(temp_file_path)
            logging.info(f"✅ Temporary file {temp_file_path} removed successfully.")

        except Exception as e:
            logging.error(f"❌ Upload failed: {e}")
