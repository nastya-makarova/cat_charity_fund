from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(...)


class CharityProjectDB(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt = Field(...)
    invested_amount: int = Field(default=0)
    fully_invested: bool = Field(default=False)
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
