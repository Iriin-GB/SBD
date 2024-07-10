from ...infra.database import db

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)

    cart = db.relationship('Cart', uselist=False, backref='customer')
