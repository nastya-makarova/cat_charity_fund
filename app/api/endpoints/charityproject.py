from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_closed_projects,
    check_for_delete,
    check_full_amount_to_update,
    check_name_duplicate,
    check_project_exist,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.crud.donation import donation_crud
from app.schemas.charityproject import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.invest_process import investment_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)

    new_project = await charity_project_crud.create(charity_project, session)
    available_donations = await donation_crud.get_not_closed_objects(session)

    updated_project, updated_donations = investment_process(
        new_item=new_project, objects=available_donations
    )
    await charity_project_crud.save_investing_updates(
        new_item=updated_project, objects=updated_donations, session=session
    )
    return updated_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_projects(
    session: AsyncSession = Depends(get_async_session),
):
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    project = await check_project_exist(
        project_id, session
    )

    await check_closed_projects(project_id, session)

    if obj_in.full_amount:
        if obj_in.full_amount == project.invested_amount:
            project.close_date = datetime.now()
            project.fully_invested = True
        await check_full_amount_to_update(
            obj_in, project_id, session
        )

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)

    return await charity_project_crud.update(
        project, obj_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def remove_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""
    project = await check_project_exist(
        project_id, session
    )
    await check_for_delete(project_id, session)

    return await charity_project_crud.remove(
        project, session
    )
