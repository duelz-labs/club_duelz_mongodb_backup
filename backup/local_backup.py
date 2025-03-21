import pymongo
import logging
import json
from io import BytesIO
from config import Config
from compression.compress import Compressor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class LocalBackup:
    def __init__(self, drive):
        """Initialize MongoDB connection and compression utility with GoogleDrive instance."""
        self.config = Config()
        self.client = pymongo.MongoClient(self.config.MONGO_URI)
        self.db = self.client[self.config.DATABASE_NAME]
        self.compressor = Compressor(drive)  # Pass GoogleDrive instance to Compressor
        self.drive = drive  # Store GoogleDrive instance

    def backup_collection(self, collection_name):
        """Backup a single collection and return the data as in-memory JSON."""
        collection = self.db[collection_name]
        
        # Create an in-memory buffer (BytesIO) to store JSON backup data
        json_buffer = BytesIO()

        for doc in collection.find():
            json_buffer.write(json.dumps(doc, default=str).encode('utf-8') + b"\n")

        json_buffer.seek(0)
        logging.info(f"✅ Backup completed for collection: {collection_name}")

        # Compress and upload the data directly from memory
        self.compressor.compress_and_upload_from_memory(json_buffer, collection_name)

    def backup_all_collections(self):
        """Backup all collections and upload them directly to Google Drive."""
        logging.info("Starting backup of all collections...")

        for collection_name in self.db.list_collection_names():
            json_buffer = self.backup_collection(collection_name)
            
        logging.info("✅ All collections have been backed up successfully.")
