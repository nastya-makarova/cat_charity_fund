from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Text

from app.core.db import Base


class Donation(Base):
    # user_id
    comment = Column(Text)
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    close_date = Column(DateTime)
