from db import db


class IngredientModel(db.Model):
    __tablename__ = 'ingredients'

    sku = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(150))
    cost_price = db.Column(db.Float(precision=2))
    pack_size = db.Column(db.Float(precision=2)) # in lbs.
    on_hand = db.Column(db.Float(precision=5)) # getsweet rounds to 5 places
    available = db.Column(db.Float(precision=5))
    committed = db.Column(db.Float(precision=5))

    batch_uses = db.relationship('RecipeModel', lazy='dynamic')

    def __init__(self, sku, name, cost_price, pack_size, on_hand, available, committed):
        self.sku = sku
        self.name = name
        self.cost_price = cost_price
        self.pack_size = pack_size
        self.on_hand = on_hand
        self.available = available
        self.committed = committed

    def json(self):
        return {'sku': self.sku, 'name': self.name,
                'cost_price': self.cost_price,
                'pack_size (lbs)': self.pack_size, 'on_hand': self.on_hand,
                'available': self.available, 'committed': self.committed}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
