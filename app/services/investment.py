from datetime import datetime
from typing import Union

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Message
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


async def perform_investment(
    session: AsyncSession,
    new_db_obj: Union[CharityProject, Donation]
) -> Union[CharityProject, Donation]:
    """
    Функция распределения средств среди активных проектов и пожертвований.
    """
    try:
        active_donations = await (
            donation_crud.get_active_order_by_create_date(session)
        )
        active_projects = await (
            charity_project_crud.get_active_order_by_create_date(session)
        )
        if not (active_donations or active_projects):
            return
        donation_index = 0
        project_index = 0
        len_active_donations = len(active_donations)
        len_active_projects = len(active_projects)
        while (
            donation_index < len_active_donations and
            project_index < len_active_projects
        ):
            first_active_donation = active_donations[donation_index]
            first_active_project = active_projects[project_index]
            donation_capacity = (
                first_active_donation.full_amount -
                first_active_donation.invested_amount
            )
            project_capacity = (
                first_active_project.full_amount -
                first_active_project.invested_amount
            )
            min_capacity = min(donation_capacity, project_capacity)
            first_active_donation.invested_amount += min_capacity
            first_active_project.invested_amount += min_capacity

            if (
                first_active_donation.invested_amount ==
                first_active_donation.full_amount
            ):
                first_active_donation.fully_invested = True
                first_active_donation.close_date = datetime.now()
                donation_index += 1

            if (
                first_active_project.invested_amount ==
                first_active_project.full_amount
            ):
                first_active_project.fully_invested = True
                first_active_project.close_date = datetime.now()
                project_index += 1
            session.add(first_active_donation)
            session.add(first_active_project)

        await session.commit()
        await session.refresh(new_db_obj)
        return new_db_obj

    except SQLAlchemyError as error:
        await session.rollback()
        raise SQLAlchemyError(Message.INVESTMENT_ERROR) from error
    except Exception as error:
        await session.rollback()
        raise Exception(Message.INVESTMENT_ERROR) from error
