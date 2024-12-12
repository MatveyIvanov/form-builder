from typing import Any, Iterable, Type, TypeVar

from pydantic import TypeAdapter, ValidationError

from services.interfaces import IValidateType

T = TypeVar("T")


def validate_value_by_types(
    value: Any,
    *,
    types: Iterable[Type] = ...,  # type:ignore[assignment]
    validate_type: IValidateType = ...,  # type:ignore[assignment]
) -> bool:
    for type in types:
        if validate_type(value, type):
            return True
    return False


def validate_type_with_pydantic(value: Any, type: Type) -> bool:
    try:
        TypeAdapter(type).validate_python(value)
        return True
    except ValidationError:
        return False
