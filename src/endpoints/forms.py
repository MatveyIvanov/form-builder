from typing import List
from fastapi import Depends, Request
from fastapi_versioning import version
from dependency_injector.wiring import Provide, inject
from motor.motor_asyncio import AsyncIOMotorClient

from config.di import Container
from config import settings
from schemas.form import Form
from schemas.parse import ParsedFormField
from schemas.types import FormFieldType
from services.parsers import parse_type
from utils.routing import APIRouter

router = APIRouter(prefix="/forms", tags=["tags"])


@router.post("/build/")
@version(0)
@inject
async def build(
    request: Request,
    mongo: AsyncIOMotorClient = Depends(Provide[Container.mongo]),
):
    fields = dict(request.query_params)
    print(fields)
    parsed: List[ParsedFormField] = []
    for name, value in fields.items():
        parsed.append(
            ParsedFormField(
                name=name,
                type=parse_type(value),
            )
        )
    print(parsed)
    try:
        # result = (
        #     await mongo.get_database(settings.DB_NAME)
        #     .get_collection("forms")
        #     .insert_one({"name": "form", "field1": "PHONE", "field2": "TEXT"})
        # )
        # print(result)

        await mongo.get_database(settings.DB_NAME).get_collection(
            settings.MONGO_FORMS_COLLECTION
        ).delete_many({"name": {"$exists": True}})

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
        )
        result = await cursor.to_list()
        print(result)
        if result:
            return Form(name=result[0]["name"])

        return Form(name="", **{field.name: field.type for field in parsed})
    except Exception as e:
        print(str(e))
    return {}
