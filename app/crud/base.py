from typing import Optional, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation, User
from app.schemas.charity_project import CharityProjectCreate
from app.schemas.donation import DonationCreate


class CRUDBase:

    def __init__(
        self,
        model: Union[CharityProject, Donation]
    ) -> None:
        self.model = model

    async def get(
        self,
        obj_id: int,
        session: AsyncSession
    ) -> Union[CharityProject, Donation]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: Union[CharityProjectCreate, DonationCreate],
        session: AsyncSession,
        user: Optional[User] = None
    ) -> Union[CharityProject, Donation]:
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get_active_order_by_create_date(
        self,
        session: AsyncSession
    ) -> list[Union[CharityProject, Donation]]:
        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == False # noqa E712
            ).order_by('create_date')
        )
        db_obj = db_objs.scalars().all()
        return db_obj
