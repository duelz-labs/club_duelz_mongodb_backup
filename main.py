import argparse
import logging
import time
from config import Config
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from backup.bulk_backup import BulkBackup
from cloud.google_drive import GoogleDriveUploader

# --- configure logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%y %H:%M:%S"
)

def authenticate_service_account():
    info = Config.service_account_info()
    creds = Credentials.from_service_account_info(
        info,
        scopes=Config.DRIVE_SCOPES
    )
    drive = build("drive", "v3", credentials=creds)
    logging.info("✅ Authenticated to Google Drive via service account")
    return drive

def main():
    parser = argparse.ArgumentParser(
        description="📦 MongoDB → in-memory ZIP → Google Drive (one command only)"
    )
    parser.add_argument(
        "--zip-all",
        action="store_true",
        help="🎁 Dump every collection to one ZIP and upload it"
    )
    args = parser.parse_args()

    if not args.zip_all:
        parser.print_help()
        return

    if not Config.GOOGLE_DRIVE_ENABLED:
        logging.error("❌ GOOGLE_DRIVE_ENABLED is false; aborting.")
        return

    drive = authenticate_service_account()
    uploader = GoogleDriveUploader(drive, folder_id=Config.GOOGLE_DRIVE_FOLDER_ID)

    start = time.time()
    buf, zip_name = BulkBackup().create_zip()
    if buf is None:
        logging.warning("⚠ No collections found; nothing to upload.")
    else:
        uploader.upload_from_memory(buf, zip_name)
        logging.info(f"✅ All done in {time.time() - start:.1f}s")

if __name__ == "__main__":
    main()