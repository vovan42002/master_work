from config import get_settings
from fastapi import status
import httpx
import logging
from schemas import DeploymentID, DeploymentToDeploy


logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


class DeployAdapter:
    def __init__(self, deployment_id: str):
        self.deployment_id = deployment_id

    async def start_deployment(self, deployment: DeploymentToDeploy) -> DeploymentID:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                url=f"{get_settings().application.deploy_backend_base_url}/v1/deployments/{self.deployment_id}",
                headers={
                    "Authorization": f"Bearer {get_settings().application.deploy_backend_token}",
                    "Accept": "application/json",
                },
                json=deployment.model_dump(),
            )
            if resp.status_code != status.HTTP_200_OK:
                logger.error(
                    msg=f"Failed to start deployment in deploy subsystem",
                    extra={"details": resp.json()},
                )
                resp.raise_for_status()
            return DeploymentID(deployment_id=self.deployment_id)

    async def uninstall_deployment(self) -> DeploymentID:
        async with httpx.AsyncClient() as client:
            resp = await client.delete(
                url=f"{get_settings().application.deploy_backend_base_url}/v1/deployments/{self.deployment_id}",
                headers={
                    "Authorization": f"Bearer {get_settings().application.deploy_backend_token}",
                    "Accept": "application/json",
                },
            )
            if resp.status_code != status.HTTP_200_OK:
                logger.error(
                    msg=f"Failed to delete deployment using deploy subsystem",
                    extra={"details": resp.json()},
                )
                resp.raise_for_status()
            return DeploymentID(deployment_id=self.deployment_id)
