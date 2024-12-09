import logging
from datetime import datetime

from beanie import Document, Indexed
from schemas import AppSchema, DeploymentCreate
from uuid import UUID


logger = logging.getLogger(__name__)


class Application(AppSchema, Document):
    adding_timestamp: Indexed(datetime)  # Indexed field for timestamp

    class Settings:
        name = "schemas"  # Collection name in MongoDB


class Deployment(DeploymentCreate, Document):
    adding_timestamp: Indexed(datetime)  # Indexed field for timestamp
    deployment_id: UUID

    class Settings:
        name = "deployments"
