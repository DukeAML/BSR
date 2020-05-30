from db import db
from models.ingredient import IngredientModel


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    quantity = db.Column(db.Float(precision=3)) # getsweet rounds to 3 places

    batch_id = db.Column(db.BigInteger, db.ForeignKey('batches.uid'),
                                    primary_key=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.uid'),
                                    primary_key=True)
    batch = db.relationship('BatchModel')
    ingredient = db.relationship('IngredientModel')

    def __init__(self, batch_id, ingredient_id, quantity):
        self.batch_id = batch_id
        self.ingredient_id = ingredient_id
        self.quantity = quantity

    def json(self):
        return {'batch_id': self.batch_id,
                'ingredient_id': self.ingredient_id,
                'ingredient_quantity (lbs)': self.quantity}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
