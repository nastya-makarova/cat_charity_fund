from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, Field


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]


class DonationDb(BaseModel):
    id: int
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDbFull(BaseModel):
    id: int
    user_id: Optional[int]
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]
    invested_amount: int
    fully_invested: bool
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
