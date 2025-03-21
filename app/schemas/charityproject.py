from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator

from app.core.constants import DEFAULT_INVESTED_AMOUNT, MAX_LENGTH, MIN_LENGTH


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=MIN_LENGTH, max_length=MAX_LENGTH)
    description: str = Field(..., min_length=MIN_LENGTH)
    full_amount: PositiveInt = Field(...)


class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        None,
        min_length=MIN_LENGTH,
        max_length=MAX_LENGTH
    )
    description: Optional[str] = Field(None, min_length=MIN_LENGTH)
    full_amount: Optional[PositiveInt]

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(default=DEFAULT_INVESTED_AMOUNT)
    fully_invested: bool = Field(default=False)
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
