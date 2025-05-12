# club_duelz_mongodb_backup

Automate your MongoDB backups, compress them in-memory, and securely upload a single ZIP to Google Drive with one command!

🛠️ Simple Setup | Secure Backup | In-Memory Compression | One-Step Flow

## 📌 Features
- ✅ Dump every MongoDB collection into a structured JSONL file (in memory).  
- ✅ Bundle all collections into one timestamped ZIP file.  
- ✅ Upload the ZIP to Google Drive via Drive v3 API (service account).  
- ✅ Skip duplicates if the same ZIP name already exists.  
- ✅ Single `--zip-all` flag to run backup → compress → upload in one shot.  

---

## 📌 Prerequisites
- 🔹 Python 3.7+  
- 🔹 A MongoDB instance (local or cloud)  
- 🔹 A Google Cloud service account JSON key with Drive API enabled  
- 🔹 Access to a Google Drive folder ID where backups will be stored  

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone git@github.com:duelz-labs/club_duelz_mongodb_backup.git
cd club_duelz_mongodb_backup
```

### 2. Create and Configure `.env`
Copy the example `.env.example` and edit the values:
```bash
cp .env.example .env
```

Open `.env` and set:

```ini
# MongoDB Connection
MONGO_URI=mongodb://<user>:<pass>@<host>:<port>/<database>
DATABASE_NAME=your_database_name

# Google Drive (Service Account)
GOOGLE_DRIVE_ENABLED=true
GOOGLE_CREDENTIALS_PATH=path/to/service_account_key.json
GOOGLE_DRIVE_FOLDER_ID=your_drive_folder_id

# Logging (optional)
LOG_LEVEL=INFO
LOG_FILE=backup.log
```

- `MONGO_URI`: Your MongoDB connection string.  
- `DATABASE_NAME`: Database to back up.  
- `GOOGLE_CREDENTIALS_PATH`: Path to your service account JSON.  
- `GOOGLE_DRIVE_FOLDER_ID`: Drive folder ID from the URL.  

---

## 🚀 Running the Backup Tool

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the all-in-one backup:

```bash
python main.py --zip-all
```

Example output:

```
20-05-12 20:00:00 - INFO - 🔗 Connecting to MongoDB at 'mongodb://...'
20-05-12 20:00:00 - INFO - ✅ MongoDB connection successful
20-05-12 20:00:00 - INFO - 🗄 Using database: 'my_database'
20-05-12 20:00:00 - INFO - 📋 Found 5 collections: ['users','orders','products',...]
20-05-12 20:00:00 - INFO - ✉️  Bundling 5 collections into 12-05-20-200000.zip
20-05-12 20:00:02 - INFO - ✅ Created in-memory zip: 12-05-20-200000.zip
20-05-12 20:00:02 - INFO - ✅ Uploaded '12-05-20-200000.zip' (ID: 1a2b3c)
20-05-12 20:00:02 - INFO - ✅ Completed in 2.1s


## 📄 License
This project is licensed under the [MIT License](LICENSE).