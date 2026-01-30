import logging.config
from pathlib import Path

LOG_DIR = Path("../logs")


def setup_logging() -> None:
    LOG_DIR.mkdir(exist_ok=True)

    logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
