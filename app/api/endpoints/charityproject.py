from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import (
    create_charity_project,
    get_project_by_id,
    get_project_id_by_name,
    read_all_projects,
    update_charity_project
)
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB, CharityProjectUpdate


router = APIRouter(
    prefix='/charity_project',
    tags=['Charity Projects']
)


async def check_name_duplicate(
    project_name: str,
    session: AsyncSession,
) -> None:
    project_id = await get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(charity_project.name, session)
    new_project = await create_charity_project(charity_project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    all_projects = await read_all_projects(session)
    return all_projects


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    project = await get_project_by_id(
        project_id, session
    )
    if project is None:
        raise HTTPException(
            status_code=404,
            detail='Пороект не найден'
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    project = await update_charity_project(
        project, obj_in, session
    )
    return project

