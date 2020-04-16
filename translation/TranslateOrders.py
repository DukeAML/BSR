from products_to_base import Order
import pandas as pd

def order_translation(orders):
    '''
    order: csv of forecasted orders in format given by "two_week_proj_withSKU.csv"
    returns df of   
    '''

    order = pd.read_csv(orders)  #get niko's projections
    order = pd.DataFrame(order)

    lst = {}
    for sku in order["sku"]:
        amt = order.loc[order['sku'] == sku]["proj_sales"]
        amt = amt.reset_index().drop(columns = ["index"])
        amt = amt.lookup(row_labels =[0], col_labels=["proj_sales"])
        amt  = float(amt[0])

        if sku not in lst:
            lst[sku] = amt
        elif sku in lst:
            lst[sku] += amt


    order = Order(lst)
    order.get_base()
    base = order.base #get base

    new_amt = pd.DataFrame()
    new_amt["sku"] = base.keys()
    new_amt["amt"] = base.values()


    temp2 = pd.read_csv('base-products.csv')  #can be replaced with emily's df later
    base_products = pd.DataFrame(temp2)

    skus = base_products["sku"]
    skus = [item[1] for item in skus.items()]
    skus = [item.strip(" '' ") for item in skus]

    helperA ={}
    helperB= {}

    for sku in skus: 
        stock = base_products.loc[base_products['sku'] == sku]["stock"]
        stock = stock.reset_index().drop(columns = ["index"])
        stock = stock.lookup(row_labels =[0], col_labels=["stock"])
        stock = stock.tolist()[0]
        stock = stock.strip("[]")
        stock = ast.literal_eval(stock)

        have = float(stock["on_hand"]) 
        committed = float(stock["committed"])

        helperA[sku] = have
        helperB[sku] = committed

    df = pd.DataFrame()
    df["sku"] = helperA.keys()
    df["available"] = helperA.values()
    df["prev committed"] = helperB.values()

    new_amt = []
    for sku in skus:
        if sku in base:
            new_amount = base[sku]
        elif sku not in base:
            new_amount = helperB[sku]
        new_amt.append(new_amount)

    df["updated committed"] = new_amt
    df["left over"] = df["available"] - df["updated committed"]
    df["name"] = base_products["fully_qualified_name"]
    df.to_csv('updated_baseinventory.csv', index = False)

    return df




