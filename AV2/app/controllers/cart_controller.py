from flask import Blueprint, request, jsonify
from ..services.product_on_cart_service import ProductOnCartService

from ..repositories.customer_repository import CustomerRepository
from ..repositories.cart_repository import CartRepository
from ..repositories.product_repository import ProductRepository

cart_blueprint = Blueprint('cart', __name__)

@cart_blueprint.route('/add', methods=['POST'])
def add_product_on_cart():
    data = request.get_json()

    try:
        ProductOnCartService.process_product_on_cart(data)
    except Exception as err:
        return jsonify({'message': str(err)}), 400

    if data['quantity'] > 1:
        return jsonify({'message': 'Products added on cart.'}), 200

    return jsonify({'message': 'Product added on cart.'}), 200


@cart_blueprint.route('/', methods=['GET'])
def get_cart_items():
    customer_email = request.args['customer_email']
    
    # Verificando customer
    customer = CustomerRepository.get_customer_by_email(customer_email)

    if not customer: # Criar customer
        customer = CustomerRepository.create_customer(email=customer_email)

    # Procurar carrinho
    cart = CartRepository.get_cart_by_customer_id(customer.id)

    if not cart: # Criar carrinho
        cart = CartRepository.create_cart(customer_id=customer.id)

    products = [] # Criar lista de produtos

    # Recebendo os produtos
    for item in cart.items:
        product = ProductRepository.get_product_by_id(item.product_id)

        products.append({
            'name': product.name,
            'price': product.price,
            'quantity': item.quantity,
        })

    return jsonify(products), 200