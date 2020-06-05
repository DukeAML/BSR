from db import db


class IngredientModel(db.Model):
    __tablename__ = 'ingredients'


    uid = db.Column(db.Integer, primary_key=True)
    sku = db.Column(db.String(50))
    name = db.Column(db.String(150))
    cost_price = db.Column(db.Float(precision=2))
    pack_size = db.Column(db.Float(precision=2)) # in lbs.
    on_hand = db.Column(db.Float(precision=5)) # getsweet rounds to 5 places
    available = db.Column(db.Float(precision=5))
    committed = db.Column(db.Float(precision=5))

    batch_uses = db.relationship('RecipeModel', lazy='dynamic')

    def __init__(self, uid, sku, name, cost_price, pack_size, on_hand, available, committed):
        self.uid = uid
        self.sku = sku
        self.name = name
        self.cost_price = cost_price
        self.pack_size = pack_size
        self.on_hand = on_hand
        self.available = available
        self.committed = committed

    def json(self):
        return {'ingredient_id': self.uid, 'sku': self.sku, 'name': self.name,
                'cost_price': self.cost_price,
                'pack_size (lbs)': self.pack_size, 'on_hand': self.on_hand,
                'available': self.available, 'committed': self.committed}

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
        import json
        import psycopg2
        from testapp import PATH, PASSWORD

        conn = psycopg2.connect(host="localhost", dbname="bsrdata", user="postgres", password=PASSWORD)
        cur = conn.cursor()

        with open(PATH.joinpath('data\ingredients.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                # catch missing pack_size
                try:
                    pack_size = float(row[6][:-3])
                except:
                    pack_size = None

                if (row[0] == "L90D"): pack_size = 617.0
                if (row[0] == "I-CHOC-70%"): pack_size = 22.05
                if (row[0] == "I-LECITHIN"): pack_size = 8.6
                if (row[0] == "I-SUN-LECITHIN"): pack_size = 41.89

                # parse stock info
                stock_info = row[8][1:-1].replace("'", "\"")
                stock_info = stock_info.replace('"backorderable": False, ', '')
                stock_info = stock_info.replace('"backorderable": True, ', '')
                stockdict = json.loads(stock_info)


                cur.execute(
                    "INSERT INTO ingredients VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (row[1], row[0], row[3], row[2], pack_size, stockdict['on_hand'], stockdict['available'], stockdict['committed'])
                )


        conn.commit()
