from fastapi import FastAPI
from server.app.connect import async_engine
from server.app.controllers import (
    auth_controller,
    customer_controller,
    product_controller,
    order_controller,
)
from server.app.models import Base

app = FastAPI()


async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def on_startup():
    await init_models()


# Include routers from controllers
app.include_router(auth_controller.router, prefix="/login", tags=["auth"])
app.include_router(customer_controller.router, prefix="/customers", tags=["customers"])
app.include_router(product_controller.router, prefix="/products", tags=["products"])
app.include_router(order_controller.router, prefix="/orders", tags=["orders"])
