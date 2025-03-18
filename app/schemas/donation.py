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
