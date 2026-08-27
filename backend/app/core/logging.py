import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        for key in ("path", "method", "status_code", "patient_code", "analysis_code", "nct_id", "step"):
            if hasattr(record, key):
                payload[key] = getattr(record, key)
        return json.dumps(payload)


def configure_logging(debug: bool = True) -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG if debug else logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
