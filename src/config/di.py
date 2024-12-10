from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient

from config import settings


class Container(containers.DeclarativeContainer):
    mongo = providers.Object(
        AsyncIOMotorClient(
            f"mongodb://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/"
        )
    )


__container = Container()


def get_di_container() -> Container:
    return __container
