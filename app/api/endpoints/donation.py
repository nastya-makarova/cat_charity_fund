from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import DonationCreate, DonationDb, DonationDbFull
from app.services.invest_process import investment_process

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDbFull],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_dontions(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDb,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """Для авторизированных пользователей."""
    new_donation = await donation_crud.create(donation, session, user)
    await investment_process(
        session=session,
        new_item=new_donation,
        model=CharityProject
    )
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationDb],
    response_model_exclude_none=True,
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получает список всех пожертвований для текущего пользователя."""
    donations = await donation_crud.get_by_user(
        session=session, user=user
    )
    return donations
