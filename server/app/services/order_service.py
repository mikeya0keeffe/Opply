from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from server.app.schemas import OrderCreate, OrderRead, User, ProductRead
from server.app.repositories.order_repository import OrderRepository
from server.app.repositories.product_repository import ProductRepository
from server.app.repositories.customer_repository import CustomerRepository
from server.app.services.base_service import BaseService
from server.app.models import Order


class OrderService(BaseService[Order]):
    def __init__(self):
        super().__init__(OrderRepository())
        self.product_repository = ProductRepository()
        self.customer_repository = CustomerRepository()

    async def create_order(
        self, db: AsyncSession, current_user: User, order: OrderCreate
    ) -> OrderRead:
        customer = await self.customer_repository.get_by_id(db, current_user.id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        product = await self.product_repository.get_by_id(db, order.product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.quantity_in_stock < order.quantity:
            raise HTTPException(
                status_code=400, detail="Not enough product quantity available"
            )
        
        # Order of operations ensures data integrity
        product.quantity_in_stock -= order.quantity
        new_order = await self.repository.create_order(
            db, current_user.id, order.product_id, order.quantity
        )

        product = await self.product_repository.get_by_id(db, new_order.product_id)
        return OrderRead(
            id=new_order.id,
            customer_id=new_order.customer_id,
            product_id=new_order.product_id,
            quantity=new_order.quantity,
            status=new_order.status,
            order_date=new_order.order_date,
            product=ProductRead(
                id=product.id,
                name=product.name,
                price=product.price,
                quantity_in_stock=product.quantity_in_stock,
            ),
        )

    async def get_order_history(
        self, db: AsyncSession, current_user: User
    ) -> list[OrderRead]:
        orders = await self.repository.get_order_history(db, current_user.id)
        if not orders:
            raise HTTPException(
                status_code=404, detail="No orders found for this customer"
            )

        order_details = []
        for order in orders:
            product = await self.product_repository.get_by_id(db, order.product_id)
            order_details.append(
                OrderRead(
                    id=order.id,
                    customer_id=order.customer_id,
                    product_id=order.product_id,
                    quantity=order.quantity,
                    status=order.status,
                    order_date=order.order_date,
                    product=ProductRead(
                        id=product.id,
                        name=product.name,
                        price=product.price,
                        quantity_in_stock=product.quantity_in_stock,
                    ),
                )
            )

        return order_details
