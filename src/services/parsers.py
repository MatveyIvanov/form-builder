from typing import Callable, Dict, Iterable

from services import validators
from schemas.types import FormFieldType
from config import settings


TYPE_TO_VALIDATOR: Dict[FormFieldType, Callable[[str], bool]] = {
    FormFieldType.DATE: validators.validate_date,
    FormFieldType.PHONE: validators.validate_phone,
    FormFieldType.EMAIL: validators.validate_email,
    FormFieldType.TEXT: validators.validate_text,
}
FALLBACK_TYPE = FormFieldType.TEXT


def parse_type(
    value: str,
    *,
    priority: Iterable[FormFieldType] = settings.FORM_FIELD_TYPES_PRIORITY
) -> FormFieldType:
    for field_type in priority:
        valid = TYPE_TO_VALIDATOR[field_type](value)
        if valid:
            return field_type

    return FALLBACK_TYPE
