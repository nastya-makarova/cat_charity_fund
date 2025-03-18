from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charityproject import (
    create_charity_project,
    get_project_id_by_name,
    read_all_projects
)
from app.schemas.charityproject import CharityProjectCreate, CharityProjectDB


router = APIRouter(
    prefix='/charity_project',
    tags=['Charity Projects']
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
    project_id = await get_project_id_by_name(charity_project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )
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
