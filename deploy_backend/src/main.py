import logging
import uvicorn
from fastapi import FastAPI
import schemas
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from router import router as deployments_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Check whether all required setting are set
    """
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
async def health() -> schemas.HealthCheckResponse:
    """Verify the server's health"""
    logger.info("Requested service health check")
    return schemas.HealthCheckResponse(status="ok")


app.include_router(router=deployments_router, prefix="/v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
