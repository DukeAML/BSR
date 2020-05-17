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
    shopify = db.Column(db.Boolean, primary_key=True)

    company_id = db.Column(db.Integer, db.ForeignKey('companies.uid'))
    company = db.relationship('CompanyModel')
    content = db.relationship('OrderItemsModel', lazy='dynamic')

    def __init__(self, uid, shopify, submitted_date, due_date, invoice_date, cost, company_id):
        self.uid = uid
        self.shopify = shopify
        self.submitted_date = submitted_date
        self.due_date = due_date
        self.invoice_date = invoice_date
        self.cost = cost
        self.company_id = company_id

    def json(self):
        if self.shopify:
            return {'order_id': 'R' + str(self.uid),
                    'company_id': self.company_id,
                    'paid': self.cost,
                    'submitted_date': str(self.submitted_date),
                    'due_date': str(self.due_date),
                    'invoice_date': str(self.invoice_date),
                    'items': [item.json(hide_oid=True)
                                for item in self.content.all()]}
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

    @classmethod
    def init_fill_db(cls):
        import csv
        import psycopg2
        from testapp import PATH, PASSWORD

        conn = psycopg2.connect(host="localhost", dbname="bsrdata", user="postgres", password=PASSWORD)
        cur = conn.cursor()

        # insert all orders
        with open(PATH.joinpath('data\order_data.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                if row[3][0] == "R":
                    shopify = True
                    order_id = row[3][1:]
                else:
                    shopify = False
                    order_id = row[3]

                try:
                    cur.execute(
                        "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s)",
                        (order_id, row[0], row[1], row[2], row[6], shopify, row[5])
                    )
                except:
                    print("There was an error inserting order with id: ", str(order_id))

        conn.commit()

        # insert all order instances
        with open(PATH.joinpath('data\order_data.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                if row[3][0] == "R":
                    shopify = True
                    order_id = row[3][1:]
                else:
                    shopify = False
                    order_id = row[3]

                for item in row[8]:
                    try:
                        cur.execute(
                            "INSERT INTO orderitems VALUES (%s, %s, %s, %s)",
                            (item[2], order_id, shopify, item[0])
                        )
                    except:
                        print("There was an error inserting order instance with order id: {} and product id: {}".format(order_id, item[0]))

        conn.commit()
