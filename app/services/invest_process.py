from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def investment_process(
    new_item,
    model,
    session: AsyncSession,
):
    available_list = await session.execute(select(model).where(
        model.fully_invested == False
    ).order_by(model.create_date))

    available_list = available_list.scalars().all()

    if not available_list:
        return

    for element in available_list:
        available_amount = min(
            new_item.full_amount - new_item.invested_amount,
            element.full_amount - element.invested_amount
        )

        new_item.invested_amount += available_amount
        element.invested_amount += available_amount

        if new_item.invested_amount == new_item.full_amount:
            new_item.fully_invested = True
            new_item.close_date = datetime.now()

        if element.invested_amount == element.full_amount:
            element.fully_invested = True
            element.close_date = datetime.now()

    await session.commit()
    await session.refresh(new_item)
    for element in available_list:
        await session.refresh(element)
    return new_item
