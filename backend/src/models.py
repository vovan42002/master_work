import logging
from datetime import datetime

from beanie import Document, Indexed
from schemas import AppSchema, Deployment


logger = logging.getLogger(__name__)


class ApplicationsCollection(AppSchema, Document):
    adding_timestamp: Indexed(datetime)  # Indexed field for timestamp

    class Settings:
        name = "schemas"  # Collection name in MongoDB


class DeploymentsCollection(Deployment, Document):
    adding_timestamp: Indexed(datetime)  # Indexed field for timestamp
    deployment_id: Indexed(int)

    class Settings:
        name = "deployments"  # Collection name in MongoDB
