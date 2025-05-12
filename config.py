import os
import json
from dotenv import load_dotenv

load_dotenv()

class Config:
   
    MONGO_URI= os.getenv("MONGO_URI")
    DATABASE_NAME= os.getenv("DATABASE_NAME")

   
    BACKUP_DIR              = os.getenv("BACKUP_DIR", "backup")
    REMOVE_AFTER_COMPRESSION= os.getenv("REMOVE_AFTER_COMPRESSION", "true").lower() == "true"

    
    GOOGLE_DRIVE_ENABLED    = os.getenv("GOOGLE_DRIVE_ENABLED", "false").lower() == "true"
    GOOGLE_DRIVE_FOLDER_ID  = os.getenv("GOOGLE_DRIVE_FOLDER_ID")


    SA_TYPE                         = os.getenv("SA_TYPE", "service_account")
    SA_PROJECT_ID                   = os.getenv("SA_PROJECT_ID")
    SA_PRIVATE_KEY_ID               = os.getenv("SA_PRIVATE_KEY_ID")
    SA_PRIVATE_KEY                  = os.getenv("SA_PRIVATE_KEY", "").replace("\\n", "\n")
    SA_CLIENT_EMAIL                 = os.getenv("SA_CLIENT_EMAIL")
    SA_CLIENT_ID                    = os.getenv("SA_CLIENT_ID")
    SA_AUTH_URI                     = os.getenv("SA_AUTH_URI")
    SA_TOKEN_URI                    = os.getenv("SA_TOKEN_URI")
    SA_AUTH_PROVIDER_X509_CERT_URL  = os.getenv("SA_AUTH_PROVIDER_X509_CERT_URL")
    SA_CLIENT_X509_CERT_URL         = os.getenv("SA_CLIENT_X509_CERT_URL")
    SA_UNIVERSE_DOMAIN              = os.getenv("SA_UNIVERSE_DOMAIN")

    # OAuth scopes for Google Drive
    DRIVE_SCOPES = ["https://www.googleapis.com/auth/drive"]

    @classmethod
    def service_account_info(cls) -> dict:
        """
        Compose the service-account JSON payload from individual env‐vars.
        """
        return {
            "type": cls.SA_TYPE,
            "project_id": cls.SA_PROJECT_ID,
            "private_key_id": cls.SA_PRIVATE_KEY_ID,
            "private_key": cls.SA_PRIVATE_KEY,
            "client_email": cls.SA_CLIENT_EMAIL,
            "client_id": cls.SA_CLIENT_ID,
            "auth_uri": cls.SA_AUTH_URI,
            "token_uri": cls.SA_TOKEN_URI,
            "auth_provider_x509_cert_url": cls.SA_AUTH_PROVIDER_X509_CERT_URL,
            "client_x509_cert_url": cls.SA_CLIENT_X509_CERT_URL,
            "universe_domain": cls.SA_UNIVERSE_DOMAIN,
        }