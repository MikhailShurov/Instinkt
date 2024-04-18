from fastapi import FastAPI

from src.auth.routers import router as auth_router

app = FastAPI(title="Instinkt", description="")

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
