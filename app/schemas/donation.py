from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint

from app.schemas.charity_mixins import CharityDBMixin


class DonationCreate(BaseModel):
    """Схема для создания нового пожертвования."""
    full_amount: conint(gt=0)
    comment: Optional[str]


class DonationOwnerView(DonationCreate):
    """Схема для просмотра пожертвований его создателем (упрощённый)."""
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(CharityDBMixin, DonationCreate):
    """Схема для просмотра пожертвований администратором (полный)."""
    user_id: int
