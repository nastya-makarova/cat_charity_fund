from fastapi import APIRouter

from app.api.endpoints.charityproject import router as project_router
from app.api.endpoints.donation import router as donation_router


main_router = APIRouter()
main_router.include_router(project_router)
main_router.include_router(donation_router)
