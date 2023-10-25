from datetime import datetime
from typing import Optional

from pydantic import BaseModel, conint, Field


class CharityDBMixin(BaseModel):
    """
    Миксина для общих полей схем полного отображения данных проектов и
     пожервований.
    """
    id: int
    invested_amount: conint(ge=0) = Field(default=0)
    fully_invested: bool = Field(default=False)
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
