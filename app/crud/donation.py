from app.crud.base import CRUDBase
from app.models.donation import Donation


class CRUDDonation(CRUDBase):
    async def get_my_donation(self):
        pass


donation_crud = CRUDDonation(Donation)
