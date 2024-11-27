from pydantic import BaseModel, Field, field_validator
from typing import Dict, Optional
import re
from uuid import UUID
from enum import Enum


class HealthCheckResponse(BaseModel):
    """A response schema for Health Check"""

    status: str = Field(
        ...,
        title="Status",
        description="Whether server is running",
        examples=["ok"],
    )


class Deployment(BaseModel):
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


class DeploymentID(BaseModel):
    deployment_id: UUID = Field(
        examples=[
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "2fa85f64-5717-4562-b3fc-2c963f66afa6",
        ],
        description="UUID of the deployment",
    )


class DeploymentStatus(str, Enum):
    success = "success"
    failed = "failed"
    in_process = "in_process"


class DeploymentResult(BaseModel):
    status: DeploymentStatus
    msg: Optional[str]
    stderr: Optional[str]


class DeploymentScheduled(BaseModel):
    deployment_id: UUID
    msg: str
