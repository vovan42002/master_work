from schemas import ApplicationsList, VersionsList
from database import app_schemas_collection as collection
from fastapi import HTTPException, status


class ApplicationsService:

    @staticmethod
    async def get_all_applications() -> ApplicationsList:
        documents = await collection.distinct(key="application_name")
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There aren't any applications",
            )
        return ApplicationsList(applications=documents)

    @staticmethod
    async def get_all_versions_by_application_name(
        application_name: str,
    ) -> VersionsList:
        documents = await collection.distinct(
            key="version", filter={"application_name": application_name}
        )
        if not documents:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There aren't such an application",
            )
        return VersionsList(versions=documents)
