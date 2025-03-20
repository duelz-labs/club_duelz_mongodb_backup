import logging
from io import BytesIO
import glob
from zipfile import ZipFile
from config import Config
from cloud.google_drive import GoogleDriveUploader
import os 
import shutil
import tempfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Compressor:
    def __init__(self, drive):
        """Initialize compressor with GoogleDrive instance."""
        self.config = Config()
        self.drive = drive  # Store GoogleDrive instance
        self.uploader = GoogleDriveUploader(drive)  # Pass GoogleDrive instance to uploader

    def compress_and_upload_from_memory(self, json_buffer: BytesIO, collection_name: str):
        """Compress in-memory JSON backup and upload it to Google Drive."""
        try:
            # Create an in-memory buffer for the zip file
            zip_buffer = BytesIO()
            with ZipFile(zip_buffer, 'w') as zipf:
                # Writing the JSON content to the zip file
                zipf.writestr(f"{collection_name}.json", json_buffer.getvalue())

            zip_buffer.seek(0)  # Move cursor to the beginning of the buffer

            # Generate the name of the zip file
            zip_filename = f"{collection_name}_{self.config.DATABASE_NAME}.zip"
            
            # **Upload directly from memory (as binary)**
            self.uploader.upload_from_memory(zip_buffer, zip_filename)

            logging.info(f"✅ Compressed and uploaded to Google Drive: {zip_filename}")

        except Exception as e:
            logging.error(f"❌ Compression and upload failed: {e}")

    def compress_backup(self, backup_file):
        """Compress JSON backup and upload directly to Google Drive."""
        try:
            base_name = os.path.basename(backup_file).replace(".json", "")
            zip_file_path = f"zip/{base_name}.zip"  # Save in zip/ directory

            # Skip compression if ZIP file already exists
            if os.path.exists(zip_file_path):
                logging.warning(f"⚠ Skipping compression, file already exists: {zip_file_path}")
                return zip_file_path

            # Create the zip archive from the backup file (no .json extension)
            shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', os.path.dirname(backup_file), os.path.basename(backup_file))

            # Move the compressed file to the 'zip/' directory
            compressed_file = f"{backup_file}.zip"
            shutil.move(compressed_file, 'zip')

            # Remove original JSON backup if configured
            if self.config.REMOVE_AFTER_COMPRESSION:
                os.remove(backup_file)

            logging.info(f"✅ Compressed file saved in: {zip_file_path}")
            return zip_file_path

        except Exception as e:
            logging.error(f"❌ Compression failed: {e}")
            return None

    def handle_json_files(self):
        """Handle compression of JSON files."""
        # Get all JSON files
        backup_files = glob.glob("json/*.json")

        # If no JSON files are found, skip logging this message
        if not backup_files:
            logging.info("⚠ No JSON files found to compress.")
            return  # Simply return and skip logging this message.

        # Compress each backup file
        for backup_file in backup_files:
            self.compress_backup(backup_file)

        logging.info("✅ Compression process completed.")
