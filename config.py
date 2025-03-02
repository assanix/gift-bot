from dotenv import load_dotenv
import os
import base64
from typing import Optional, List
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    SPREADSHEET_ID: str
    GOOGLE_CREDENTIALS_FILE: str = "./credentials.json"
    GOOGLE_CREDENTIALS_JSON: Optional[str] = None
    DEFAULT_SHEET_RANGE: str = "Лист1!A2"
    AWS_BUCKET_NAME: str
    AWS_BUCKET_NAME_REPLICA: str
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_REGION: str
    BITLY_API_KEY: str
    MONGODB_URL: str
    DATABASE_NAME: str
    USERS: str
    ADMIN_ID: str
    WEBHOOK_URL: str
    KASPI_URL: str
    KASPI_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
    def process_credentials(self):
        if self.GOOGLE_CREDENTIALS_JSON:
            try:
                credentials_json = base64.b64decode(self.GOOGLE_CREDENTIALS_JSON).decode("utf-8")
                with open(self.GOOGLE_CREDENTIALS_FILE, "w") as f:
                    f.write(credentials_json)
                print(f"Credentials written to {self.GOOGLE_CREDENTIALS_FILE}")
            except Exception as e:
                print(f"Error writing credentials file: {e}")
    
    def get_users_list(self) -> List[int]:
        return [int(user_id.strip()) for user_id in self.USERS.split(",") if user_id.strip()]
    
    def get_admin_ids_list(self) -> List[int]:
        return [int(admin_id.strip()) for admin_id in self.ADMIN_ID.split(",") if admin_id.strip()]


settings = Settings()
settings.process_credentials()


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