from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

def generate_token():
    """Manually authenticate Google Drive & save token.json"""
    gauth = GoogleAuth()

    # 🔹 Explicitly load credentials.json
    gauth.LoadClientConfigFile("credentials.json")

    # 🔹 Start the authentication flow
    gauth.LocalWebserverAuth()

    # 🔹 Save token.json
    gauth.SaveCredentialsFile("token.json")
    print("✅ token.json has been saved successfully!")

def test_google_drive_connection():
    """Test Google Drive connection"""
    try:
        gauth = GoogleAuth()

        # 🔹 If token.json exists, load it
        if os.path.exists("token.json"):
            print("🔹 Loading existing token.json...")
            gauth.LoadCredentialsFile("token.json")
        else:
            print("🔹 No token.json found. Generating new token...")
            generate_token()
            gauth.LoadCredentialsFile("token.json")  # Load newly created token

        # 🔹 Check if token expired & refresh if needed
        if gauth.credentials is None:
            print("🔹 No credentials found. Please authenticate.")
            generate_token()
        elif gauth.access_token_expired:
            print("🔹 Token expired. Refreshing...")
            gauth.Refresh()
            gauth.SaveCredentialsFile("token.json")
        else:
            gauth.Authorize()

        # 🔹 Connect to Google Drive
        drive = GoogleDrive(gauth)

        # 🔹 List files in Google Drive root directory
        file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        
        print("✅ Google Drive authentication successful!")
        print(f"🔹 Found {len(file_list)} files in root directory.")

        # 🔹 Print first 5 files
        for file in file_list[:5]:
            print(f"📄 {file['title']} (ID: {file['id']})")

        print("🚀 Google Drive is ready for uploads!")

    except Exception as e:
        print("❌ Google Drive authentication failed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_google_drive_connection()
