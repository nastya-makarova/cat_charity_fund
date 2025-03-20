from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import ProjectDonationBase


class Donation(ProjectDonationBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
