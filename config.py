from dotenv import load_dotenv
import os
import base64


load_dotenv()

# старый код пока не трогаю
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
credentials_base64 = os.getenv("GOOGLE_CREDENTIALS_JSON")
if credentials_base64:
    with open("credentials.json", "w") as f:
        f.write(base64.b64decode(credentials_base64).decode("utf-8"))

GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE")

DEFAULT_SHEET_RANGE = os.getenv('DEFAULT_SHEET_RANGE')

AWS_BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')
AWS_BUCKET_NAME_REPLICA = os.getenv('AWS_BUCKET_NAME_REPLICA')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')

BITLY_API_KEY = os.getenv('BITLY_API_KEY')

MONGO_DB_URL = os.getenv('MONGODB_URL')
DATABASE_NAME = os.getenv('DATABASE_NAME')

USERS = os.getenv('USERS')

ADMIN_IDS = os.getenv('ADMIN_ID')

WEBHOOK_URL = os.getenv('WEBHOOK_URL')

KASPI_URL = os.getenv('KASPI_URL')

KASPI_API_KEY = os.getenv('KASPI_API_KEY')