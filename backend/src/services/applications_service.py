from schemas import ApplicationsList, VersionsList
from models import Application
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class ApplicationsService:

    @staticmethod
    async def get_all_applications() -> ApplicationsList:
        documents = await Application.get_motor_collection().distinct(
            key="application_name"
        )
        if not documents:
            logger.warning(f"There aren't any applications in the database")
            documents = []
        return ApplicationsList(applications=documents)

    @staticmethod
    async def get_all_versions_by_application_name(
        application_name: str,
    ) -> VersionsList:
        documents = await Application.get_motor_collection().distinct(
            key="version", filter={"application_name": application_name}
        )
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There aren't such an application",
            )
        return VersionsList(versions=documents)
