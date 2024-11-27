import logging
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from schemas import DeploymentID, DeploymentCreate, DeploymentUpdate, DeploymentStatus

from services.deployment_service import DeploymentsService
from services.app_schema import AppSchemaService
import uuid

logger = logging.getLogger(__name__)

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
    logger.info("Request to create a new deployment")
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
    logger.info(f"Request to delete deployment with id={deployment_id}")
    service = DeploymentsService()
    return await service.delete_deployment(deployment_id=deployment_id)


@router.put("/{deployment_id}", status_code=status.HTTP_200_OK)
async def update_deployment(deployment_id: uuid.UUID, deployment: DeploymentUpdate):
    logger.info(f"Request to update deployment with id={deployment_id}")
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


@router.patch(
    "/{deployment_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=DeploymentID,
)
async def update_deployment_status(deployment_id: uuid.UUID, status: DeploymentStatus):
    logger.info(f"Request to update status for deployment with id={deployment_id}")
    service = DeploymentsService()
    # raise if deployment_id doesn't exist
    deployment = await service.get_deployment_by_id(deployment_id=deployment_id)
    logger.info("Got a proof that deployment exists")
    if deployment.status == status.status:
        logger.info(f"Status of deployment {deployment_id} is already {status}")
        return DeploymentID(deployment_id=deployment_id)
    return await service.update_deployment_status(
        deployment_id=deployment_id,
        status=status,
    )


@router.get(
    "/{deployment_id}/status",
    status_code=status.HTTP_200_OK,
    response_model=DeploymentStatus,
)
async def get_deployment_status(deployment_id: uuid.UUID):
    logger.info(f"Request to get a status for deployment with id={deployment_id}")
    service = DeploymentsService()
    # raise if deployment_id doesn't exist
    deployment = await service.get_deployment_by_id(deployment_id=deployment_id)
    logger.info("Got a proof that deployment exists")
    return DeploymentStatus(
        status=deployment.status,
        info=deployment.info,
    )


@router.get(
    "/{deployment_id}",
    status_code=status.HTTP_200_OK,
    response_model=DeploymentCreate,
)
async def get_deployment(deployment_id: uuid.UUID):
    logger.info(f"Request to get deployment with id={deployment_id}")
    service = DeploymentsService()
    return await service.get_deployment_by_id(deployment_id=deployment_id)
