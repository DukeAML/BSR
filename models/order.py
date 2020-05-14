from db import db
from models.company import CompanyModel
from models.orderitems import OrderItemsModel


class OrderModel(db.Model):
    __tablename__ = 'orders'

    uid = db.Column(db.Integer, primary_key=True)
    submitted_date = db.Column(db.Date)
    due_date = db.Column(db.Date)
    invoice_date = db.Column(db.Date)
    cost = db.Column(db.Float(precision=2))

    company_id = db.Column(db.Integer, db.ForeignKey('companies.uid'))
    company = db.relationship('CompanyModel')
    content = db.relationship('OrderItemsModel', lazy='dynamic')

    def __init__(self, uid, submitted_date, due_date, invoice_date, cost, company_id):
        self.uid = uid
        self.submitted_date = submitted_date
        self.due_date = due_date
        self.invoice_date = invoice_date
        self.cost = cost
        self.company_id = company_id

    def json(self):
        return {'order_id': self.uid, 'company_id': self.company_id,
                'paid': self.cost, 'submitted_date': str(self.submitted_date),
                'due_date': str(self.due_date), 'invoice_date': str(self.invoice_date), 'items': [item.json(hide_oid=True) for item in self.content.all()]}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(uid=id).first()
