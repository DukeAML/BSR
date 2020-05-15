from flask import Flask
from flask_restful import Api

from db import db
from resources.expense import Expense, ExpenseRange
from resources.order import Order, OrderRange
from resources.company import Company
from resources.product import Product, ProductHistory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)


#temporary since don't have production database
@app.before_first_request
def create_tables():
    db.create_all()

    # from datetime import datetime
    # from models.order import OrderModel
    # temporder = OrderModel(12345, datetime(2019,1,1).date(), datetime(2019,1,1).date(), datetime(2019,1,1).date(), 47.2, 456)
    # temp2order = OrderModel(12346, datetime(2019,1,15).date(), datetime(2019,1,15).date(), datetime(2019,1,15).date(), 47.2, 456)
    # temp3order = OrderModel(12347, datetime(2019,1,29).date(), datetime(2019,1,29).date(), datetime(2019,1,29).date(), 47.2, 457)
    # db.session.add(temporder)
    # db.session.add(temp2order)
    # db.session.add(temp3order)

    # from models.company import CompanyModel
    # tempcomp = CompanyModel(456, 'Tonys Pizzeria', 'Restaurant')
    # db.session.add(tempcomp)

    # from models.product import ProductModel
    # tempro = ProductModel(1, "SOME-THIN-H12oz.", 12.4)
    # db.session.add(tempro)

    # from models.orderitems import OrderItemsModel
    # tempoi = OrderItemsModel(6, 12345, 1)
    # tempoi2 = OrderItemsModel(3, 12345, 2)
    # tempoi3 = OrderItemsModel(6, 12346, 1)
    # tempoi4 = OrderItemsModel(6, 12347, 1)
    # db.session.add(tempoi)
    # db.session.add(tempoi2)
    # db.session.add(tempoi3)
    # db.session.add(tempoi4)

    # from models.expense import ExpenseModel
    # tempe = ExpenseModel(datetime(2019,1,29).date(), 457.60)
    # tempe2 = ExpenseModel(datetime(2019,2,5).date(), 34.70)
    # db.session.add(tempe)
    # db.session.add(tempe2)

    # db.session.commit()



# currently date must be in YYYY-mm-dd format
api.add_resource(Expense, '/expense/<string:date>')
api.add_resource(ExpenseRange, '/expenses')
api.add_resource(Order, '/order/<int:id>')
api.add_resource(OrderRange, '/orders')
api.add_resource(Company, '/company/<int:id>')
api.add_resource(Product, '/product/<int:id>')
api.add_resource(ProductHistory, '/history/product/<int:id>')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
