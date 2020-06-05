import json
import datetime
import requests
import time

from db import db
from models.ingredient import IngredientModel
from models.recipe import RecipeModel


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

    @classmethod
    def getBatches(cls, pageNum=1):
        """Retrieve all non-cancelled orders after date from page pageNum from getsweet api."""
        from testapp import SWEET_API_KEY, SWEET_HEADERS
        payload = {'token': SWEET_API_KEY, 'page':pageNum, 'q[product_type_not_eq]': "inventory_item"}
        return requests.get(url='https://app.getsweet.com/api/v1/products', headers=SWEET_HEADERS, params=payload).json()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(uid=id).first()

    @classmethod
    def init_fill_db(cls):
        """Call the api to fill db tables batches, recipe with initial information."""
        from models.product import ProductModel
        print("Instantiating batches and recipe tables.")
        ###batch_asset_id = 1055
        total_pages = cls.getBatches()['meta']['total_pages']

        # access each page available
        for page in range(1, total_pages+1):
            batch_data = cls.getBatches()

            # pause if API unresponsive
            while ('products' not in batch_data):
                print("Pausing execution for API time delay on batches...")
                time.sleep(10)
                batch_data = cls.getBatches(page)
            print("Integrating batches page: {} / {}".format(page, total_pages))

            # record each batch's information
            for product in batch_data['products']:
                if product["active"]==True and product["name"]=="BATCH":
                    for batch in product['variants']:
                        if cls.find_by_id(batch['id']): continue
                        print("Found batch with id: ", batch['id'])

                        # insert batch into database
                        batch_insert = BatchModel(uid=batch['id'], name=batch['fully_qualified_name'], sweet_reference=batch['sku'], weight=batch['weight'])
                        cls.save_to_db(batch_insert, False)

                        # check if batch's ingredients(s) exist in db, if not, add them
                        for ingredient in batch["components"]:
                            ingredient_id = ingredient["id"]
                            if IngredientModel.find_by_id(ingredient_id) is None:
                                ingredient_data = ProductModel.getProduct(ingredient_id)

                                # pause if API unresponsive
                                while ('variant' not in ingredient_data):
                                    print("Pausing execution for API time delay on product retrieval...")
                                    time.sleep(10)
                                    ingredient_data = ProductModel.getProduct(ingredient_id)

                                # insert ingredient into database
                                i = ingredient_data['variant']
                                try: size = float(i['pack_size'][:-3])
                                except: size = None
                                ingredient_insert = IngredientModel(uid=i['id'], sku=i['sku'], name=i['fully_qualified_name'], cost_price=i['cost_price'], pack_size=size, on_hand=i['stock_items'][0]['on_hand'], available=i['stock_items'][0]['available'], committed=i['stock_items'][0]['committed'])
                                IngredientModel.save_to_db(ingredient_insert, False)

                            # place recipe instance into db with individual product
                            recipe_insert = RecipeModel(quantity=ingredient['quantity'], batch_id=batch['id'], ingredient_id=ingredient['id'])
                            RecipeModel.save_to_db(recipe_insert, False)

                        try:
                            db.session.commit()
                        except:
                            print("Issue inserting batch (& values) with id:", batch['id'])


