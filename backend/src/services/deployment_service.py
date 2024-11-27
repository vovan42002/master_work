from schemas import DeploymentCreate, DeploymentID, DeploymentUpdate, DeploymentStatus
from fastapi import HTTPException, status
from models import Deployment
import uuid
from datetime import datetime


class DeploymentsService:

    @staticmethod
    async def create_new_deployment(deployment: DeploymentCreate) -> DeploymentID:
        doc = Deployment(
            **deployment.model_dump(),
            deployment_id=uuid.uuid4(),
            adding_timestamp=datetime.now(),
        )

        inserted_doc = await doc.insert()
        return DeploymentID(deployment_id=inserted_doc.deployment_id)

    @staticmethod
    async def get_deployment_by_id(deployment_id: uuid.UUID) -> DeploymentCreate:
        document = await Deployment.find_one(Deployment.deployment_id == deployment_id)
        if document is None:
            raise DeploymentsService._raise_http_error(deployment_id)
        return DeploymentCreate(**document.model_dump())

    @staticmethod
    async def delete_deployment(deployment_id: uuid.UUID) -> DeploymentID:
        doc = await Deployment.find_one(
            Deployment.deployment_id == deployment_id
        ).delete()
        if doc.deleted_count == 0:
            raise DeploymentsService._raise_http_error(deployment_id)

        return DeploymentID(deployment_id=deployment_id)

    @staticmethod
    async def update_deployment(
        deployment_id: uuid.UUID, new_deployment: DeploymentUpdate
    ) -> DeploymentID:
        result = await Deployment.find_one(
            Deployment.deployment_id == deployment_id
        ).set(
            {
                Deployment.version: new_deployment.version,
                Deployment.parameters: new_deployment.parameters,
            }
        )
        if result.modified_count == 0:
            raise DeploymentsService._raise_http_error(deployment_id)
        return DeploymentID(deployment_id=deployment_id)

    @staticmethod
    async def update_deployment_status(
        deployment_id: uuid.UUID, status: DeploymentStatus
    ) -> DeploymentID:
        result = await Deployment.find_one(
            Deployment.deployment_id == deployment_id
        ).set(
            {
                Deployment.status: status.status,
                Deployment.info: status.info,
            }
        )
        if result.modified_count == 0:
            raise DeploymentsService._raise_http_error(deployment_id)
        return DeploymentID(deployment_id=deployment_id)

    @staticmethod
    def _raise_http_error(deployment_id: uuid.UUID) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"A deployment with id={deployment_id} doesn't exists.",
        )
