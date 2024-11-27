import httpx
from schemas import DeploymentResult
from config import settings
from fastapi import status
import logging


logger = logging.getLogger(__name__)


class Backend:
    def __init__(self, deployment_id: str):
        self.deployment_id = deployment_id

    def update_status(self, deploy_result: DeploymentResult) -> bool:
        """
        Return:
            - True if status successfully updated
            - False if status update failed
        """
        with httpx.Client() as client:
            body = {
                "status": deploy_result.status,
                "info": deploy_result.model_dump(),
            }
            resp = client.patch(
                url=f"{settings.backend_base_url}/v1/deployments/{self.deployment_id}/status",
                headers={"Authorization": f"Bearer {settings.backend_access_token}"},
                json=body,
            )
            if resp.status_code != status.HTTP_200_OK:
                logger.error(
                    msg=f"Failed to update deployment {self.deployment_id} status",
                    extra={"details": resp.json()},
                )
                return False
        return True
