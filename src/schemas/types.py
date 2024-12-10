import re
from enum import StrEnum
from datetime import date
from typing import Annotated

from pydantic import EmailStr, StringConstraints
from pydantic_extra_types.phone_numbers import PhoneNumber


RU_DATE_REGEX = re.compile(
    r"^(3[01]|[12][0-9]|0?[1-9])(\.)(1[0-2]|0?[1-9])\2([0-9]{2})?[0-9]{2}$"
)


class FormFieldType(StrEnum):
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    DATE = "DATE"
    TEXT = "TEXT"


class RuPhoneNumber(PhoneNumber):
    supported_regions = ["ru"]


EMAIL_TYPES = [EmailStr]
PHONE_TYPES = [RuPhoneNumber]
DATE_TYPES = [
    date,
    Annotated[str, StringConstraints(pattern=RU_DATE_REGEX)],
]
TEXT_TYPES = [str]
