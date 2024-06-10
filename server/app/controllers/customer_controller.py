from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from server.app.connect import get_db
from server.app.services.customer_service import CustomerService
from server.app.schemas import CustomerRead, User
from server.app.dependencies import get_current_active_user

router = APIRouter()
customer_service = CustomerService()


@router.get("/", response_model=List[CustomerRead])
async def get_customers(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a list of all customers.

    - **return**: List of CustomerRead objects.
    """
    customers = await customer_service.get_all(db)
    if not customers:
        raise HTTPException(status_code=404, detail="No customers found")
    return customers
