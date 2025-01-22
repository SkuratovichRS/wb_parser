import logging

from apscheduler.jobstores.base import ConflictingIdError
from fastapi import APIRouter, Depends

from app.dependencies import verify_token
from app.jobs import add_product
from app.scheduler import scheduler
from app.schemas import PostProductRequest
from app.settings import Settings

router = APIRouter(prefix="/api/v1")


@router.post("/products", status_code=204, dependencies=[Depends(verify_token)])
async def create_product(data: PostProductRequest) -> None:
    scheduler.add_job(add_product, args=(data.artikul,), id=f"single_{data.artikul}")


@router.get("/products/subscribe/{artikul}", status_code=204, dependencies=[Depends(verify_token)])
async def create_product(artikul: int) -> None:
    try:
        scheduler.add_job(
            add_product,
            args=(artikul,),
            id=f"subscribe_{artikul}",
            trigger="interval",
            minutes=Settings.SUBSCRIBE_INTERVAL_MINUTES,
        )
    except ConflictingIdError:
        logging.info(f"job {add_product.__name__} with artikul {artikul} already exists")
