import logging
from fastapi import status, APIRouter
from schemas import VersionsList, ApplicationsList

from services.applications_service import ApplicationsService


router = APIRouter(prefix="/applications")
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


@router.get("", status_code=status.HTTP_200_OK, response_model=ApplicationsList)
async def get_applications():
    logger.info("Request to get all applications")
    service = ApplicationsService()
    return await service.get_all_applications()


@router.get(
    "/{application_name}/versions",
    status_code=status.HTTP_200_OK,
    response_model=VersionsList,
)
async def get_application_versions(application_name: str):
    logger.info(f"Request to get all {application_name} versions")
    service = ApplicationsService()
    return await service.get_all_versions_by_application_name(
        application_name=application_name
    )
