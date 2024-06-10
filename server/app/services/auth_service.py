from datetime import timedelta, datetime, timezone
from typing import Optional
import os
import jwt
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from server.app.schemas import UserInDB
from server.app.repositories.customer_repository import CustomerRepository


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


class AuthService:
    def __init__(self):
        self.customer_repository = CustomerRepository()

    async def get_user(self, db: AsyncSession, username: str) -> Optional[UserInDB]:
        return await self.customer_repository.get_by_username(db, username)

    async def authenticate_user(
        self, db: AsyncSession, username: str, password: str
    ) -> Optional[UserInDB]:
        user = await self.get_user(db, username)
        if not user or not pwd_context.verify(password, user.hash):
            return None
        return user

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
