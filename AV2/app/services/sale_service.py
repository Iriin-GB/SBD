from ..repositories.customer_repository import CustomerRepository
from ..repositories.cart_repository import CartRepository
from ..repositories.product_repository import ProductRepository
from ..repositories.cart_item_repository import CartItemRepository
from ..repositories.stock_order_repository import StockOrderRepository

class SaleService():
    @staticmethod
    def process_sale(data) -> float:
        # Verificando customer
        customer = CustomerRepository.get_customer_by_email(data['customer_email'])

        if not customer: # Criar customer
            customer = CustomerRepository.create_customer(email=data['customer_email'])

        # Procurar carrinho
        cart = CartRepository.get_cart_by_customer_id(customer.id)

        if not cart: # Criar carrinho
            cart = CartRepository.create_cart(customer_id=customer.id)

        if len(cart.items) == 0:
            raise Exception('Cart is empty.')

        # Verificando se os Produtos no carrinho estão em estoque
        products_to_order = []
        for item in cart.items:
            product = ProductRepository.get_product_by_id(item.product_id)

            if product.stock < item.quantity:
                # Resetando os Stock Order do carrinho
                old_orders = StockOrderRepository.get_all_stock_order_from_cart(cart_id=cart.id)

                for order in old_orders: # Deletando stock Order antigo
                    StockOrderRepository.delete_stock_order_by_id(stock_order_id=order.id)

                # Criando order 
                stock_order = StockOrderRepository.create_stock_order(
                    product_id=product.id,
                    quantity=item.quantity - product.stock,
                    cart_id=cart.id,
                )

                products_to_order.append({
                    'id': stock_order.id,
                    'product_id': stock_order.product_id,
                    'quantity': stock_order.quantity
                })

        if len(products_to_order) > 0:
            raise Exception({
                'detail': 'Some Products in your Cart is out of stock, we create a Stock analisys to order.',
                'products_to_order': products_to_order,  # Lista de produtos que estão sem estoque e precisam ser pedidos
            })


        total_price: float = 0 # Variável para guardar o valor total da compra
        # Deletando todos os items do Carrinho (simulando compra)
        for item in cart.items:
            product = ProductRepository.get_product_by_id(item.product_id)
            total_price += product.price * item.quantity
            CartItemRepository.delete_cart_item(item.id)
            ProductRepository.edit_product_stock_by_id(
                product_id=product.id,
                stock=product.stock - item.quantity,
            )

        return total_price
    