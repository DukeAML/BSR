import requests
import json
import pandas as pd
import time

'''
    generates ingredients.csv, which is a csv of ingredients only
'''


API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/products.json'

columns = ["sku", "ID", "cost_price", "fully_qualified_name", "active", "incremental_order_quantity",
           "pack_size", "pack_size_qty","stock", "weight", "weight_units", "asset_account_id", "is_master"]
allProducts = []

def extractData(data):
    global allOrders

    products = data["products"]   #orders is a list of every order

    for product in products: # order is a dict
        variants = product["variants"]
        # print(variants)
        for variant in variants:
            sku = variant["sku"].strip(" ")
            ID = variant["id"]
            fully_qualified_name = variant["fully_qualified_name"]
            active = variant["active"]
            cost_price = variant["cost_price"]
            incremental_order_quantity = variant["incremental_order_quantity"]
            pack_size = variant["pack_size"]
            pack_size_qty = variant["pack_size_qty"]
            weight = variant["weight"]
            weight_units = variant["weight_units"]
            stock = variant["stock_items"]
            asset_account_id = variant["asset_account_id"]
            is_master = variant["is_master"]
            
            # make a list of all these values
            values = [sku, ID, cost_price, fully_qualified_name, active, incremental_order_quantity,
                      pack_size, pack_size_qty, stock, weight, weight_units, asset_account_id, is_master]
            allProducts.append(values)


def jprint(obj):
    ''' 
    Converts retrieved json files into legible print format 
    
    '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum):
    ''' Returns the products that == inventory_item '''
    payload = {'token': API_KEY, 'page':pageNum, 'q[product_type_eq]': "inventory_item"}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def main():
    global allOrders
    
    data = apiCall(1)
    totalPages = data['meta']['total_pages']
    
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum)
        extractData(data)

    # create pandas dataframe
    df = pd.DataFrame(allProducts, columns = columns)

    # only keep products that are active
    df = df[df["active"] == True]

    # out of all inventory items, only ones w/ asset_account_id == 1017 are ingredients
    df = df[df["asset_account_id"] == 1017]

    # write to csv
    df.to_csv (r'ingredients.csv', index = False, header=True)
    

if __name__ == '__main__':
    main()

