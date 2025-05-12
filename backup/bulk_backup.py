import json
import time
import zipfile
import logging
from io import BytesIO
from typing import Tuple, Optional
from config import Config
import pymongo

class BulkBackup:
    """
    Dump every collection from MongoDB into a single in-memory ZIP.
    """
    def __init__(self):
        cfg = Config()
        self.client = pymongo.MongoClient(cfg.MONGO_URI)
        self.db = self.client[cfg.DATABASE_NAME]

    def create_zip(self) -> Optional[Tuple[BytesIO, str]]:
        
        names = self.db.list_collection_names()
        if not names:
            logging.warning("⚠ No collections found to bundle.")
            return None

        timestamp = time.strftime("%d-%m-%y-%H%M%S")
        zip_name = f"{timestamp}.zip"
        buf = BytesIO()

        logging.info(f"✉️  Bundling {len(names)} collections into {zip_name}")
        with zipfile.ZipFile(buf, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            for idx, coll in enumerate(names, start=1):
                logging.info(f"[{idx}/{len(names)}] Adding '{coll}.jsonl'")
                # collect docs
                data = []
                for doc in self.db[coll].find():
                    data.append(json.dumps(doc, default=str))
                # write a single JSONL file per collection
                content = "\n".join(data).encode("utf-8")
                zf.writestr(f"{coll}.jsonl", content)

        buf.seek(0)
        logging.info(f"✅ Created in-memory zip: {zip_name}")
        return buf, zip_name