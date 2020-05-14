from datetime import datetime
from flask_restful import Resource, reqparse
from models.order import OrderModel


class Order(Resource):

    def get(self, id):
        print(OrderModel.query.all())
        order = OrderModel.find_by_id(id)
        if order:
            return order.json()
        return {'message': 'Date not found'}, 404


class OrderRange(Resource):

    def get(self, starting_date, ending_date):
        orders = OrderModel.query.filter(OrderModel.due_date.
                                between(starting_date, ending_date))
        print("here: " + starting_date + " - " + ending_date)
        print(orders)
        print("---")
        print([order.json() for order in orders])
        print('---')
        print(OrderModel.query.all())
        if orders:
            return {'orders': [order.json() for order in orders]}
        return {'message': 'Range provided not valid'}, 404

