from db import db


class BatchModel(db.Model):
    __tablename__ = 'batches'

    uid = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(75))
    sweet_reference = db.Column(db.String(30))
    weight = db.Column(db.Float(precision=2)) # csv rounds to 2 places, in lbs

    ingredients = db.relationship('RecipeModel', lazy='dynamic')
    products = db.relationship('ProductModel', lazy='dynamic')

    def __init__(self, uid, name, sweet_reference, weight):
        self.uid = uid
        self.name = name
        self.sweet_reference = sweet_reference
        self.weight = weight

    def json(self):
        return {'batch_id': self.uid,
                'name': self.name,
                'getsweet_reference': self.sweet_reference,
                'weight (lbs)': self.weight}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
