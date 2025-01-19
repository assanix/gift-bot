import logging
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from config import SPREADSHEET_ID, GOOGLE_CREDENTIALS_FILE

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
logger = logging.getLogger(__name__)


def get_service():
    creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    return service

async def append_to_sheet(values, range_name):
    service = get_service()
    body = {'values': values}

    try:
        request = service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_ID,
            range=range_name,
            valueInputOption='USER_ENTERED',
            insertDataOption='INSERT_ROWS',
            body=body
        )
        response = request.execute()
        logger.info("Данные успешно добавлены в Google Sheets.")
        return response
    except Exception as e:
        logger.error(f"Ошибка при добавлении данных в Google таблицу: {e}")
        return None
