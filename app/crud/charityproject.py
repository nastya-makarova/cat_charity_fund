from typing import Optional

from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectCreate


async def create_charity_project(
    new_project: CharityProjectCreate
) -> CharityProject:
    new_project_data = new_project.dict()
    db_new_project = CharityProject(**new_project_data)
    async with AsyncSessionLocal() as session:
        session.add(db_new_project)
        await session.commit()
        await session.refresh(db_new_project)
    return db_new_project


async def get_project_id_by_name(project_name: str) -> Optional[int]:
    async with AsyncSessionLocal() as session:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id
