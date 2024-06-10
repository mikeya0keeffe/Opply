from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from server.app.connect import get_db
from server.app.services.product_service import ProductService
from server.app.schemas import ProductRead, User
from server.app.dependencies import get_current_active_user

router = APIRouter()
product_service = ProductService()


@router.get("/", response_model=List[ProductRead])
async def get_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    Retrieve a paginated list of products.

    - **page**: The page number to retrieve.
    - **page_size**: The number of items per page.
    - **return**: List of Product objects.
    """
    products = await product_service.get_products_paginated(db, page, page_size)
    if not products:
        raise HTTPException(status_code=404, detail="No products found")
    return products
