from fastapi import APIRouter

from app.api.endpoints import (charityproject_router, donation_router,
                               google_api_router, user_router)
from app.core.config import Constant

main_router = APIRouter()

main_router.include_router(
    router=charityproject_router,
    prefix=Constant.CHARITY_PROJ_ENDPOINTS_PREFIX,
    tags=Constant.CHARITY_PROJ_ENDPOINTS_TAGS
)
main_router.include_router(
    router=donation_router,
    prefix=Constant.DONATION_ENDPOINTS_PREFIX,
    tags=Constant.DONATION_ENDPOINTS_TAGS
)
main_router.include_router(
    router=google_api_router,
    prefix=Constant.GOOGLE_ENDPOINTS_PREFIX,
    tags=Constant.GOOGLE_ENDPOINTS_TAGS
)
main_router.include_router(user_router)
