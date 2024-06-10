from server.app.models import Customer
from server.app.repositories.customer_repository import CustomerRepository
from server.app.services.base_service import BaseService


class CustomerService(BaseService[Customer]):
    def __init__(self):
        super().__init__(CustomerRepository())
