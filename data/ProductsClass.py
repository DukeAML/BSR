import requests
import json
import pandas as pd
import time

'''
    Centralized attempt at getting products & inventory bc there's like 5 million files
    trying to do the same thing

    to do: filter out samples, scrap, transiton jars, batches, marketing (MKT)
'''

# GLOBAL VARIABLES
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/products.json'

columns = ["sku", "price", "fully_qualified_name", "active", "for_sale", "product_type", "incremental_order_quantity", "pack_size", "pack_size_qty", "weight", "weight_units"]
allProducts = []
"""
class Products:
    '''
    Class attributes:
    order: the order itself, represented as a dict of sku's and amts
    length: length of order, how many products did they order?
    base: dictionary corresponding to order: keys = base products (sku) the order requires, 
                                             values = num of each base product
    '''

    # Constructor method.
    def __init__(self, dfColumns):
        self.dfCols = dfColumns
"""
    
def extractData(data):
    global allProducts
    products = data["products"]   #orders is a list of every order
    
    for product in products:
        for_sale = product["for_sale"]
        product_type = product["product_type"]
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
            values = [sku, cost_price, fully_qualified_name, active, for_sale, product_type, incremental_order_quantity, pack_size, pack_size_qty, weight, weight_units]
            allProducts.append(values)


def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum):
    #payload = {'token': API_KEY, 'page':pageNum, 'q[product_type_eq]': "inventory_item"}
    #payload = {'token': API_KEY, 'page':pageNum, 'q[product_type_eq]': "inventory_assembly"}
    payload = {'token': API_KEY, 'page':pageNum, 'q[active_true]': "1"}
    
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def main():
    global allOrders
    
    data = apiCall(1)
    totalPages = data['meta']['total_pages']
    print(totalPages)
    
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum)
        extractData(data)

    # create pandas dataframe
    df = pd.DataFrame(allProducts, columns = columns)

    # only keep products that are active
    df = df[df["active"] == True]

    # only keep products that are for sale
    df = df[df["for_sale"] == True]
    
    # only keep products that are inventory_item or inventory_assembly (not non_inventory_item or service)
    product_types = ["inventory_item", "inventory_assembly"]
    df = df[df.product_type.isin(product_types)]

    # sort values by product type
    df.sort_values(by=['product_type'], inplace=True)

    # make csv
    df.to_csv (r'top_level_products.csv', index = False, header=True)
    print(len(df.index))    #tells you how many orders there are
    

if __name__ == '__main__':
    main()





