from typing import Tuple, Type, TypeVar
from pydantic import TypeAdapter, ValidationError

from schemas import types


T = TypeVar("T")


def validate_date(value: str) -> bool:
    for type in types.DATE_TYPES:
        if _validate(value, type):
            return True
    return False


def validate_phone(value: str) -> bool:
    for type in types.PHONE_TYPES:
        if _validate(value, type):
            return True
    return False


def validate_email(value: str) -> bool:
    for type in types.EMAIL_TYPES:
        if _validate(value, type):
            return True
    return False


def validate_text(value: str) -> bool:
    for type in types.TEXT_TYPES:
        if _validate(value, type):
            return True
    return False


def _validate(value: T, type: Type) -> Tuple[bool, T]:
    try:
        TypeAdapter(type).validate_python(value)
        return True
    except ValidationError as e:
        return False
