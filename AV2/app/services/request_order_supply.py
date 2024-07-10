from ..repositories.customer_repository import CustomerRepository
from ..repositories.cart_repository import CartRepository
from ..repositories.product_repository import ProductRepository
from ..repositories.cart_item_repository import CartItemRepository
from ..repositories.stock_order_repository import StockOrderRepository

class OrderSupplyService:
    @staticmethod
    def process_supply():
        stocks = StockOrderRepository.get_all_stock_orders()

        if len(stocks) == 0:
            raise Exception('No stock orders to process.')

        for stock_order in stocks:
            # Adicionar item ao estoque
            product = ProductRepository.get_product_by_id(product_id=stock_order.product_id)
            ProductRepository.edit_product_stock_by_id(product_id=product.id, stock=product.stock + stock_order.quantity)

            # Deletando a StockOrder
            StockOrderRepository.delete_stock_order_by_id(stock_order_id=stock_order.id)
    