from typing import TypeVar, Generic
from server.app.repositories.base_repository import BaseRepository

T = TypeVar("T")


class BaseService(Generic[T]):
    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def get_by_id(self, db, entity_id: int) -> T:
        return await self.repository.get_by_id(db, entity_id)

    async def get_all(self, db) -> list[T]:
        return await self.repository.get_all(db)
