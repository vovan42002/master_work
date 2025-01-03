import re
from enum import Enum
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional, Dict
from uuid import UUID


class MongoSettings(BaseSettings):
    USER: str = Field(..., alias="MONGO_USER")
    PASSWORD: str = Field(..., alias="MONGO_PASSWORD")
    HOST: str = Field(..., alias="MONGO_HOST")
    PORT: int = Field(27017, alias="MONGO_PORT")
    DB_NAME: str = Field(..., alias="MONGO_DB_NAME")
    AUTH_DB_NAME: str = Field(..., alias="MONGO_AUTH_DB_NAME")


class ApplicationSettings(BaseSettings):
    logLevel: str = "debug"
    auth_backend_base_url: str
    deploy_backend_base_url: str
    deploy_backend_token: str
    access_token: str


class Settings(BaseModel):
    mongodb: MongoSettings = MongoSettings()
    application: ApplicationSettings = ApplicationSettings()


class HealthCheckResponse(BaseModel):
    """A response schema for Health Check"""

    status: str = Field(
        ...,
        title="Status",
        description="Whether server is running",
        examples=["ok"],
    )


class VarType(str, Enum):
    string = "string"
    boolean = "boolean"
    dropdown_list = "dropdown-list"


class EnvVarConfig(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="Environment variable name",
        examples=["LOG_LEVEL", "BASE_PATH"],
    )
    type: VarType = Field(
        ...,
        title="Variable type",
        description="Type of the variable(how it will be shown on frontend configuration page)",
        examples=[VarType.string, VarType.boolean, VarType.dropdown_list],
    )
    default: str = Field(
        ...,
        title="Default value",
        description="Default value for the environment variable",
        examples=["info", "/test"],
    )
    hint: Optional[str] = Field(
        ...,
        title="Tip for variable",
        description="This tip will be shown on configuration page when hovering over variable",
        examples=["Logging level", "Prefix path"],
    )


class ContainerConfig(BaseModel):
    name: str = Field(
        ...,
        title="Name",
        description="Container name",
        examples=["frontend", "backend"],
    )
    env_vars: List[EnvVarConfig]


class AppBaseSchema(BaseModel):
    application_name: str = Field(
        ...,
        title="Name",
        description="Name of the application",
        examples=["my-app", "MyApp123"],
    )
    version: str = Field(
        ...,
        title="Version",
        description="Application version",
        examples=["1.0.0", "1.0.9"],
    )

    # Validator for semantic versioning
    @field_validator("version")
    def validate_semantic_version(cls, value):
        if not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError(
                "version must be in semantic versioning format (MAJOR.MINOR.PATCH)"
            )
        return value

    # Validator for application_name to allow only letters, numbers, dashes, and underscores
    @field_validator("application_name")
    def validate_application_name(cls, value):
        if not re.match(r"^[\w-]+$", value):
            raise ValueError(
                "application_name can only contain letters, numbers, dashes, or underscores"
            )
        return value


class ContainersList(BaseModel):
    containers: List[ContainerConfig]


class AppSchema(ContainersList, AppBaseSchema):
    pass


class AppSchemaUpdatedResponse(AppBaseSchema):
    pass


class VersionsList(BaseModel):
    versions: List[str]


class ApplicationsList(BaseModel):
    applications: List[str]


class DeploymentID(BaseModel):
    deployment_id: UUID


class DeploymentStatusEnum(str, Enum):
    success = "success"
    failed = "failed"
    in_process = "in_process"
    none = "null"


class DeploymentCreate(AppBaseSchema):
    username: str
    status: Optional[DeploymentStatusEnum] = Field(
        DeploymentStatusEnum.none,
        title="Status",
        description="Optional deployment status",
        examples=["null", "in_process", "completed", "failed"],
    )
    info: Optional[dict] = Field(
        {},
        title="Deployment info",
        description="Optional deployment info",
    )
    parameters: Dict[str, Dict[str, str]]


class DeploymentUpdate(BaseModel):
    version: str = Field(
        ...,
        title="Version",
        description="Application version",
        examples=["1.0.0", "1.0.9"],
    )

    # Validator for semantic versioning
    @field_validator("version")
    def validate_semantic_version(cls, value):
        if not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError(
                "version must be in semantic versioning format (MAJOR.MINOR.PATCH)"
            )
        return value

    status: Optional[DeploymentStatusEnum] = Field(
        DeploymentStatusEnum.none,
        title="Status",
        description="Optional deployment status",
        examples=["null", "in_process", "completed", "failed"],
    )
    info: Optional[dict] = Field(
        {},
        title="Deployment info",
        description="Optional deployment info",
    )
    parameters: Dict[str, Dict[str, str]]


class DeploymentToDeploy(BaseModel):
    application_name: str = Field(
        ...,
        title="Name",
        description="Name of the application",
        examples=["my-app", "MyApp123"],
    )
    version: str = Field(
        ...,
        title="Version",
        description="Application version",
        examples=["1.0.0", "1.0.9"],
    )

    # Validator for semantic versioning
    @field_validator("version")
    def validate_semantic_version(cls, value):
        if not re.match(r"^\d+\.\d+\.\d+$", value):
            raise ValueError(
                "version must be in semantic versioning format (MAJOR.MINOR.PATCH)"
            )
        return value

    # Validator for application_name to allow only letters, numbers, dashes, and underscores
    @field_validator("application_name")
    def validate_application_name(cls, value):
        if not re.match(r"^[\w-]+$", value):
            raise ValueError(
                "application_name can only contain letters, numbers, dashes, or underscores"
            )
        return value

    parameters: Dict[str, Dict[str, str]]


class DeploymentStatus(BaseModel):
    status: DeploymentStatusEnum
    info: Optional[dict] = Field(
        {},
        title="Deployment info",
        description="Optional deployment info",
    )


class AuthAdapterUser(BaseModel):
    is_admin: bool
    username: str


class DeploymentResponse(AppBaseSchema):
    deployment_id: str


class UserDeployments(BaseModel):
    deployments: List[DeploymentResponse]
