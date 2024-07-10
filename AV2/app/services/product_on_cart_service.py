from ..repositories.customer_repository import CustomerRepository
from ..repositories.cart_repository import CartRepository
from ..repositories.product_repository import ProductRepository
from ..repositories.cart_item_repository import CartItemRepository

class ProductOnCartService():
    @staticmethod
    def process_product_on_cart(data):
        # Verificando customer
        customer = CustomerRepository.get_customer_by_email(data['customer_email'])

        if not customer: # Criar customer
            customer = CustomerRepository.create_customer(email=data['customer_email'])

        # Procurar carrinho
        cart = CartRepository.get_cart_by_customer_id(customer.id)

        if not cart: # Criar carrinho
            cart = CartRepository.create_cart(customer_id=customer.id)

        # Verificar se o produto existe
        product = ProductRepository.get_product_by_id(data['product_id'])

        if not product:
            raise Exception('Product not found')

        if data['quantity'] <= 0:
            raise Exception('Quantity must be greater than 0')
        
        # Verificar se o produto já existe no Carrinho
        for index, item in enumerate(cart.items):
            if item.product_id == product.id:
                # Atualizar a quantidade do item no carrinho
                CartItemRepository.edit_cart_item_quantity_by_id(
                    cart_item_id=item.id,
                    quantity=item.quantity + int(data['quantity'])
                )
                break

            elif index == len(cart) - 1:
                # Adicionar item ao carrinho
                CartItemRepository.create_cart_item(product_id=product.id, cart_id=cart.id, quantity=int(data['quantity']))

        if len(cart.items) == 0:
            # Adicionar item ao carrinho
            CartItemRepository.create_cart_item(product_id=product.id, cart_id=cart.id, quantity=int(data['quantity']))
