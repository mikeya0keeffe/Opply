from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from server.app.models import Order, OrderStatus
from server.app.repositories.base_repository import BaseRepository


class OrderRepository(BaseRepository[Order]):
    def __init__(self):
        super().__init__(Order)

    async def create_order(
        self, db: AsyncSession, customer_id: int, product_id: int, quantity: int
    ) -> Order:
        new_order = Order(
            customer_id=customer_id,
            product_id=product_id,
            status=OrderStatus.PENDING,
            quantity=quantity,
        )
        db.add(new_order)
        await db.commit()
        await db.refresh(new_order)
        return new_order

    async def get_order_history(
        self, db: AsyncSession, customer_id: int
    ) -> list[Order]:
        result = await db.execute(select(Order).where(Order.customer_id == customer_id))
        return result.scalars().all()
