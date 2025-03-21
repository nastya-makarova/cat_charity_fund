from datetime import datetime


def investment_process(
    new_item,
    objects
):
    for obj in objects:
        available_amount = min(
            new_item.full_amount - new_item.invested_amount,
            obj.full_amount - obj.invested_amount
        )

        new_item.invested_amount += available_amount
        obj.invested_amount += available_amount

        if new_item.invested_amount == new_item.full_amount:
            new_item.fully_invested = True
            new_item.close_date = datetime.now()

        if obj.invested_amount == obj.full_amount:
            obj.fully_invested = True
            obj.close_date = datetime.now()

    return new_item, objects
