from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.app.models import Product
from server.app.repositories.base_repository import BaseRepository


class ProductRepository(BaseRepository[Product]):
    def __init__(self):
        super().__init__(Product)

    async def get_products_paginated(
        self, db: AsyncSession, page: int, page_size: int
    ) -> list[Product]:
        offset = (page - 1) * page_size
        result = await db.execute(select(Product).offset(offset).limit(page_size))
        return result.scalars().all()
