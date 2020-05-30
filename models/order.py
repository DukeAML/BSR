import json
import requests
import time

from db import db
from sqlalchemy.sql import func
from models.company import CompanyModel
from models.orderitems import OrderItemsModel
from models.product import ProductModel


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
    def getOrders(cls, date, pageNum):
        """Retrieve all non-cancelled orders after date from page pageNum from getsweet api."""
        from testapp import SWEET_API_KEY, SWEET_HEADERS
        payload = {'token': SWEET_API_KEY, 'page':pageNum, 'q[invoice_date_gteq]':date, 'q[state_not_eq]':'canceled'}
        return requests.get(url='https://app.getsweet.com/api/v1/orders.json', headers=SWEET_HEADERS, params=payload).json()

    @classmethod
    def parseOrder(cls, data):
        """Return only relevant key:value pairs from getsweet api call formatted to fit OrderModel class."""
        if data['number'][0] == "R":
            shopify = True
            order_id = data['number'][1:]
        else:
            shopify = False
            order_id = data['number']

        return {'uid': order_id, 'shopify': shopify, 'submitted_date': data['submitted_at'], 'due_date': data['due_date'], 'invoice_date': data['invoice_date'], 'cost': data['payment_total'], 'company_id': data['account']['id']}

    @classmethod
    def update(cls):
        """Update 'orders' table by pulling most recent submitted_date from database and then calling all orders following that date from the getsweet api. Update 'orderitems', 'companies' and 'products' tables based on new order information.
        """
        print("Updating orders, orderitems, companies, and products tables.")
        newest_date = db.session.query(func.max(OrderModel.submitted_date)).one()[0]
        total_pages = cls.getOrders(newest_date, 1)['meta']['total_pages']

        # access each page available
        for page in range(1, total_pages+1):
            order_data = cls.getOrders(newest_date, page)

            # pause if API unresponsive
            while ('orders' not in order_data):
                print("Pausing execution for API time delay on orders...")
                time.sleep(10)
                order_data = getOrders(newest_date, page)
            print("Integrating orders page:", page)

            # record each order's information
            for order in order_data['orders']:
                if cls.find_by_id(cls.parseOrder(order)['uid'], cls.parseOrder(order)['shopify']): continue

                # check if company exists in db, if not, add it
                company_id = order["account"]["id"]
                if CompanyModel.find_by_id(company_id) is None:
                    company_data = CompanyModel.getCompany(company_id)

                    # pause if API unresponsive
                    while ('customer' not in company_data):
                        print("Pausing execution for API time delay on company retrieval...")
                        print("-> id =", company_id)
                        time.sleep(10)
                        company_data = CompanyModel.getCompany(company_id)

                    # insert company into database
                    c = company_data['customer']
                    company_insert = CompanyModel(c['id'],
                                        c['fully_qualified_name'],
                                        c['customer_type_id'])
                    CompanyModel.save_to_db(company_insert, False)

                # place order into db
                order_insert = OrderModel(**cls.parseOrder(order))
                cls.save_to_db(order_insert, False)

                # check if order's product(s) exist in db, if not, add them
                for product in order["line_items"]:
                    product_id = product["variant_id"]
                    if ProductModel.find_by_id(product_id) is None:
                        product_data = ProductModel.getProduct(product_id)

                        # pause if API unresponsive
                        while ('variant' not in product_data):
                            print("Pausing execution for API time delay on product retrieval...")
                            time.sleep(10)
                            product_data = ProductModel.getProduct(product_id)

                        # insert product into database
                        p = product_data['variant']
                        product_insert = ProductModel(uid=p['id'], name=p['fully_qualified_name'], sku=p['sku'], active=p['active'], price=p['price'])
                        ProductModel.save_to_db(product_insert, False)

                    # place order instance into db with individual product
                    orderitems_insert = OrderItemsModel(product['quantity'], order_insert.uid, order_insert.shopify, product['variant_id'])
                    OrderItemsModel.save_to_db(orderitems_insert, False)

                try:
                    db.session.commit()
                except:
                    print("Issue inserting order (& values) with id:", cls.parseOrder(order)['uid'])


    @classmethod
    def find_by_id(cls, id, shopify):
        """Return order from database with order_id id."""
        return cls.query.filter_by(uid=id, shopify=shopify).first()

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
