from typing import Dict, Iterable

from schemas.types import FormFieldType
from services.interfaces import IValidateValue


def parse_type(
    value: str,
    *,
    priority: Iterable[FormFieldType] = ...,  # type:ignore[assignment]
    type_to_validator: Dict[
        FormFieldType, IValidateValue
    ] = ...,  # type:ignore[assignment]
    fallback_type: FormFieldType = ...,  # type:ignore[assignment]
) -> FormFieldType:
    for field_type in priority:
        try:
            if type_to_validator[field_type](value):
                return field_type
        except KeyError:
            continue

    return fallback_type
