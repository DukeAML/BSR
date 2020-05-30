from flask import Flask
from flask_restful import Api
import pathlib

from db import db
from resources.expense import Expense, ExpenseRange
from resources.order import Order, OrderRange
from resources.company import Company
from resources.product import Product, ProductHistory

PATH = pathlib.Path(__file__).parent
PASSWORD = "postgres"
SWEET_API_KEY = "44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373"
SWEET_HEADERS = {'Content-Type': 'application/json'}

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:{}@localhost/bsrdata'.format(PASSWORD)#'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


from models.order import OrderModel
@app.before_first_request
def update():
    OrderModel.update()


# currently date must be in YYYY-mm-dd format
api.add_resource(Expense, '/expense/<string:date>')
api.add_resource(ExpenseRange, '/expenses')
api.add_resource(Order, '/order/<int:id>&<string:shopify>')
api.add_resource(OrderRange, '/orders')
api.add_resource(Company, '/company/<int:id>')
api.add_resource(Product, '/product/<int:id>')
api.add_resource(ProductHistory, '/history/product/<int:id>')


if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
