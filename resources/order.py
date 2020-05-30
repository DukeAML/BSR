from datetime import datetime
from flask_restful import Resource, reqparse, inputs
from models.order import OrderModel


class Order(Resource):

    def get(self, id, shopify):
        order = OrderModel.find_by_id(id, shopify)
        if order:
            return order.json()
        return {'message': 'Date not found'}, 404


class OrderRange(Resource):

    def get(self):
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

        orders = OrderModel.query.filter(OrderModel.due_date.
                                between(starting_date, ending_date))
        if orders:
            return {'orders': [order.json() for order in orders]}
        return {'message': 'Range provided not valid'}, 404

