from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings
from schemas import types
from services import builders, parsers, validators


class Container(containers.DeclarativeContainer):
    mongo = providers.Object(
        AsyncIOMotorClient(
            f"mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/"  # noqa:E501
        )
    )

    validate_type_with_pydantic = providers.Callable(
        validators.validate_type_with_pydantic,
    )

    validate_date = providers.Callable(
        validators.validate_value_by_types,
        types=types.DATE_TYPES,
        validate_type=validate_type_with_pydantic.provider,
    )
    validate_phone = providers.Callable(
        validators.validate_value_by_types,
        types=types.PHONE_TYPES,
        validate_type=validate_type_with_pydantic.provider,
    )
    validate_email = providers.Callable(
        validators.validate_value_by_types,
        types=types.EMAIL_TYPES,
        validate_type=validate_type_with_pydantic.provider,
    )
    validate_text = providers.Callable(
        validators.validate_value_by_types,
        types=types.TEXT_TYPES,
        validate_type=validate_type_with_pydantic.provider,
    )

    type_to_validator = providers.Object(
        {
            types.FormFieldType.DATE: validate_date,
            types.FormFieldType.PHONE: validate_phone,
            types.FormFieldType.EMAIL: validate_email,
            types.FormFieldType.TEXT: validate_text,
        }
    )

    parse_type = providers.Callable(
        parsers.parse_type,
        priority=settings.FORM_FIELD_TYPES_PRIORITY,
        type_to_validator=type_to_validator,
        fallback_type=types.FormFieldType.TEXT,
    )

    get_or_build_form = providers.Callable(
        builders.get_or_build_form,
        mongo=mongo,
        parse_type=parse_type.provider,
    )


__container = Container()


def get_di_container() -> Container:
    return __container
