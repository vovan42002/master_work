import logging
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from schemas import DeploymentID, DeploymentCreate, DeploymentUpdate, ApplicationsList

from services.deployment_service import DeploymentsService
from services.app_schema import AppSchemaService
from services.applications_service import ApplicationsService
import uuid


router = APIRouter(prefix="/deployments")


async def application_version_exists(application_name: str, version: str) -> bool:
    app_schema_service = AppSchemaService()
    return (
        await app_schema_service.get_app_schema_by_version_and_name(
            application_name=application_name,
            version=version,
        )
        is not None
    )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DeploymentID)
async def create_deployment(deployment: DeploymentCreate):
    logging.info("Request to create a new deployment")
    service = DeploymentsService()
    if await application_version_exists(
        application_name=deployment.application_name,
        version=deployment.version,
    ):
        return await service.create_new_deployment(deployment)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=f"Version {deployment.version} of app {deployment.application_name} doesn't exist",
    )


@router.delete("/{deployment_id}", status_code=status.HTTP_200_OK)
async def delete_deployment(deployment_id: uuid.UUID):
    logging.info(f"Request to delete deployment with id={deployment_id}")
    service = DeploymentsService()
    return await service.delete_deployment(deployment_id=deployment_id)


@router.put("/{deployment_id}", status_code=status.HTTP_200_OK)
async def update_deployment(deployment_id: uuid.UUID, deployment: DeploymentUpdate):
    logging.info(f"Request to update deployment with id={deployment_id}")
    service = DeploymentsService()
    current_deployment_data = await service.get_deployment_by_id(
        deployment_id=deployment_id
    )
    if await application_version_exists(
        application_name=current_deployment_data.application_name,
        version=deployment.version,
    ):
        return await service.update_deployment(
            deployment_id=deployment_id, new_deployment=deployment
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=f"Version {deployment.version} of app {current_deployment_data.application_name} doesn't exist",
    )
