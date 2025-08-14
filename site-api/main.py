from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import router
from config.settings import settings
from config.logging import setup_logging

logger = setup_logging(
    project_id=settings.GCLOUD_PROJECT_ID,
    log_level=settings.LOG_LEVEL,
    credentials_dict=settings.GOOGLE_APPLICATION_CREDENTIALS
)

app = FastAPI(
    docs_url= "/api/docs",
    redoc_url= "/api/redocs",
    title="Website Details API",
    version="1.0",
    description="API for retrieving website details and navigation",
    openapi_url="/api/openapi.json"
)

allowed_origins = [url.strip() for url in settings.ALLOWED_ORIGINS.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Website Details API is running"}

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Website Details API server")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
