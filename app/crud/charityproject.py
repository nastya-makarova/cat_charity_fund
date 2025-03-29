from typing import Optional

from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):

    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession
    ) -> Optional[int]:
        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        return db_project_id.scalars().first()

    async def get_projects_by_completion_rate(
        self,
        session: AsyncSession
    ) -> list[dict[str, int]]:
        time_to_complete = (
            func.julianday(CharityProject.close_date) -
            func.julianday(CharityProject.create_date)
        ).label('time_diff')
        projects = await session.execute(
            select(CharityProject, time_to_complete).where(
                CharityProject.fully_invested == 1
            ).order_by(time_to_complete)
        )
        projects = projects.all()
        return projects


charity_project_crud = CRUDCharityProject(CharityProject)
