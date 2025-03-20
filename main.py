import argparse
import logging
import glob
import os
from backup.local_backup import LocalBackup
from compression.compress import Compressor
from cloud.google_drive import GoogleDriveUploader
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from io import BytesIO
import tempfile

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def authenticate_google_drive():
    """Authenticate and ensure token.json is valid for offline use."""
    gauth = GoogleAuth()

    # 1️⃣ Try Loading Existing Token First
    if os.path.exists("token.json"):
        logging.info("🔹 Loading existing token.json...")
        gauth.LoadCredentialsFile("token.json")

        if gauth.credentials is None:
            logging.warning("🔹 No valid credentials found. Re-authenticating...")
        elif gauth.access_token_expired:
            logging.info("🔹 Token expired. Attempting to refresh...")
            try:
                gauth.Refresh()
                gauth.SaveCredentialsFile("token.json")
                return GoogleDrive(gauth)
            except Exception as e:
                logging.error(f"❌ Token refresh failed: {e}. Re-authenticating...")

    # 2️⃣ Force Re-authentication with Offline Access if No Token Exists
    logging.info("🔹 No valid token found. Performing full authentication...")
    gauth.LoadClientConfigFile("credentials.json")
    
    # Force getting a refresh token
    gauth.LocalWebserverAuth()  
    gauth.SaveCredentialsFile("token.json")
    
    logging.info("✅ Authentication successful. token.json has been saved!")
    
    return GoogleDrive(gauth)


def main():
    logging.info("Starting main function...")
    parser = argparse.ArgumentParser(description="MongoDB Backup Tool")
    parser.add_argument("--backup", action="store_true", help="Backup all collections")
    parser.add_argument("--compress", action="store_true", help="Compress backup files")
    parser.add_argument("--upload", action="store_true", help="Upload backup files to Google Drive")
    args = parser.parse_args()

    logging.info(f"Arguments received: backup={args.backup}, compress={args.compress}, upload={args.upload}")

    # Authenticate Google Drive and proceed with actions
    drive = authenticate_google_drive()  # Authenticate and return GoogleDrive instance
    uploader = GoogleDriveUploader(drive)  # Pass the GoogleDrive instance here

    # **FIX**: Pass `drive` instance to `LocalBackup` and `Compressor`
    if args.backup:
        logging.info("Starting backup...")
        backup = LocalBackup(drive)  # Pass drive instance to LocalBackup
        backup.backup_all_collections()
        logging.info("✅ Backup process completed.")
    
    if args.compress:
        logging.info("Starting compression...")
        compressor = Compressor(drive)  # Pass drive instance to Compressor

        backup_files = glob.glob("json/*.json")
        logging.info(f"Found {len(backup_files)} JSON files to compress.")
        for backup_file in backup_files:
            compressor.compress_backup(backup_file)

        logging.info("✅ Compression process completed.")

    if args.upload:
        logging.info("Starting upload to Google Drive...")
        zip_files = glob.glob("zip/*.zip")
        logging.info(f"Found {len(zip_files)} zip files to upload.")
        for zip_file in zip_files:
            uploader.upload_file(zip_file)

        logging.info("✅ Upload process completed.")


# Ensure main() is executed when script is run directly
if __name__ == "__main__":
    main()
