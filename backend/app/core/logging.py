import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from datetime import datetime
import json

BASE_LOG_DIR = Path("logs")
BASE_LOG_DIR.mkdir(exist_ok=True)


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "module": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "extra_fields"):
            log_record.update(record.extra_fields)
        return json.dumps(log_record)


def get_logger(module_name: str, audit: bool = False) -> logging.Logger:
    module_dir = BASE_LOG_DIR / module_name
    module_dir.mkdir(exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = module_dir / f"{module_name}-{'audit-' if audit else ''}{date_str}.log"

    logger = logging.getLogger(f"{module_name}{'-audit' if audit else ''}")
    logger.setLevel(logging.DEBUG if not audit else logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file,
            maxBytes=5 * 1024 * 1024,
            backupCount=10 if audit else 5,
            encoding="utf-8",
        )
        if audit:
            handler.setFormatter(JSONFormatter())
        else:
            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )
            handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger