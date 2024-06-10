from sqlalchemy.ext.asyncio import AsyncSession
from server.app.models import Product
from server.app.repositories.product_repository import ProductRepository
from server.app.services.base_service import BaseService


class ProductService(BaseService[Product]):
    def __init__(self):
        super().__init__(ProductRepository())

    async def get_products_paginated(
        self, db: AsyncSession, page: int, page_size: int
    ) -> list[Product]:
        return await self.repository.get_products_paginated(db, page, page_size)
