from flask import Blueprint, request, jsonify

from ..services.sale_service import SaleService

sale_blueprint = Blueprint('sale', __name__)

@sale_blueprint.route('/', methods=['POST'])
def sale():
    data = request.get_json()
    
    try:
        total_price = SaleService.process_sale(data)
        return jsonify({'message': f'Sale processed, total was {total_price}.'}), 200
    except Exception as err:
        return jsonify({'message': str(err)}), 400