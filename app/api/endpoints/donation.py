from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.schemas.donation import DonationCreate, DonationDb


router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDb],
    response_model_exclude_none=True
)
async def get_all_dontions(
    session: AsyncSession = Depends(get_async_session)
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDb,
    response_model_exclude_none=True,
)
async def create_new_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session)
):
    new_donation = await donation_crud.create(donation, session)
    return new_donation

