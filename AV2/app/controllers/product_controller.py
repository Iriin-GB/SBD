from flask import Blueprint, request, jsonify

from ..repositories.product_repository import ProductRepository

product_blueprint = Blueprint('product', __name__)

@product_blueprint.route('/add', methods=['POST'])
def create_product():
    data = request.get_json()
    ProductRepository.create_product(name=data['name'], price=data['price'], stock=data['stock'])
    return jsonify({'message': 'Product created.'}), 200


@product_blueprint.route('/', methods=['GET'])
def get_products():
    products = ProductRepository.get_all_products()

    # Serializar dados para JSON
    serializer = []

    for product in products:
        serializer.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'stock': product.stock,
        })

    return jsonify(serializer), 200
