from datetime import datetime
from flask_restful import Resource
from models.expense import ExpenseModel


class Expense(Resource):

    def get(self, date):
        expense = ExpenseModel.find_by_date(date)
        if expense:
            return expense.json()
        return {'message': 'Date not found'}, 404


class ExpenseRange(Resource):

    def get(self, starting_date, ending_date):
        expenses = ExpenseModel.query.filter(ExpenseModel.date.
                                between(starting_date, ending_date))
        if expenses:
            return {'expenditures': [expenditure.json() for expenditure in expenses]}
        return {'message': 'Range provided not valid'}, 404

