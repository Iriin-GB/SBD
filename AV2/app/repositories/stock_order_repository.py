from ..infra.database import db
from ..domain.models.stock_order import StockOrder

class StockOrderRepository:
    @staticmethod
    def get_stock_order_by_id(stock_order_id: int):
        return StockOrder.query.get(stock_order_id)
    
    
    @staticmethod
    def get_all_stock_order_from_cart(cart_id: int):
        return StockOrder.query.filter_by(cart_id=cart_id).all()

    
    @staticmethod
    def get_all_stock_orders():
        return StockOrder.query.all()


    @staticmethod
    def create_stock_order(product_id: int, quantity: int, cart_id: int):
        stock_order = StockOrder(product_id=product_id, quantity=quantity, cart_id=cart_id)
        db.session.add(stock_order)
        db.session.commit()
        return stock_order
    

    @staticmethod
    def delete_stock_order_by_id(stock_order_id: int):
        cart_item = StockOrder.query.get(stock_order_id)
        db.session.delete(cart_item)
        db.session.commit()



