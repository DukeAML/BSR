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
        import time
        from testapp import PATH, PASSWORD
        from data.getCustomerType import addCMap

        conn = psycopg2.connect(host="localhost", dbname="bsrdata", user="postgres", password=PASSWORD)
        cur = conn.cursor()

        # insert all orders
        with open(PATH.joinpath('data\order_data.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                if row[3] == '19906' or row[3] == '20815' or row[3] == '20781' or row[3] == '20821': continue

                if row[3][0] == "R":
                    shopify = True
                    order_id = row[3][1:]
                else:
                    shopify = False
                    order_id = row[3]
                company_id = row[5]


                cur.execute("SELECT * FROM companies WHERE uid = (%s)", (company_id,))
                exists = len(cur.fetchall()) != 0
                if not exists:
                    cdata = addCMap(company_id)
                    while ('customer' not in cdata):
                        time.sleep(10)
                        cdata = addCMap(company_id)
                    cid = cdata['customer']['id']
                    cname = cdata['customer']['fully_qualified_name']
                    ctype = cdata['customer']['customer_type_id']
                    cur.execute(
                        "INSERT INTO companies VALUES (%s, %s, %s)",
                        (cid, cname, ctype)
                    )

                cur.execute(
                    "INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (order_id, row[0], row[1], row[2], row[6], shopify, company_id)
                )

        conn.commit()

        # part 2: order instances
        import json
        from data.temptransfer import pullProduct

        # insert all order instances
        with open(PATH.joinpath('data\order_data.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                if row[3] == '19906' or row[3] == '20815' or row[3] == '20781' or row[3] == '20821': continue

                if row[3][0] == "R":
                    shopify = True
                    order_id = row[3][1:]
                else:
                    shopify = False
                    order_id = row[3]


                itemdict = dict()
                for item in json.loads(row[8]):

                    pid = item[0]
                    cur.execute("SELECT * FROM products WHERE uid = (%s)", (pid,))
                    exists = len(cur.fetchall()) != 0
                    if not exists:
                        data = pullProduct(pid)
                        while ('variant' not in data):
                            print("Pausing execution for API time delay...")
                            time.sleep(10)
                            data = pullProduct(pid)
                        psku = data['variant']['sku']
                        pprice = data['variant']['price']
                        pname = data['variant']['fully_qualified_name']
                        pactive = data['variant']['active']
                        cur.execute(
                            "INSERT INTO products VALUES (%s, %s, %s, %s, %s)",
                            (pid, pname, psku, pactive, pprice)
                        )

                    if pid in itemdict: itemdict[pid] += item[2]
                    else: itemdict[pid] = item[2]

                for pid,quantity in itemdict.items():
                    cur.execute(
                        "INSERT INTO orderitems VALUES (%s, %s, %s, %s)",
                        (quantity, order_id, shopify, pid)
                    )

        conn.commit()
