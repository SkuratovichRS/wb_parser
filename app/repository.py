from app.database import DbSession
from app.models import Product


class Repository:
    async def add_product(self, validated_data: dict):
        async with DbSession() as session:
            product = Product(**validated_data)
            await session.merge(product)
            await session.commit()

    async def get_product(self, artikul: int) -> Product | None:
        async with DbSession() as session:
            product = await session.get(Product, artikul)
            return product
    

    