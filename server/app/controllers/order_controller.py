from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from server.app.connect import get_db
from server.app.services.order_service import OrderService
from server.app.schemas import OrderCreate, OrderRead, User
from server.app.dependencies import get_current_active_user

router = APIRouter()
order_service = OrderService()


@router.post("/", response_model=OrderRead)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Create a new order.

    - **order**: OrderCreate object containing product ID and quantity.
    - **return**: The created OrderRead object.
    """
    return await order_service.create_order(db, current_user, order)


@router.get("/", response_model=List[OrderRead])
async def get_order_history(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve the order history for the current user.
    
    - **return**: List of OrderRead objects.
    """
    return await order_service.get_order_history(db, current_user)
