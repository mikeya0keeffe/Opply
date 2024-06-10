from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, TypeVar, Generic

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_by_id(self, db: AsyncSession, entity_id: int) -> T:
        result = await db.execute(select(self.model).where(self.model.id == entity_id))
        return result.scalars().first()

    async def get_all(self, db: AsyncSession) -> list[T]:
        result = await db.execute(select(self.model))
        return result.scalars().all()
