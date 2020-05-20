from db import db


class RecipeModel(db.Model):
    __tablename__ = 'recipes'

    quantity = db.Column(db.Float(precision=3)) # getsweet rounds to 3 places

    batch_id = db.Column(db.TYPE_NOT_SURE_YET, db.ForeignKey('batches.uid'))
    ingredient_sku = db.Column(db.String(50), db.ForeignKey('ingredients.sku'))
    batch = db.relationship('BatchModel')
    ingredient = db.relationship('IngredientModel')

    def __init__(self, batch_id, ingredient_sku, quantity):
        self.batch_id = batch_id
        self.ingredient_sku = ingredient_sku
        self.quantity = quantity

    def json(self):
        return {'batch_id': self.batch_id,
                'ingredient_sku': self.ingredient_sku,
                'ingredient_quantity (lbs)': self.quantity}

    def save_to_db(self, commit=True):
        db.session.add(self)
        if commit: db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
