from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_active,
                                check_charity_project_exists,
                                check_charity_project_name_duplicate,
                                check_charity_project_new_full_amount,
                                check_charity_project_not_invested)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.investment import perform_investment
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)

router = APIRouter()


@router.get(
    path='/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session=session)


@router.post(
    path='/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def create_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Создаёт благотворительный проект.
    """
    await check_charity_project_name_duplicate(
        charity_project_name=charity_project.name,
        session=session
    )
    new_charity_project = await charity_project_crud.create(
        obj_in=charity_project,
        session=session
    )
    return await perform_investment(session=session,
                                    new_db_obj=new_charity_project)


@router.delete(
    path='/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Удаляет проект. Нельзя удалить проект, в который уже были инвестированы
     средства, его можно только закрыть.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=project_id, session=session
    )
    check_charity_project_not_invested(charity_project=charity_project)
    return await charity_project_crud.remove(db_obj=charity_project,
                                             session=session)


@router.patch(
    path='/{project_id}',
    response_model=CharityProjectDB,
    dependencies=(Depends(current_superuser),)
)
async def update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Закрытый проект нельзя редактировать; нельзя установить требуемую сумму
     меньше уже вложенной.
    """
    charity_project = await check_charity_project_exists(
        charity_project_id=project_id, session=session
    )
    check_charity_project_active(charity_project=charity_project)
    if obj_in.name is not None:
        await check_charity_project_name_duplicate(
            charity_project_name=obj_in.name,
            session=session
        )
    if obj_in.full_amount is not None:
        check_charity_project_new_full_amount(
            charity_project=charity_project,
            new_full_amount=obj_in.full_amount
        )
    return await charity_project_crud.update(db_obj=charity_project,
                                             obj_in=obj_in,
                                             session=session)
