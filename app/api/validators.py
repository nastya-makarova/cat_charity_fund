from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charity_project_crud
from app.models.charityproject import CharityProject
from app.schemas.charityproject import CharityProjectUpdate


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_project_exist(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Пороект не найден'
        )
    return project


async def check_for_delete(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if project.invested_amount != 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )
    return project


async def check_full_amount_to_update(
    obj_in: CharityProjectUpdate,
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if obj_in.full_amount <= project.invested_amount:
        raise HTTPException(
            status_code=400,
            detail='Нелья установить значение full_amount меньше уже вложенной суммы.'
        )
    return project


async def check_closed_projects(
    project_id: int,
    session: AsyncSession
) -> CharityProject:
    project = await charity_project_crud.get(
        project_id, session
    )
    if project.fully_invested is True:
        raise HTTPException(
            status_code=400,
            detail='Нелья изменять закрытые проекты.'
        )
    return project
