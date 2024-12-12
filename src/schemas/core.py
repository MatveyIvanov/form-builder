from typing import Self, Set

from pydantic import BaseModel, model_validator

from schemas.types import FormFieldType

DEFAULT_MONGO_FIELDS: Set[str] = {"_id"}


class _MongoModel(BaseModel, extra="allow"):  # type:ignore[call-arg]
    @property
    def fields(self) -> Set[str]:
        return set(self.model_fields)

    @property
    def extra(self) -> Set[str]:
        return set(self.model_extra) - DEFAULT_MONGO_FIELDS

    @model_validator(mode="after")
    def validate_extra_fields(self) -> Self:
        for field in self.extra:
            try:
                FormFieldType(getattr(self, field))
            except ValueError:
                raise ValueError("Invalid field type.")
        return self
