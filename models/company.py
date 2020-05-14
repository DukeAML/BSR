from db import db


class CompanyModel(db.Model):
    __tablename__ = 'companies'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    channel = db.Column(db.String(20))

    orders = db.relationship('OrderModel', lazy='dynamic')

    def __init__(self, uid, name, channel):
        self.uid = uid
        self.name = name
        self.channel = channel

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
