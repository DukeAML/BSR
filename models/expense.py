from db import db


class ExpenseModel(db.Model):
    __tablename__ = 'expenses'

    date = db.Column(db.Date, primary_key=True)
    payments = db.Column(db.Float(precision=2))

    def __init__(self, date, payments):
        self.date = date
        self.payments = payments

    def json(self):
        return {'date': str(self.date), 'payments': self.payments}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_date(cls, date):
        return cls.query.filter_by(date=date).first()

    @classmethod
    def init_fill_db(cls):
        import csv
        import psycopg2
        from testapp import PATH, PASSWORD

        conn = psycopg2.connect(host="localhost", dbname="bsrdata", user="postgres", password=PASSWORD)
        cur = conn.cursor()

        with open(PATH.joinpath('data\expense_data.csv'), 'r') as f:
            reader = csv.reader(f)
            next(reader) # skip header row

            for row in reader:

                try:
                    cur.execute(
                        "INSERT INTO expenses VALUES (%s, %s)",
                        (row[0], row[1])
                    )
                except:
                    print("There was an error inserting expense on date: ", str(row[0]))

        conn.commit()
