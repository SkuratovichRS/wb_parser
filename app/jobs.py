import logging

from app.service import service


async def add_product(artikul: int):
    await service.add_product(artikul)
    logging.info(f"job {add_product.__name__} with artikul {artikul} done")