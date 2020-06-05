from models.batch import BatchModel
from models.company import CompanyModel
from models.expense import ExpenseModel
from models.order import OrderModel
from models.product import ProductModel
from models.ingredient import IngredientModel

if __name__ == "__main__":
    BatchModel.init_fill_db()
    CompanyModel.init_fill_db()
    ProductModel.init_fill_db()
    ExpenseModel.init_fill_db()
    OrderModel.init_fill_db()
    IngredientModel.init_fill_db()

