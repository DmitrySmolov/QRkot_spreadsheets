from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationOwnerView
from app.services.investment import perform_investment

router = APIRouter()


@router.get(
    path='/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=(Depends(current_superuser),)
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.

    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session=session)


@router.post(
    path='/',
    response_model=DonationOwnerView,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(
        obj_in=donation, user=user, session=session
    )
    return await perform_investment(session=session, new_db_obj=new_donation)


@router.get(
    path='/my',
    response_model=list[DonationOwnerView],
    response_model_exclude_none=True
)
async def get_user_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_multi_for_current_user(user=user,
                                                          session=session)
