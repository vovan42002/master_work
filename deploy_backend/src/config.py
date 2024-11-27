import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    access_token: str = Field(
        ...,
        description="Statis API key used for Bearer authorization",
    )
    deployments_dir: str = Field(
        ...,
        description="Base directory where all deployments templates will be stored",
    )
    deployment_timeout: float = Field(
        default=300,
        description="Timeout for helmfile subprocess call. default is 5 min",
    )
    helm_registry_url: str = Field(
        ...,
        description="Helm registry where all helm charts are stored. If starts with https:// then it's not OCI based, if starts with domain then it's oci based",
    )
    helm_registry_username: str = Field(
        ...,
        description="Username to access helm registry",
    )
    helm_registry_username_password: str = Field(
        ...,
        description="Username's password to access helm registry",
    )
    kubernetes_namespace: str = Field(
        default="default",
        description="Kubernetes namespace where applications will be deployed",
    )
    celery_broker: str = Field(
        ...,
        description="Celery broker URL",
    )
    backend_base_url: str = Field(
        ...,
        description="Base URL to access backend. In format http://localhost:8000",
    )
    backend_access_token: str = Field(
        ...,
        description="Static access token to authorize request to backend",
    )


settings = Settings()
