from db import db


class ProductModel(db.Model):
    __tablename__ = 'products'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    sku = db.Column(db.String(50))
    active = db.Column(db.Boolean)
    price = db.Column(db.Float(precision=2))

    orderinstances = db.relationship('OrderItemsModel', lazy='dynamic')

    def __init__(self, uid, sku, price, name, active):
        self.uid = uid
        self.name = name
        self.sku = sku
        self.price = price
        self.active = active

    def json(self):
        return {'product_id': self.uid, 'sku': self.sku,
                'name': self.name, 'price': self.price, 'active': self.active}

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

        with open(PATH.joinpath('data\products_for_db.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                try:
                    cur.execute(
                        "INSERT INTO products VALUES (%s, %s, %s, %s, %s)",
                        (row[0], row[3], row[1], row[4], row[2])
                    )
                except:
                    print("There was an error inserting product with id: ", str(row[0]))

        conn.commit()
