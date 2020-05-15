from db import db
from datetime import datetime
from flask_restful import Resource, reqparse, inputs
from models.product import ProductModel
from models.order import OrderModel
from models.orderitems import OrderItemsModel


class Product(Resource):

    def get(self, id):
        product = ProductModel.find_by_id(id)
        if product:
            return product.json()
        return {'message': 'Product not found'}, 404


class ProductHistory(Resource):

    def get(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('start_date',
                            type=inputs.date,
                            required=True,
                            help="This field cannot be left blank.")
        parser.add_argument('end_date',
                            type=inputs.date,
                            required=False,
                            help="Specify an ending date.")
        args = parser.parse_args()
        starting_date = args['start_date'].date()
        if not args['end_date']: ending_date = datetime.now().date()
        else: ending_date = args['end_date'].date()

        product = ProductModel.find_by_id(id)
        if not product: return {'message': 'Product not found'}, 404

        info = db.session.query(ProductModel, OrderItemsModel, OrderModel)\
                    .filter(
                        ProductModel.uid == id,
                        ProductModel.uid == OrderItemsModel.product_id,
                        OrderItemsModel.order_id == OrderModel.uid,
                        OrderModel.submitted_date.between(starting_date, ending_date)
                    ).all()

        return {'product_id': id,
                'transaction_history': [
                        {
                        'date': str(row.OrderModel.submitted_date),
                        'quantity': row.OrderItemsModel.quantity
                        }
                        for row in info]
                }
