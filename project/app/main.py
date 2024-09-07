import logging

from fastapi import FastAPI, Depends
from tortoise.contrib.fastapi import register_tortoise

from app.config import get_settings, Settings
from app.api import ping, summaries, auth, marketplace, product
# from app.auth.auth import auth_router, register_router
from contextlib import asynccontextmanager

from app.db import init_db


log = logging.getLogger("uvicorn")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     log.info("Starting up...")
#     init_db(app)

#     yield

#     log.info("Shutting down...")

def create_application() -> FastAPI:
    application = FastAPI(
        title="revision_app",
        # lifespan=lifespan,
    )
    application.include_router(ping.router)
    application.include_router(summaries.router, prefix="/summaries", tags=["summaries"])
    application.include_router(auth.router, tags=["users"])
    application.include_router(marketplace.router, prefix="/mp", tags=['marketplaces'])
    application.include_router(product.router, prefix="/products", tags=['products'])
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")
    init_db(app)


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")