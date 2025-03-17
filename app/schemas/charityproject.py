from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(...)

    @validator('full_amount')
    def check_full_amount_bigger_than_null(cls, value):
        if value <= 0:
            raise ValueError('Tребуемая сумма должна быть больше 0')

        return value
