from flask import Blueprint, request, jsonify

from ..repositories.stock_order_repository import StockOrderRepository
from ..services.request_order_supply import OrderSupplyService

stock_order_blueprint = Blueprint('stock_order', __name__)

@stock_order_blueprint.route('/', methods=['GET'])
def list():
    stocks = []

    for stock in StockOrderRepository.get_all_stock_orders():
        stocks.append({
            'id': stock.id,
            'product_id': stock.product_id,
            'quantity': stock.quantity,
            'cart_id': stock.cart_id,
        })

    return jsonify(stocks), 200


@stock_order_blueprint.route('/supply', methods=['POST'])
def request_supplier():
    try:
        OrderSupplyService.process_supply()
        return jsonify({'message': 'Request for supplier processed, stock is now supplied.'}), 200
    except Exception as err:
        return jsonify({'message': str(err)}), 400
