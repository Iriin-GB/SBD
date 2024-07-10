from ...infra.database import db

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    quantity = db.Column(db.Integer, nullable=False)

    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), unique=False, nullable=False)
    cart = db.relationship('Cart', back_populates='items')
