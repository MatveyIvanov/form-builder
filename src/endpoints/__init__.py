from typing import Tuple

from endpoints.forms import router as forms_router
from utils.routing import APIRouter


def get_routers() -> Tuple[APIRouter]:
    return (forms_router,)
