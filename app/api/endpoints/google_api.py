from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (set_user_permissions,
                                     spreadsheets_create,
                                     spreadsheets_update_value)

router = APIRouter()


@router.post(
    path='/',
    response_model=list[list[str, str, str]],
    dependencies=(Depends(current_superuser),)
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service)
):
    """Только для суперъюзеров."""
    charity_projects = await (
        charity_project_crud.get_multi_closed_sorted_by_open_delta(
            session=session
        )
    )
    spreadsheet_id = await spreadsheets_create(
        wrapper_services=wrapper_services
    )
    await set_user_permissions(spreadsheet_id=spreadsheet_id,
                               wrapper_services=wrapper_services)
    await spreadsheets_update_value(spreadsheet_id=spreadsheet_id,
                                    charity_projects=charity_projects,
                                    wrapper_services=wrapper_services)
    return charity_projects
