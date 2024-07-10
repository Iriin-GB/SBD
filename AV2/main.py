from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from app.infra.database import db
from app.controllers.sale_controller import sale_blueprint
from app.controllers.cart_controller import cart_blueprint
from app.controllers.product_controller import product_blueprint
from app.controllers.stock_order_controller import stock_order_blueprint


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

    db.init_app(app)

    app.register_blueprint(sale_blueprint, url_prefix='/api/sale')
    app.register_blueprint(cart_blueprint, url_prefix='/api/cart')
    app.register_blueprint(product_blueprint, url_prefix='/api/products')
    app.register_blueprint(stock_order_blueprint, url_prefix='/api/stock')
    
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
