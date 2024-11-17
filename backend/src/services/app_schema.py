from schemas import AppSchema, AppSchemaUpdatedResponse, AppSchemaUpdatedResponse
from database import app_schemas_collection as collection
from fastapi import HTTPException, status


class AppSchemaService:
    @staticmethod
    async def create_app_schema(app_schema: AppSchema) -> AppSchemaUpdatedResponse:
        # Check for unique app/version combination
        filter_dict = app_schema.model_dump(include={"application_name", "version"})
        if await collection.find_one(filter_dict):
            raise AppSchemaService._conflict_error(
                app_schema.application_name, app_schema.version
            )
        app_schema_dict = app_schema.model_dump()
        await collection.insert_one(app_schema_dict)
        return AppSchemaUpdatedResponse(**app_schema_dict)

    @staticmethod
    async def get_app_schema_by_version_and_name(
        application_name: str, version: str
    ) -> AppSchema:
        document = await collection.find_one(
            {"application_name": application_name, "version": version}
        )
        if not document:
            raise AppSchemaService._not_found_error(application_name, version)
        return AppSchema(**document)

    @staticmethod
    async def delete_app_schema_by_version_and_name(
        application_name: str, version: str
    ) -> AppSchemaUpdatedResponse:
        result = await collection.delete_one(
            {"application_name": application_name, "version": version}
        )
        if result.deleted_count == 0:
            raise AppSchemaService._not_found_error(application_name, version)
        return AppSchemaUpdatedResponse(
            application_name=application_name, version=version
        )

    @staticmethod
    async def update_app_schema_by_version_and_name(app_schema: AppSchema) -> AppSchema:
        # Update the document
        filter_dict = app_schema.model_dump(include={"application_name", "version"})
        update_dict = {
            "$set": app_schema.model_dump(exclude={"application_name", "version"})
        }
        result = await collection.update_one(filter_dict, update_dict)

        if result.matched_count == 0:
            raise AppSchemaService._not_found_error(
                app_schema.application_name, app_schema.version
            )
        return AppSchemaUpdatedResponse(
            application_name=app_schema.application_name, version=app_schema.version
        )

    @staticmethod
    def _not_found_error(application_name: str, version: str) -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Schema for '{application_name}' version '{version}' not found.",
        )

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
