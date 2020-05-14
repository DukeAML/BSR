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
