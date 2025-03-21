from sqlalchemy import Column, String, Text

from app.core.constants import MAX_LENGTH
from app.core.db import ProjectDonationBase


class CharityProject(ProjectDonationBase):
    name = Column(String(MAX_LENGTH), unique=True, nullable=False)
    description = Column(Text, nullable=False)
