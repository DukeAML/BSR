import requests
import json
import pandas as pd
import time

'''
    Generate a dataframe with ALL products
'''

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/products.json'

columns = ["sku", "cost_price", "fully_qualified_name", "for_sale", "for_purchase",
               "product_type", "active", "incremental_order_quantity", "pack_size",
               "pack_size_qty", "weight", "weight_units"]
allProducts = []

def extractData(data):
    global allOrders
    products = data["products"]   #orders is a list of every order
    
    for product in products:        # order is a dict
        for_sale = product["for_sale"]
        for_purchase = product["for_purchase"]
        product_type = product["product_type"]
        
        variants = product["variants"]
        for variant in variants:
            sku = variant["sku"].strip(" ")
            cost_price = variant["cost_price"]
            # extras
            fully_qualified_name = variant["fully_qualified_name"]
            active = variant["active"]
            # delete incremental, pack_size, & pack_size_qty
            incremental_order_quantity = variant["incremental_order_quantity"]
            pack_size = variant["pack_size"]
            pack_size_qty = variant["pack_size_qty"]
            weight = variant["weight"]
            weight_units = variant["weight_units"]
            # make a list of all these values
            values = [sku, cost_price, fully_qualified_name, for_sale, for_purchase, product_type,
                          active, incremental_order_quantity, pack_size, pack_size_qty, weight, weight_units]
            allProducts.append(values)


def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum):
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def main():
    # make an API call to the first page of results in order to get # of total pages 
    data = apiCall(1)
    totalPages = data['meta']['total_pages']
    print(totalPages)

    # loop thru every page, making a new API call every time
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum)
        extractData(data)

    # create pandas dataframe
    df = pd.DataFrame(allProducts, columns = columns)

    # sort the dataframe by the order date
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Money Paid'] = pd.to_numeric(df['Money Paid'])
    df.sort_values(by=['Order Date', 'Money Paid'], inplace=True, ascending=False)

    # turn dataframe into a csv
    df.to_csv (r'inventory_info.csv', index = False, header=True)
    print(len(df.index))    #tells you how many orders there are
    

if __name__ == '__main__':
    main()

