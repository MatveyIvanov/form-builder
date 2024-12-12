from typing import Dict, List

from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from schemas.form import Form, FormMongoDict
from schemas.parse import ParsedFormField
from schemas.types import FormFieldMapping
from services.interfaces import IParseType


async def get_or_build_form(
    fields: FormFieldMapping,
    *,
    mongo: AsyncIOMotorClient = ...,  # type:ignore[assignment]
    parse_type: IParseType = ...,  # type:ignore[assignment]
) -> Form:
    parsed: Dict[str, ParsedFormField] = {}
    for name, value in fields.items():
        parsed[name] = ParsedFormField(
            name=name,
            type=parse_type(value),
        )

    forms_with_mathing_fields = await _get_forms_with_matching_fields(fields, mongo)
    if not forms_with_mathing_fields:
        return Form(name="", **{field.name: field.type for field in parsed.values()})

    # TODO: I'm sure this can be done with mongo,
    # but haven't figured out how yet.
    for form in forms_with_mathing_fields:
        for field in form["fields"]:
            if field["value"] != parsed[field["name"]].type:
                break
        else:
            return Form(name=form["name"])

    return Form(name="", **{field.name: field.type for field in parsed.values()})


async def _get_forms_with_matching_fields(
    fields: FormFieldMapping,
    mongo: AsyncIOMotorClient,
) -> List[FormMongoDict]:
    return (
        await mongo.get_database(settings.DB_NAME)
        .get_collection(settings.MONGO_FORMS_COLLECTION)
        .aggregate(
            [
                {
                    "$match": {
                        "fields": {
                            "$not": {
                                "$all": [
                                    {
                                        "$elemMatch": {
                                            "name": {"$nin": list(fields.keys())}
                                        }
                                    },
                                ]
                            },
                        },
                    }
                },
            ]
        )
        .to_list()
    )
