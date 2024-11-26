from schemas import AppSchema, AppSchemaUpdatedResponse, AppSchemaUpdatedResponse
from models import Application
from fastapi import HTTPException, status
from datetime import datetime


class AppSchemaService:
    @staticmethod
    async def create_app_schema(app_schema: AppSchema) -> AppSchemaUpdatedResponse:
        # Check for unique app/version combination

        check = await Application.find_one(
            Application.application_name == app_schema.application_name,
            Application.version == app_schema.version,
        )

        if check:
            raise AppSchemaService._conflict_error(
                app_schema.application_name, app_schema.version
            )
        await Application(
            **app_schema.model_dump(),
            adding_timestamp=datetime.now(),
        ).insert()

        return AppSchemaUpdatedResponse(**app_schema.model_dump())

    @staticmethod
    async def get_app_schema_by_version_and_name(
        application_name: str, version: str
    ) -> AppSchema:
        document = await Application.find_one(
            Application.application_name == application_name,
            Application.version == version,
        )
        if document is None:
            raise AppSchemaService._not_found_error(application_name, version)
        return AppSchema(**document.model_dump())

    @staticmethod
    async def delete_app_schema_by_version_and_name(
        application_name: str, version: str
    ) -> AppSchemaUpdatedResponse:
        result = await Application.find_one(
            Application.application_name == application_name,
            Application.version == version,
        ).delete()
        if result.deleted_count == 0:
            raise AppSchemaService._not_found_error(application_name, version)
        return AppSchemaUpdatedResponse(
            application_name=application_name, version=version
        )

    @staticmethod
    async def update_app_schema_by_version_and_name(app_schema: AppSchema) -> AppSchema:
        result = await Application.find_one(
            Application.application_name == app_schema.application_name,
            Application.version == app_schema.version,
        ).set({Application.containers: app_schema.containers})

        if result.modified_count == 0:
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
