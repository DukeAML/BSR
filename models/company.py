from db import db


class CompanyModel(db.Model):
    __tablename__ = 'companies'

    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    channel = db.Column(db.Integer)

    orders = db.relationship('OrderModel', lazy='dynamic')

    def __init__(self, uid, name, channel):
        self.uid = uid
        self.name = name
        self.channel = channel

    def json(self):
        return {'company_id': self.uid, 'company_name': self.name,
                'company_type': self.channel}

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

        with open(PATH.joinpath('data\customer_type_map.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                # catch missing type ids
                try:
                    type_id = int(float(row[2]))
                except:
                    type_id = None

                # actual insert statement
                try:
                    cur.execute(
                        "INSERT INTO companies VALUES (%s, %s, %s)",
                        (row[1], row[0], type_id)
                    )
                except:
                    print("There was an error inserting company with id: ", str(row[1]))

        conn.commit()
