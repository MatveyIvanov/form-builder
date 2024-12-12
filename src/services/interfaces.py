from typing import Any, Dict, Iterable, Protocol, Type

from motor.motor_asyncio import AsyncIOMotorClient

from schemas.form import Form
from schemas.types import FormFieldMapping, FormFieldType


class IValidateType(Protocol):
    def __call__(self, value: Any, type: Type) -> bool: ...


class IValidateValue(Protocol):
    def __call__(
        self,
        value: Any,
        *,
        types: Iterable[Type] = ...,
        validate_type: IValidateType = ...,
    ) -> bool: ...


class IParseType(Protocol):
    def __call__(
        self,
        value: Any,
        *,
        priority: Iterable[FormFieldType] = ...,
        type_to_validator: Dict[FormFieldType, IValidateValue] = ...,
        fallback_type: FormFieldType = ...,
    ) -> FormFieldType: ...


class IBuildForm(Protocol):
    async def __call__(
        self,
        fields: FormFieldMapping,
        *,
        mongo: AsyncIOMotorClient = ...,
    ) -> Form: ...
