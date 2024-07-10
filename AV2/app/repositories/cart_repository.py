from ..infra.database import db
from ..domain.models.cart import Cart

class CartRepository:
    @staticmethod
    def get_cart_by_id(cart_id: int):
        return Cart.query.get(cart_id)
    

    @staticmethod
    def get_cart_by_customer_id(customer_id: int):
        return Cart.query.filter_by(customer_id=customer_id).first()


    @staticmethod
    def create_cart(customer_id: int):
        cart = Cart(customer_id=customer_id)
        db.session.add(cart)
        db.session.commit()
        return cart
    
