from ...infra.database import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
