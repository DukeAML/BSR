from flask_restful import Resource
from models.company import CompanyModel


class Company(Resource):

    def get(self, id):
        company = CompanyModel.find_by_id(id)
        if company:
            return company.json()
        return {'message': 'Date not found'}, 404
