from datetime import datetime
from flask_restful import Resource, reqparse, inputs
from models.expense import ExpenseModel


class Expense(Resource):

    def get(self, date):
        expense = ExpenseModel.find_by_date(date)
        if expense:
            return expense.json()
        return {'message': 'Date not found'}, 404


class ExpenseRange(Resource):

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

        expenses = ExpenseModel.query.filter(ExpenseModel.date.
                                between(starting_date, ending_date))
        if expenses:
            return {'expenditures': [expenditure.json() for expenditure in expenses]}
        return {'message': 'Range provided not valid'}, 404

