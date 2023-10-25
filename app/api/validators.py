from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Message
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_charity_project_name_duplicate(
    charity_project_name: str,
    session: AsyncSession
) -> None:
    """Валидатор имени создаваемого проекта на дупликаты."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name=charity_project_name,
        session=session
    )
    if charity_project is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Message.CHARITY_PROJ_NAME_EXISTS
        )


async def check_charity_project_exists(
    charity_project_id: int,
    session: AsyncSession
) -> CharityProject:
    """Валидатор на наличие проекта в БД по id."""
    charity_project = await charity_project_crud.get(
        obj_id=charity_project_id, session=session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=Message.CHARITY_PROJ_NOT_FOUND
        )
    return charity_project


def check_charity_project_not_invested(
    charity_project: CharityProject
) -> None:
    """Валидатор проекта на наличие внесённых среств."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Message.CHARITY_PROJ_INVESTED
        )


def check_charity_project_active(
    charity_project: CharityProject
) -> None:
    """Валидатор проекта на его состояние (открыт/закрыт)."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Message.CHARITY_PROJ_CLOSED
        )


def check_charity_project_new_full_amount(
    charity_project: CharityProject,
    new_full_amount: int
) -> None:
    """Валидатор нового значения full_amount изменяемого проекта."""
    if new_full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=Message.CHARITY_AMOUNTS_ERROR
        )
