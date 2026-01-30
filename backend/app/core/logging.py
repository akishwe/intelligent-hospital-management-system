import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime

BASE_LOG_DIR = Path("logs")
BASE_LOG_DIR.mkdir(exist_ok=True)

def get_logger(module_name: str) -> logging.Logger:
    module_dir = BASE_LOG_DIR / module_name
    module_dir.mkdir(exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = module_dir / f"{module_name}-{date_str}.log"

    logger = logging.getLogger(f"{module_name}")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding="utf-8"
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger