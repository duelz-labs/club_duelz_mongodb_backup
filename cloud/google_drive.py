import logging
import os
import tempfile
from io import BytesIO
from googleapiclient.http import MediaFileUpload

class GoogleDriveUploader:
    """
    Uploads files (or in-memory buffers) to Google Drive v3.
    """

    def __init__(self, drive_service, folder_id: str):
        self.drive = drive_service
        self.folder_id = folder_id

    def file_exists(self, name: str) -> bool:
        """Return True if a non-trashed file with this name already exists in the folder."""
        try:
            resp = self.drive.files().list(
                q=(
                    f"'{self.folder_id}' in parents "
                    f"and name = '{name}' "
                    "and trashed = false"
                ),
                fields="files(id, name)"
            ).execute()
            return bool(resp.get("files"))
        except Exception as e:
            logging.error(f"❌ Failed to check existing files: {e}")
            return False

    def upload_from_memory(self, buf: BytesIO, filename: str):
        """
        Upload a BytesIO buffer as a file named `filename` under self.folder_id.
        Skips upload if the file already exists.
        """
        if self.file_exists(filename):
            logging.warning(f"⚠ Skipping upload; '{filename}' already exists.")
            return

        # Dump buffer to a temp file
        tf = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
        try:
            tf.write(buf.getvalue())
            tf.flush()
            tf.close()

            media = MediaFileUpload(tf.name, mimetype="application/zip")
            metadata = {
                "name": filename,
                "parents": [self.folder_id]
            }
            created = (
                self.drive.files()
                          .create(body=metadata, media_body=media, fields="id,name")
                          .execute()
            )
            logging.info(f"✅ Uploaded '{created['name']}' (ID: {created['id']})")
        except Exception as e:
            logging.error(f"❌ Upload-from-memory failed: {e}")
        finally:
            try:
                os.unlink(tf.name)
            except OSError:
                pass