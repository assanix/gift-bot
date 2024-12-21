import base64

from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
credentials_base64 = os.getenv("GOOGLE_CREDENTIALS_JSON")
if credentials_base64:
    with open("credentials.json", "w") as f:
        f.write(base64.b64decode(credentials_base64).decode("utf-8"))

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

DEFAULT_SHEET_RANGE = os.getenv('DEFAULT_SHEET_RANGE')

AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

BITLY_API_KEY = os.getenv('BITLY_API_KEY')

MONGO_DB_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')