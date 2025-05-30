import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.firebase import initialize_firebase
initialize_firebase()
from src.config.config import get_settings
from src.api.v1.routers import api_router

app = FastAPI(
    title=get_settings().PROJECT_NAME,
    description=get_settings().PROJECT_DESCRIPTION,
    version=get_settings().VERSION,
    openapi_url=f"{get_settings().API_V1_STR}/openapi.json",
    docs_url=f"{get_settings().API_V1_STR}/docs",
    redoc_url=f"{get_settings().API_V1_STR}/redoc",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router, prefix=get_settings().API_V1_STR)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=get_settings().HOST,
        port=get_settings().PORT,
        reload=get_settings().RELOAD,
        workers=get_settings().WORKERS,
    )