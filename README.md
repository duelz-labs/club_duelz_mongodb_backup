# MongoDB_Backup 

Automate your MongoDB backups, compress them, and securely upload to Google Drive!

🛠️ Simple Setup | Secure Backup | Easy Restoration

## 📌 Features
- ✅ Backup all MongoDB collections and store them in a structured format (.json).
- ✅ Compress backups into ZIP files to save space.
- ✅ Upload backups to Google Drive for secure cloud storage.
- ✅ Automatic cleanup of old backup files to avoid duplicates.
- ✅ Flexible configuration via .env file.

## 📖 Table of Contents
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
  - [Step 1: Clone the Repository](#step-1-clone-the-repository)
  - [Step 2: Set Up Google Cloud Credentials](#step-2-set-up-google-cloud-credentials)
  - [Step 3: Configure the .env File](#step-3-configure-the-env-file)
- [Configuration Details](#configuration-details)
- [Running the Backup Tool](#running-the-backup-tool)
- [Common Issues & Troubleshooting](#common-issues--troubleshooting)
- [License](#license)

## 📌 Prerequisites
Before running this tool, make sure you have:
- 🔹 Python 3.7+ installed.
- 🔹 A MongoDB database (local or cloud-based).
- 🔹 A Google Cloud Project with Drive API enabled (for Google Drive uploads).
- 🔹 Google OAuth Credentials (credentials.json) for authentication.

## ⚙️ Setup Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/mongodb-backup.git
cd mongodb-backup
```

### Step 2: Set Up Google Cloud Credentials
🎯 **Why is this needed?**
This allows the script to authenticate with Google Drive and upload backups automatically.

#### ✅ 1. Enable Google Drive API
- Go to Google Cloud Console.
- Create a new project or select an existing one.
- In the APIs & Services section, search for "Google Drive API" and enable it.

#### ✅ 2. Generate OAuth 2.0 Credentials
- Go to APIs & Services → Credentials.
- Click Create Credentials → Select OAuth Client ID.
- Choose "Web Application" as the application type.
- Add http://localhost:8080/ as the Authorized Redirect URI.
- Click Create, then download credentials.json.

#### ✅ 3. Move credentials.json to the Project Folder
```bash
mv ~/Downloads/credentials.json mongodb-backup/
```
📌 Make sure to update the .env file with the correct path to this file!

### Step 3: Configure the .env File
📌 The .env file is used to securely store configuration settings.

#### ✅ Create the .env file
```bash
cp .env.example .env
```

#### ✅ Edit the .env file
Open the .env file in any text editor and update the necessary values:

```ini
# MongoDB Connection
MONGO_URI=mongodb://your_mongo_user:password@host:port/database_name
DATABASE_NAME=my_database

# Backup Settings
BACKUP_DIR=backup
BACKUP_FORMAT=jsonl
BATCH_SIZE=500
COMPRESS_BACKUPS=true
COMPRESSION_LEVEL=6
REMOVE_AFTER_COMPRESSION=true

# Google Drive Configuration
GOOGLE_DRIVE_ENABLED=true
GOOGLE_CREDENTIALS_PATH=credentials.json
GOOGLE_DRIVE_FOLDER_ID=your_google_drive_folder_id

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=backup.log
```

🎯 **Important Notes:**
- `MONGO_URI`: Replace with your MongoDB connection string.
- `GOOGLE_CREDENTIALS_PATH`: Must point to your credentials.json file.
- `GOOGLE_DRIVE_FOLDER_ID`: Find the Folder ID in Google Drive by opening the folder and copying the long string from the URL.

## ⚙️ Configuration Details

| Variable | Description |
|----------|-------------|
| MONGO_URI | MongoDB connection string (Atlas/local) |
| DATABASE_NAME | Name of the database to back up |
| BACKUP_DIR | Directory where backups will be stored |
| COMPRESS_BACKUPS | Enable compression (true / false) |
| GOOGLE_DRIVE_ENABLED | Enable Google Drive upload (true / false) |
| GOOGLE_DRIVE_FOLDER_ID | Folder ID in Google Drive where backups will be uploaded |
| LOG_LEVEL | Logging level (e.g., INFO, DEBUG, ERROR) |

## 🚀 Running the Backup Tool
Once everything is set up, you can start using the tool.

### ✅ 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### ✅ 2. Run the Backup Script
```bash
python main.py --backup --compress --upload
```

- `--backup` → Backs up all MongoDB collections to the json/ folder.
- `--compress` → Compresses backup files into zip/.
- `--upload` → Uploads .zip backups to Google Drive.

🔹 **Example Output:**
```
✅ Backup completed: json/ahmedabad_2025_03_17_2315.json
✅ Compression completed: zip/ahmedabad_2025_03_17_2315.zip
✅ Successfully uploaded ahmedabad_2025_03_17_2315.zip to Google Drive.
✅ Upload process completed.
```

## ❌ Common Issues & Troubleshooting

| Issue | Solution |
|-------|----------|
| "MongoDB connection failed" | Double-check your MONGO_URI and ensure MongoDB is running. |
| "Google Drive authentication failed" | Ensure credentials.json exists and is correctly configured. Run `python test.py` to verify authentication. |
| "File already exists" | The script skips duplicate uploads. If necessary, delete old backups manually. |
| ".env not found" | Make sure you have created .env from .env.example. |

📌 To debug issues, check backup.log for detailed logs.