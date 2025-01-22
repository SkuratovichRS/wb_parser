import logging

import aiohttp

from app.models import Product
from app.repository import Repository
from app.schemas import DataSchema

BASE_URL = "https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm="


class Service:
    def __init__(self, repository: Repository):
        self._repository = repository

    async def add_product(self, artikul: int) -> None:
        async with aiohttp.ClientSession() as http_session:
            response = await http_session.get(f"{BASE_URL}{artikul}")
            response_json = await response.json()
        data = DataSchema(**response_json)
        if not data.data.products:
            logging.info(f"product {artikul} not found")
            return
        validated_data = {
            "artikul": artikul,
            "name": data.data.products[0].name,
            "price": data.data.products[0].salePriceU,
            "rating": data.data.products[0].reviewRating,
            "quantity": data.data.products[0].totalQuantity,
        }
        await self._repository.add_product(validated_data)

    async def get_product(self, artikul: int) -> Product | None:
        return await self._repository.get_product(artikul)


service = Service(Repository())
