from db import db
from models.product import ProductModel


class OrderItemsModel(db.Model):
    __tablename__ = 'orderitems'

    quantity = db.Column(db.Integer)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.uid'),
                            primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.uid'),
                            primary_key=True)
    order = db.relationship('OrderModel')
    product = db.relationship('ProductModel')

    def __init__(self, quantity, order_id, product_id):
        self.quantity = quantity
        self.order_id = order_id
        self.product_id = product_id

    def json(self):
        return {'order_id': self.order_id, 'product_id': self.product_id,
                'quantity': self.quantity}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
