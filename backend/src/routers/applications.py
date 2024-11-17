import logging
from fastapi import status, APIRouter
from schemas import VersionsList, ApplicationsList

from services.applications_service import ApplicationsService


router = APIRouter(prefix="/applications")


@router.get("", status_code=status.HTTP_200_OK, response_model=ApplicationsList)
async def get_applications():
    logging.info("Request to get all applications")
    service = ApplicationsService()
    return await service.get_all_applications()


@router.get(
    "/{application_name}/versions",
    status_code=status.HTTP_200_OK,
    response_model=VersionsList,
)
async def get_application_versions(application_name: str):
    logging.info(f"Request to get all {application_name} versions")
    service = ApplicationsService()
    return await service.get_all_versions_by_application_name(
        application_name=application_name
    )
