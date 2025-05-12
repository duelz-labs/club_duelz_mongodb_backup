import logging
import os
import glob
import shutil
import tempfile
from io import BytesIO
from zipfile import ZipFile

from config import Config
from cloud.google_drive import GoogleDriveUploader

class Compressor:
    def __init__(self, drive_service):
        """
        Initialize compressor with GoogleDrive service client.
        Pull folder_id from Config and pass it to the uploader.
        """
        self.config = Config()
        self.drive = drive_service
        self.uploader = GoogleDriveUploader(
            drive_service,
            folder_id=self.config.GOOGLE_DRIVE_FOLDER_ID
        )

    def compress_and_upload_from_memory(self, json_buffer: BytesIO, collection_name: str):
        """
        Compress an in-memory JSON buffer and upload it to Google Drive.
        """
        try:
            # Create an in-memory ZIP
            zip_buf = BytesIO()
            with ZipFile(zip_buf, 'w') as zipf:
                zipf.writestr(f"{collection_name}.json", json_buffer.getvalue())
            zip_buf.seek(0)

            zip_filename = f"{collection_name}_{self.config.DATABASE_NAME}.zip"
            self.uploader.upload_from_memory(zip_buf, zip_filename)
            logging.info(f"✅ Compressed & uploaded: {zip_filename}")

        except Exception as e:
            logging.error(f"❌ compress_and_upload_from_memory failed: {e}")

    def compress_backup(self, backup_file: str):
        """
        Compress a local JSON file to disk and optionally upload it.
        Returns path to the .zip on disk or None on error.
        """
        try:
            base = os.path.basename(backup_file).rsplit('.json', 1)[0]
            zip_dir = "zip"
            os.makedirs(zip_dir, exist_ok=True)
            zip_path = os.path.join(zip_dir, f"{base}.zip")

            if os.path.exists(zip_path):
                logging.warning(f"⚠ ZIP already exists, skipping: {zip_path}")
                return zip_path

            # Create the ZIP 
            shutil.make_archive(
                base_name=os.path.join(zip_dir, base),
                format="zip",
                root_dir=os.path.dirname(backup_file),
                base_dir=os.path.basename(backup_file)
            )

            if self.config.REMOVE_AFTER_COMPRESSION:
                os.remove(backup_file)

            logging.info(f"✅ Compressed on disk: {zip_path}")
            return zip_path

        except Exception as e:
            logging.error(f"❌ compress_backup failed for {backup_file}: {e}")
            return None

    def handle_json_files(self):
        """
        Find all json/*.json files, compress them on disk, then upload.
        """
        files = glob.glob("json/*.json")
        if not files:
            logging.info("⚠ No JSON files found to compress.")
            return

        for path in files:
            zip_path = self.compress_backup(path)
            if zip_path:
                # Optionally upload each ZIP on disk
                with open(zip_path, "rb") as f:
                    buf = BytesIO(f.read())
                self.uploader.upload_from_memory(buf, os.path.basename(zip_path))

        logging.info("✅ handle_json_files completed.")  