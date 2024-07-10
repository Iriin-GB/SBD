from ..infra.database import db
from ..domain.models.customer import Customer

class CustomerRepository:
    @staticmethod
    def get_customer_by_email(customer_email: str):
        return Customer.query.filter_by(email=customer_email).first()
    

    @staticmethod
    def get_customer_by_id(customer_id: int):
        return Customer.query.get(customer_id)


    @staticmethod
    def create_customer(email: str):
        customer = Customer(email=email)
        db.session.add(customer)
        db.session.commit()
        return customer
    