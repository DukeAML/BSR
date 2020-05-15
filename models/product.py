from db import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    uid = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(200))
    price = db.Column(db.Float(precision=2))

    orderinstances = db.relationship('OrderItemsModel', lazy='dynamic')

    def __init__(self, uid, sku, price):
        self.uid = uid
        self.sku = sku
        self.price = price

    def json(self):
        return {'product_id': self.uid, 'sku': self.sku,
                'price': self.price}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(uid=id).first()
