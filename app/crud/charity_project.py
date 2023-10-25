from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Constant
from app.crud.base import CRUDBase
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


class CRUDCharityProject(CRUDBase):

    async def get_charity_project_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession
    ) -> Optional[CharityProject]:
        db_obj = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project_name
            )
        )
        return db_obj.scalars().first()

    async def update(
        self,
        db_obj: CharityProject,
        obj_in: CharityProjectUpdate,
        session: AsyncSession
    ):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.invested_amount == db_obj.full_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: CharityProject,
        session: AsyncSession
    ) -> CharityProject:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_multi_closed_sorted_by_open_delta(
        self,
        session: AsyncSession
    ) -> list[list[Any]]:
        time_delta = (func.julianday(CharityProject.close_date) -
                      func.julianday(CharityProject.create_date))
        objs = await session.execute(
            select(CharityProject.name,
                   time_delta,
                   CharityProject.description).where(
                CharityProject.fully_invested == True # noqa E712
            ).order_by(time_delta)
        )
        result = []
        for name, delta, description in objs:
            delta_seconds = delta * Constant.SECS_IN_DAY
            delta_timedelta = timedelta(seconds=delta_seconds)
            result.append([name, str(delta_timedelta), description])
        return result


charity_project_crud = CRUDCharityProject(CharityProject)
