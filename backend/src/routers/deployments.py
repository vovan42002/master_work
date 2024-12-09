import logging
import uuid
from fastapi import Path, APIRouter, Depends
from fastapi import status as fastapi_status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse

from adapters.auth_adapter import AuthAdapter
from adapters.deploy_adapter import DeployAdapter
from services.deployment_service import DeploymentsService
from services.app_schema import AppSchemaService
from schemas import (
    ApplicationsList,
    DeploymentID,
    DeploymentCreate,
    DeploymentToDeploy,
    DeploymentUpdate,
    DeploymentStatus,
    UserDeployments,
)
from config import get_settings

security = HTTPBearer()

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

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


@router.post(
    "", status_code=fastapi_status.HTTP_201_CREATED, response_model=DeploymentID
)
async def create_deployment(
    deployment: DeploymentCreate,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info("Request to create a new deployment")
    auth_adapter = AuthAdapter(token=token.credentials)
    user = await auth_adapter.get_user()
    deployment_adjust = deployment.model_copy()
    deployment_adjust.username = user.username
    service = DeploymentsService()
    if await application_version_exists(
        application_name=deployment_adjust.application_name,
        version=deployment_adjust.version,
    ):
        return await service.create_new_deployment(deployment_adjust)
    return JSONResponse(
        status_code=fastapi_status.HTTP_400_BAD_REQUEST,
        content=f"Version {deployment_adjust.version} of app {deployment_adjust.application_name} doesn't exist",
    )


@router.post(
    "/{deployment_id}/deploy",
    status_code=fastapi_status.HTTP_201_CREATED,
    response_model=DeploymentID,
)
async def start_deployment(
    deployment_id: str,
    deployment: DeploymentToDeploy,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info("Request to create a new deployment")
    auth_adapter = AuthAdapter(token=token.credentials)
    deploy_adapter = DeployAdapter(deployment_id=deployment_id)
    await auth_adapter.get_user()
    if await application_version_exists(
        application_name=deployment.application_name,
        version=deployment.version,
    ):
        return await deploy_adapter.start_deployment(deployment=deployment)
    return JSONResponse(
        status_code=fastapi_status.HTTP_400_BAD_REQUEST,
        content=f"Version {deployment.version} of app {deployment.application_name} doesn't exist",
    )


@router.delete("/{deployment_id}", status_code=fastapi_status.HTTP_200_OK)
async def delete_deployment(
    deployment_id: uuid.UUID,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info(f"Request to delete deployment with id={deployment_id}")
    service = DeploymentsService()
    auth_adapter = AuthAdapter(token=token.credentials)
    user = await auth_adapter.get_user()
    # raise if deployment_id doesn't exist
    deployment = await service.get_deployment_by_id(deployment_id=deployment_id)
    if deployment.username != user.username:
        logger.warning(
            f"User {user.username} wants to delete deployment of the user {deployment.username}"
        )
        return JSONResponse(
            status_code=fastapi_status.HTTP_403_FORBIDDEN,
            content=f"You can get change a deployment {deployment_id}, because you are not an owner",
        )
    deploy_adapter = DeployAdapter(deployment_id=deployment_id)
    await deploy_adapter.uninstall_deployment()
    await service.delete_deployment(deployment_id=deployment_id)
    return DeploymentID(deployment_id=deployment_id)


@router.put("/{deployment_id}", status_code=fastapi_status.HTTP_200_OK)
async def update_deployment(
    deployment_id: uuid.UUID,
    deployment: DeploymentUpdate,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info(f"Request to update deployment with id={deployment_id}")
    service = DeploymentsService()
    auth_adapter = AuthAdapter(token=token.credentials)
    user = await auth_adapter.get_user()
    # raise if deployment_id doesn't exist
    current_deployment_data = await service.get_deployment_by_id(
        deployment_id=deployment_id
    )
    if current_deployment_data.username != user.username:
        logger.warning(
            f"User {user.username} wants to acess deployment of the user {current_deployment_data.username}"
        )
        return JSONResponse(
            status_code=fastapi_status.HTTP_403_FORBIDDEN,
            content=f"You can get change a deployment {deployment_id}, because you are not an owner",
        )
    if await application_version_exists(
        application_name=current_deployment_data.application_name,
        version=deployment.version,
    ):
        logger.info(
            f"Application version {deployment.version} of {current_deployment_data.application_name} exists"
        )
        logger.info(f"Trying to update {deployment_id}")
        return await service.update_deployment(
            deployment_id=deployment_id, new_deployment=deployment
        )
    logger.error(
        f"Version {deployment.version} of app {current_deployment_data.application_name} doesn't exist"
    )
    return JSONResponse(
        status_code=fastapi_status.HTTP_400_BAD_REQUEST,
        content=f"Version {deployment.version} of app {current_deployment_data.application_name} doesn't exist",
    )


@router.patch(
    "/{deployment_id}/status",
    status_code=fastapi_status.HTTP_200_OK,
    response_model=DeploymentID,
)
async def update_deployment_status(
    deployment_id: uuid.UUID,
    status: DeploymentStatus,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info(f"Request to update status for deployment with id={deployment_id}")
    service = DeploymentsService()
    deployment = await service.get_deployment_by_id(deployment_id=deployment_id)
    logger.info("Got a proof that deployment exists")
    if token.credentials != get_settings().application.access_token:
        auth_adapter = AuthAdapter(token=token.credentials)
        user = await auth_adapter.get_user()
        if deployment.username != user.username:
            logger.warning(
                f"User {user.username} wants to acess deployment of the user {deployment.username}"
            )
            return JSONResponse(
                status_code=fastapi_status.HTTP_403_FORBIDDEN,
                content=f"You can get change a status of the deployment {deployment_id}, because you are not an owner",
            )
    if deployment.status == status.status:
        logger.info(f"Status of deployment {deployment_id} is already {status}")
        return DeploymentID(deployment_id=deployment_id)
    return await service.update_deployment_status(
        deployment_id=deployment_id,
        status=status,
    )


@router.get(
    "/{deployment_id}/status",
    status_code=fastapi_status.HTTP_200_OK,
    response_model=DeploymentStatus,
)
async def get_deployment_status(
    deployment_id: uuid.UUID,
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info(f"Request to get a status for deployment with id={deployment_id}")
    service = DeploymentsService()
    auth_adapter = AuthAdapter(token=token.credentials)
    user = await auth_adapter.get_user()
    # raise if deployment_id doesn't exist
    deployment = await service.get_deployment_by_id(deployment_id=deployment_id)
    if deployment.username != user.username:
        logger.warning(
            f"User {user.username} wants to acess deployment of the user {deployment.username}"
        )
        return JSONResponse(
            status_code=fastapi_status.HTTP_403_FORBIDDEN,
            content="You can get a status of the deployment, because it's not yours",
        )
    logger.info("Got a proof that deployment exists")
    return DeploymentStatus(
        status=deployment.status,
        info=deployment.info,
    )


@router.get(
    "/my", status_code=fastapi_status.HTTP_200_OK, response_model=UserDeployments
)
async def get_user_applications(
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logging.info("Request to get all user deployments (applications)")
    auth_adapter = AuthAdapter(token=token.credentials)
    user = await auth_adapter.get_user()
    service = DeploymentsService()
    return await service.get_all_user_deployments(username=user.username)


@router.get(
    "/{deployment_id}",
    status_code=fastapi_status.HTTP_200_OK,
    response_model=DeploymentCreate,
)
async def get_deployment(
    deployment_id: uuid.UUID = Path(..., description="Deployment ID"),
    token: HTTPAuthorizationCredentials = Depends(security),
):
    logger.info(f"Request to get deployment with id={deployment_id}")
    service = DeploymentsService()
    auth_adapter = AuthAdapter(token=token.credentials)
    user = await auth_adapter.get_user()
    deployment = await service.get_deployment_by_id(deployment_id=deployment_id)
    if deployment.username != user.username:
        logger.warning(
            f"User {user.username} wants to acess deployment of the user {deployment.username}"
        )
        return JSONResponse(
            status_code=fastapi_status.HTTP_403_FORBIDDEN,
            content="You can get a status of the deployment, because it's not yours",
        )
    return deployment
