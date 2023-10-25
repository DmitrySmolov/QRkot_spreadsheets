from contextlib import asynccontextmanager, AsyncExitStack

from fastapi_users.exceptions import UserAlreadyExists
from pydantic import EmailStr

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import get_user_db, get_user_manager
from app.schemas.user import UserCreate

get_async_session_context = asynccontextmanager(get_async_session)
get_user_db_context = asynccontextmanager(get_user_db)
get_user_manager_context = asynccontextmanager(get_user_manager)


async def create_user(
        email: EmailStr,
        password: str,
        is_superuser: bool = False
):
    try:
        async with AsyncExitStack() as stack:
            session = await stack.enter_async_context(
                get_async_session_context()
            )
            user_db = await stack.enter_async_context(
                get_user_db_context(session)
            )
            user_manager = await stack.enter_async_context(
                get_user_manager_context(user_db)
            )
            await user_manager.create(
                UserCreate(
                    email=email,
                    password=password,
                    is_superuser=is_superuser
                )
            )
    except UserAlreadyExists:
        pass


async def create_first_superuser():
    if not (settings.first_superuser_email is None or
            settings.first_superuser_password is None):
        await create_user(
            email=settings.first_superuser_email,
            password=settings.first_superuser_password,
            is_superuser=True
        )
