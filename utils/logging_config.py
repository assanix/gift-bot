import logging
import os

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
    logging.info("Логирование настроено. Логи записываются в %s", log_path)
