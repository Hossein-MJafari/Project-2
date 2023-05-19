from . import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    price = db.Column(db.Float)
    image = db.Column(db.Text, unique=True, nullable=False)
    info = db.Column(db.String(200))