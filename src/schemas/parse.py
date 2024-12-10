from pydantic import BaseModel

from schemas.types import FormFieldType


class ParsedFormField(BaseModel):
    name: str
    type: FormFieldType
