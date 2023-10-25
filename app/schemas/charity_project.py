from typing import Optional

from pydantic import BaseModel, conint, Extra, Field, validator

from app.core.config import Constant, Message
from app.schemas.charity_mixins import CharityDBMixin


class CharityProjectBase(BaseModel):
    """Базовая схема проекта."""
    name: Optional[str] = Field(None, max_length=Constant.NAME_FLD_MAX_LEN)
    description: Optional[str]
    full_amount: Optional[conint(gt=0)]

    class Config:
        min_anystr_length = Constant.NAME_FLD_MIN_LEN


class CharityProjectCreate(CharityProjectBase):
    """Схема для создания нового проекта."""
    name: str = Field(..., max_length=Constant.NAME_FLD_MAX_LEN)
    description: str
    full_amount: conint(gt=0)


class CharityProjectUpdate(CharityProjectBase):
    """Схема для обновления существующего проекта."""
    @validator('name')
    def name_cant_be_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError(Message.CHARITY_PROJ_NAME_NOT_NULL)
        return value

    @validator('description')
    def description_cant_be_none(cls, value: Optional[str]):
        if value is None:
            raise ValueError(Message.CHARITY_PROJ_DESCR_NOT_NULL)
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityDBMixin, CharityProjectCreate):
    """Схема для отображения проектов."""
    pass
