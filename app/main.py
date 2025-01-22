import logging
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI

from app.database import close_orm, init_orm
from app.routers import router
from app.scheduler import scheduler
from app.settings import Settings


async def lifespan(app: FastAPI) -> AsyncGenerator:
    print("starting")
    await init_orm()
    scheduler.start()
    yield
    print("shutting down")
    await close_orm()
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host=Settings.API_HOST, port=Settings.API_PORT)
