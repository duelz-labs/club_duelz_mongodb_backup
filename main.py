import argparse
import logging
import glob
import os
from backup.local_backup import LocalBackup
from compression.compress import Compressor
from cloud.google_drive import GoogleDriveUploader
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def authenticate_google_drive():
    """Authenticate Google Drive & ensure token.json is valid"""
    gauth = GoogleAuth()

  
    if os.path.exists("token.json"):
        logging.info("🔹 Loading existing token.json...")
        gauth.LoadCredentialsFile("token.json")
    else:
        logging.info("🔹 No token.json found. Generating new token...")
        gauth.LoadClientConfigFile("credentials.json")
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("token.json")
        logging.info("✅ token.json has been saved successfully!")

    # 🔹 Refresh token if expired
    if gauth.credentials is None:
        logging.warning("🔹 No credentials found. Please authenticate.")
        gauth.LocalWebserverAuth()
        gauth.SaveCredentialsFile("token.json")
    elif gauth.access_token_expired:
        logging.info("🔹 Token expired. Refreshing...")
        gauth.Refresh()
        gauth.SaveCredentialsFile("token.json")
    else:
        gauth.Authorize()

    return GoogleDrive(gauth)

def main():
    parser = argparse.ArgumentParser(description="MongoDB Backup Tool")
    parser.add_argument("--backup", action="store_true", help="Backup all collections")
    parser.add_argument("--compress", action="store_true", help="Compress backup files")
    parser.add_argument("--upload", action="store_true", help="Upload backup files to Google Drive")
    args = parser.parse_args()

    if args.backup:
        logging.info("Starting backup...")
        backup = LocalBackup()
        backup.backup_all_collections()
        logging.info("✅ Backup process completed.")
    
    if args.compress:
     logging.info("Starting compression...")
     compressor = Compressor()

    backup_files = glob.glob("json/*.json")

    for backup_file in backup_files:
        compressor.compress_backup(backup_file)

    logging.info("✅ Compression process completed.")

    if args.upload:
     logging.info("Starting upload to Google Drive...")

  
    drive = authenticate_google_drive()
    uploader = GoogleDriveUploader(drive)


    zip_files = glob.glob("zip/*.zip")

    for zip_file in zip_files:
        uploader.upload_file(zip_file)

    logging.info("✅ Upload process completed.")



if __name__ == "__main__":
    main()
