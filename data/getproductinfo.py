import requests
import json
import pandas as pd
import time

'''
    - generates product_info.csv, which contains inventory items (all the items BSR is
        purchasing from vendors)
'''

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/products.json'

columns = ["sku", "cost_price", "fully_qualified_name", "active", "incremental_order_quantity", "pack_size", "pack_size_qty", "weight", "weight_units"]
#columns = ["sku", "cost_price", "pack_size"] 
allProducts = []

def extractData(data):
    global allOrders
    products = data["products"]   #orders is a list of every order

    for product in products:        # order is a dict
        variants = product["variants"]
        for variant in variants:
            sku = variant["sku"].strip(" ")
            cost_price = variant["cost_price"]
            # extras
            fully_qualified_name = variant["fully_qualified_name"]
            active = variant["active"]
            incremental_order_quantity = variant["incremental_order_quantity"]
            pack_size = variant["pack_size"]
            pack_size_qty = variant["pack_size_qty"]
            weight = variant["weight"]
            weight_units = variant["weight_units"]
            # make a list of all these values
            values = [sku, cost_price, fully_qualified_name, active, incremental_order_quantity, pack_size, pack_size_qty, weight, weight_units]
            allProducts.append(dict(zip(columns, values)))

def jprint(obj):
    ''' 
    Converts retrieved json files into legible print format 
    
    '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum):
    ''' Returns the products that == inventory_item (rather than inventory_assembly) '''
    #'q[name_eq]': "INGREDIENTS"
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
    df = pd.DataFrame(allProducts)

    # write to csv
    df.to_csv (r'product_info.csv', index = False, header=True)
    

if __name__ == '__main__':
    main()

