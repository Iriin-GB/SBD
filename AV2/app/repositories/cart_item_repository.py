from ..infra.database import db
from ..domain.models.cart_item import CartItem

class CartItemRepository:
    @staticmethod
    def get_cart_item_by_id(cart_item_id: int):
        return CartItem.query.get(cart_item_id)
    

    @staticmethod
    def create_cart_item(product_id: int, cart_id: int, quantity: int):
        cart_item = CartItem(product_id=product_id, cart_id=cart_id, quantity=quantity)
        db.session.add(cart_item)
        db.session.commit()
        return cart_item
    

    @staticmethod
    def delete_cart_item(cart_item_id: int):
        cart_item = CartItem.query.get(cart_item_id)
        db.session.delete(cart_item)
        db.session.commit()


    @staticmethod
    def edit_cart_item_quantity_by_id(cart_item_id: int, quantity: int):
        cart_item = CartItem.query.get(cart_item_id)
        cart_item.quantity = quantity # Atualizando quantidade
        db.session.commit()
        return cart_item
