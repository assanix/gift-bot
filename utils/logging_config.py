import logging
import os

from handlers.webhook import WebhookHandler

LOG_FILE = "bot_logs.log"


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    log_path = os.path.join("logs", LOG_FILE)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_path, encoding="utf-8"),
            logging.StreamHandler()
        ],
    )

    webhook_handler = WebhookHandler()
    webhook_handler.setLevel(logging.ERROR)  # Уведомления только для ERROR и выше
    webhook_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
    logging.getLogger().addHandler(webhook_handler)

    logging.info("Логирование настроено. Логи записываются в %s", log_path)
