from fastapi import FastAPI

import src.utils
from src.auth.routers import router as auth_router
from src.profiles.routers import router as profile_router
from src.likes.routers import router as like_router

app = FastAPI(title="Instinkt", description="")

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    profile_router,
    prefix="/profiles",
    tags=["profiles"]
)

app.include_router(
    like_router,
    prefix="/likes",
    tags=["likes"]
)
