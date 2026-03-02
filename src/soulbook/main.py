from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from soulbook.api.v1 import api_router
from soulbook.config.settings import settings

app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Welcome to Soulbook API"}


@app.get("/health")
async def health_check():
    return {"status": "ok"}