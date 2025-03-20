from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt = Field(...)
    comment: Optional[str]


class DonationDb(DonationCreate):
    id: int
    create_date: datetime = Field(default_factory=datetime.utcnow)
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationDbFull(DonationDb):
    id: int
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
