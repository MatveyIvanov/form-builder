import os
from typing import Tuple

from schemas.types import FormFieldType

DB_USER: str = os.environ.get("DB_USER", "")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")
DB_NAME: str = os.environ.get("DB_NAME", "")
DB_HOST: str = os.environ.get("DB_HOST", "")
DB_PORT: int = int(os.environ.get("DB_PORT", "-1"))
DATABASE_URL: str = os.environ.get("DATABASE_URL", "")

TIMEZONE = os.environ.get("TIMEZONE")

DEBUG = bool(int(os.environ.get("DEBUG", 0)))

LOGGING_MAX_BYTES = int(os.environ.get("LOGGING_MAX_BYTES", 1024 * 3))
LOGGING_BACKUP_COUNT = int(os.environ.get("LOGGING_BACKUP_COUNT", 1))
LOGGING_LOGGERS = os.environ.get("LOGGING_LOGGERS", "").split(",")
LOGGING_SENSITIVE_FIELDS = os.environ.get("LOGGING_SENSITIVE_FIELDS", "").split(",")
LOGGING_PATH = "/logs"

PORT = os.environ.get("ASGI_PORT")

# Mongo
MONGO_FORMS_COLLECTION: str = "forms"

# Validation
FORM_FIELD_TYPES_PRIORITY: Tuple[FormFieldType, ...] = (
    FormFieldType.DATE,
    FormFieldType.PHONE,
    FormFieldType.EMAIL,
    FormFieldType.TEXT,
)
