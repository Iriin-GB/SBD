from ...infra.database import db

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    items = db.relationship('CartItem', back_populates='cart')

    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
