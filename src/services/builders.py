from typing import List

from motor.motor_asyncio import AsyncIOMotorClient

from schemas.types import FormFieldMapping
from config import settings
from schemas.form import Form
from schemas.parse import ParsedFormField
from services.interfaces import IParseType


async def get_or_build_form(
    fields: FormFieldMapping,
    *,
    mongo: AsyncIOMotorClient = ...,
    parse_type: IParseType = ...,
) -> Form:
    parsed: List[ParsedFormField] = []
    for name, value in fields.items():
        parsed.append(
            ParsedFormField(
                name=name,
                type=parse_type(value),
            )
        )
    cursor = (
        mongo.get_database(settings.DB_NAME)
        .get_collection(settings.MONGO_FORMS_COLLECTION)
        .find(
            {
                "$and": [
                    {
                        "$or": [
                            {field.name: {"$exists": False}},
                            {field.name: field.type},
                        ]
                    }
                    for field in parsed
                ]
            }
        )
        .sort("name")
    )
    result = await cursor.to_list()
    if result:
        return Form(name=result[0]["name"])
    return Form(name="", **{field.name: field.type for field in parsed})
