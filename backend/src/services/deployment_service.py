from schemas import DeploymentCreate, DeploymentID
from database import deployments_collection as collection
from fastapi import HTTPException, status


class DeploymentsService:

    @staticmethod
    async def create_new_deployment(deployment: DeploymentCreate) -> DeploymentID:
        inserted_doc = await collection.insert_one(deployment.model_dump())
        deployment_id = await collection.find_one(
            filter={"_id": inserted_doc.inserted_id}
        )
        return DeploymentID(deployment_id=deployment_id)

    @staticmethod
    def _conflict_error(application_name: str, version: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An entry with app '{application_name}' and version '{version}' already exists.",
        )

    @staticmethod
    async def list_app_schemas() -> list:
        # Retrieve all AppSchema documents
        documents = await collection.find().to_list()
        return [AppSchema(**doc) for doc in documents]
