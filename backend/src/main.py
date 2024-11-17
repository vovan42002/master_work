import logging
import uvicorn
from fastapi import FastAPI
import schemas
from config import get_settings
from contextlib import asynccontextmanager
from routers.schema import router as r_schema
from routers.applications import router as r_applications
from routers.deployments import router as r_deployments

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Check whether all required setting are set
    """
    get_settings()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> schemas.HealthCheckResponse:
    """Verify the server's health"""

    logger.info("Requested service health check")
    return schemas.HealthCheckResponse(status="ok")


app.include_router(router=r_schema, prefix="/v1")
app.include_router(router=r_applications, prefix="/v1")
app.include_router(router=r_deployments, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
