from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Text, ForeignKey

from app.core.db import Base


class Donation(Base):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
