from fastapi import FastAPI

import src.utils
from src.auth.routers import router as auth_router
from src.profiles.routers import router as profile_router
from src.likes.routers import router as like_router
from src.scrolling.routers import router as scrolling_router

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

app.include_router(
    scrolling_router,
    prefix="/scrolling",
    tags=["scrolling"]
)

# ToDo check, why i cant payload data in GET requests
