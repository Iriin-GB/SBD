from ..infra.database import db
from ..domain.models.product import Product

class ProductRepository:
    @staticmethod
    def get_product_by_id(product_id: int):
        return Product.query.get(product_id)


    @staticmethod
    def get_all_products():
        return Product.query.all()


    @staticmethod
    def create_product(name: str, price: float, stock: int):
        product = Product(name=name, price=price, stock=stock)
        db.session.add(product)
        db.session.commit()
        return product
    

    @staticmethod
    def edit_product_stock_by_id(product_id: int, stock: int):
        product = Product.query.get(product_id)
        product.stock = stock # Atualizando stock
        db.session.commit()
        return product
