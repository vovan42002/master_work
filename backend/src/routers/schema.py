import logging
from fastapi import status, APIRouter
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from schemas import (
    AppSchema,
    AppSchemaUpdatedResponse,
    AppSchemaUpdatedResponse,
    ContainersList,
)
from services.app_schema import AppSchemaService

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

security = HTTPBearer()

router = APIRouter(prefix="/schema")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_new_schema(schema: AppSchema):
    logger.info("Request to add new app schema")
    service = AppSchemaService()
    return await service.create_app_schema(app_schema=schema)


@router.get(
    "/{application_name}/{version}",
    response_model=AppSchema,
    status_code=status.HTTP_200_OK,
)
async def get_schema_by_version_and_name(application_name: str, version: str):
    logger.info(f"Request to get {application_name} {version}")
    service = AppSchemaService()
    return await service.get_app_schema_by_version_and_name(
        application_name=application_name,
        version=version,
    )


@router.delete(
    "/{application_name}/{version}",
    response_model=AppSchemaUpdatedResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_schema_by_version_and_name(application_name: str, version: str):
    logger.info(f"Request to delete {application_name} {version}")
    service = AppSchemaService()
    return await service.delete_app_schema_by_version_and_name(
        application_name=application_name,
        version=version,
    )


@router.put(
    "/{application_name}/{version}",
    response_model=AppSchemaUpdatedResponse,
    status_code=status.HTTP_200_OK,
)
async def update_schema_by_version_and_name(
    application_name: str, version: str, containers_list: ContainersList
):
    logger.info(f"Request to update {application_name} {version}")
    service = AppSchemaService()
    return await service.update_app_schema_by_version_and_name(
        app_schema=AppSchema(
            application_name=application_name,
            version=version,
            containers=containers_list.containers,
        )
    )
