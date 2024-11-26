import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from endpoints import auth, user
from schemas.config import settings
from utils.error_handlers import http_exception_handler
from scripts.create_admin import lifespan

# Configure the logging system based on settings
logging.basicConfig(level=settings.log_level.upper())
logger = logging.getLogger(__name__)

# Create an instance of FastAPI with conditional documentation URL
app = FastAPI(
    title="Authorization Service",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/v1")
app.include_router(user.router, prefix="/v1")

# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
