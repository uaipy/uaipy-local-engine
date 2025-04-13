import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler
    file_handler = RotatingFileHandler(LOG_DIR / "app.log", maxBytes=5_000_000, backupCount=5)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
