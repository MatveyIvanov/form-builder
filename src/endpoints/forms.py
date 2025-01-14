from dependency_injector.wiring import Provide, inject
from fastapi import Depends, Request
from fastapi_versioning import version

from config.di import Container
from schemas.form import Form
from services.interfaces import IBuildForm
from utils.routing import APIRouter

router = APIRouter(prefix="/forms", tags=["forms"])


@router.post("/build/", response_model=Form)
@version(0)
@inject
async def build(
    request: Request,
    build: IBuildForm = Depends(Provide[Container.get_or_build_form.provider]),
) -> Form:
    return await build(fields=dict(request.query_params))
