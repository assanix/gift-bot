import logging

import requests
from config import ADMIN_IDS, WEBHOOK_URL

LOG_FILE = "bot_logs.log"
ADMIN_IDS = [int(chat_id) for chat_id in ADMIN_IDS.split(",")]


class WebhookHandler(logging.Handler):
    def emit(self, record):
        log_entry = self.format(record)
        for chat_id in ADMIN_IDS:
            try:
                response = requests.post(
                    WEBHOOK_URL,
                    json={"chat_id": chat_id, "text": log_entry},
                )
                if response.status_code != 200:
                    print(f"Ошибка при отправке вебхука ({chat_id}): {response.status_code}, {response.text}")
            except Exception as e:
                print(f"Ошибка отправки уведомления для {chat_id}: {e}")