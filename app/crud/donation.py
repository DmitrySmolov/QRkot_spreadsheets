from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonation(CRUDBase):

    async def get_multi_for_current_user(
        self,
        user: User,
        session: AsyncSession
    ) -> list[Donation]:
        db_objs = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
