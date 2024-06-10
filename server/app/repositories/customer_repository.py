from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.app.models import Customer
from server.app.repositories.base_repository import BaseRepository


class CustomerRepository(BaseRepository[Customer]):
    def __init__(self):
        super().__init__(Customer)

    async def get_by_username(self, db: AsyncSession, username: str) -> Customer:
        result = await db.execute(select(Customer).where(Customer.username == username))
        return result.scalars().first()
