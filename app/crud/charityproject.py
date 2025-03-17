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
