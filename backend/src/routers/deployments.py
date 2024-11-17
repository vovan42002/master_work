import logging
from fastapi import status, APIRouter
from fastapi.responses import JSONResponse
from schemas import DeploymentID, DeploymentCreate

from services.deployment_service import DeploymentsService


router = APIRouter(prefix="/deployments")


@router.post("", status_code=status.HTTP_201_CREATED, response_model=DeploymentID)
async def create_deployment(deployment: DeploymentCreate):
    logging.info("Request to create a new deployment")
    service = DeploymentsService()
    return await service.create_new_deployment(deployment)


@router.delete("/{deployment_id:int}", status_code=status.HTTP_200_OK)
async def delete_deployment(deployment_id: int):
    logging.info(f"Request to delete deployment with id={deployment_id}")
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)


@router.put("/{deployment_id:int}", status_code=status.HTTP_200_OK)
async def create_deployment(deployment_id: int):
    logging.info(f"Request to delete deployment with id={deployment_id}")
    return JSONResponse(content={}, status_code=status.HTTP_200_OK)
