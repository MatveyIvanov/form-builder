from typing import List, TypedDict

from pydantic import BaseModel

from schemas.core import _MongoModel
from schemas.types import FormFieldType


class Form(_MongoModel):
    name: str


class FormFieldMongo(BaseModel):
    name: str
    value: FormFieldType


class FormMongo(BaseModel):
    name: str
    fields: List[FormFieldMongo]


class FormFieldMongoDict(TypedDict):
    name: str
    value: FormFieldType


class FormMongoDict(TypedDict):
    name: str
    fields: List[FormFieldMongoDict]
