from company import CompanyModel
from expense import ExpenseModel
from order import OrderModel
from product import ProductModel

if __name__ == "__main__":
    CompanyModel.init_fill_db()
    ProductModel.init_fill_db()
    ExpenseModel.init_fill_db()
    OrderModel.init_fill_db()
