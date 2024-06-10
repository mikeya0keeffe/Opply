import enum
import uuid
from sqlalchemy import (
    Column,
    Boolean,
    String,
    Text,
    Numeric,
    Enum,
    ForeignKey,
    TIMESTAMP,
    Integer,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    address = Column(String, index=True)
    username = Column(String, index=True)
    hash = Column(Text)
    disabled = Column(Boolean)


class Product(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, index=True)
    price = Column(Numeric(10, 2))
    quantity_in_stock = Column(Integer)


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class Order(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    product_id = Column(UUID(as_uuid=True), ForeignKey("products.id"), nullable=False)
    status = Column(
        Enum(OrderStatus, name="order_status", native_enum=False),
        nullable=False,
        default=OrderStatus.PENDING,
    )
    quantity = Column(Integer, nullable=False)
    order_date = Column(TIMESTAMP, server_default="now()")

    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product")


Customer.orders = relationship("Order", order_by=Order.id, back_populates="customer")
