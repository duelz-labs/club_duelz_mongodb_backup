import os
import shutil
import logging
from config import Config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Compressor:
    def __init__(self):
        """Initialize directories and remove old ZIP files before compression."""
        self.config = Config()
        self.json_dir = "json"  # 🔹 Directory for raw JSON backups
        self.zip_dir = "zip"    # 🔹 Directory for compressed backups
        
        # 🔹 Ensure both directories exist before using them
        os.makedirs(self.json_dir, exist_ok=True)
        os.makedirs(self.zip_dir, exist_ok=True)

        # 🔹 Remove old ZIP files before compression starts
        self.clear_old_zips()

    def clear_old_zips(self):
        """Delete old ZIP files before starting new compression."""
        for file in os.listdir(self.zip_dir):
            if file.endswith(".zip"):
                file_path = os.path.join(self.zip_dir, file)
                os.remove(file_path)
                logging.info(f"🗑 Removed old ZIP file: {file_path}")

    def compress_backup(self, backup_file):
        """Compress JSON backup and move it to zip/ folder."""
        try:
            base_name = os.path.basename(backup_file)  # Extract filename
            zip_file_path = os.path.join(self.zip_dir, f"{base_name}.zip")  # Save in zip/

            # 🔹 Skip compression if ZIP file already exists
            if os.path.exists(zip_file_path):
                logging.warning(f"⚠ Skipping compression, file already exists: {zip_file_path}")
                return zip_file_path

            # 🔹 Create ZIP archive
            shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', os.path.dirname(backup_file), os.path.basename(backup_file))

            # 🔹 Move the compressed file to 'zip/' folder
            compressed_file = f"{backup_file}.zip"
            shutil.move(compressed_file, self.zip_dir)

            # 🔹 Remove original JSON backup if configured
            if self.config.REMOVE_AFTER_COMPRESSION:
                os.remove(backup_file)

            logging.info(f"✅ Compressed file saved in: {zip_file_path}")
            return zip_file_path

        except Exception as e:
            #logging.error(f"❌ Compression failed: {e}")
            return None
