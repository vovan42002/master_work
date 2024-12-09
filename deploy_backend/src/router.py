import logging
from fastapi import APIRouter, status, Depends
import schemas
import uuid
from template import save_templated_files
from utils import verify_access_token

from celery_tasks import deploy, uninstall

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/deployments", dependencies=[Depends(verify_access_token)])


@router.post(
    "/{deployment_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DeploymentID,
)
async def start_deployment(
    deployment_id: uuid.UUID,
    deployment: schemas.Deployment,
):
    save_templated_files(
        deployment_id=str(deployment_id),
        installed=True,
        application_name=deployment.application_name,
        version=deployment.version,
        parameters=deployment.parameters,
    )
    deploy.delay(deployment_id)
    return schemas.DeploymentScheduled(
        deployment_id=deployment_id, msg="Deployment started"
    )


@router.delete(
    "/{deployment_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.DeploymentID,
)
async def delete_deployment(
    deployment_id: uuid.UUID,
):
    uninstall.delay(deployment_id)
    return schemas.DeploymentID(deployment_id=deployment_id)
