import requests
import json
import pandas as pd
from csv import writer
import pathlib
import numpy as np

#URL = 'https://app.getsweet.com/api/v1/products/:product_id/variants/:id'
#URL = 'https://app.getsweet.com/api/v1/orders/:order_id/line_items'
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
#URL = 'https://app.getsweet.com/api/v1/orders/214153/line_items' #R26418
#productID = '161955'
#URL = 'https://app.getsweet.com/api/v1/variants/' + productID
#payload = {'token': API_KEY, 'page': 1, 'line_item[variant_id]': '161944', 'line_item[quantity]': '3.0'}
#payload = {'token': API_KEY, 'page': 1}
#r = requests.get(URL, headers=headers, params=payload)
#data = r.json()

columns = ["Order Date", "Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]
allOrders = []

def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def extractData(data):
    ''' Parses the info from the API call & adds all orders to the list allOrders.
        Each order is a list of {key:value} pairs where
        key = column name & value = corresponding value '''
    global allOrders
    orders = data["orders"]   #orders is a list of every order

    for order in orders:        # order is a dict
        order_date = order["submitted_at"][:10]     #slice to get rid of time & only leave date
        due_date = order["due_date"]
        invoice_date = order["invoice_date"]
        order_num = order["number"]
        company_name = order["account"]["fully_qualified_name"]
        company_id = order["account"]["id"]
        payment_total = order["payment_total"]
        items = []
        for item in order["line_items"]:
            items.append([item["id"], item["variant_id"], item["price"], item["quantity"]])
        # zip together the columns with the values
        values = [order_date, due_date, invoice_date, order_num, company_name, company_id, payment_total, items]
        allOrders.append(dict(zip(columns, values)))

def apiCall(productID, pageNum=1):
    ''' Returns the product with specified ID '''
    URL = 'https://app.getsweet.com/api/v1/variants/' + productID
    #URL = 'https://app.getsweet.com/api/v1/products.json' 
    #URL = 'https://app.getsweet.com/api/v1/variants.json'
    payload = {'token': API_KEY, 'page':pageNum}
    #payload = {'token': API_KEY, 'page':pageNum, 'q[variants_id_eq]': '161955'}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data

def readInNikoPredictions():
    # read in csv of predictions to create a dataframe
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("../two-week-predictions.csv"), low_memory=False)

    # convert ID's to strings
    df['Unnamed: 0'] = df['Unnamed: 0'].astype(str)
    
    # from the predictions, get a list of all the product id's
    product_ids = df['Unnamed: 0'].tolist()
    #product_ids.append('13718')

    id_to_sku = dict()

    # make API call
    data = apiCall('13718')
    data = apiCall('19140')
    jprint(data)

    
    # go through each id, make an API call to get the product info, & get sku from that
    '''
    for ID in product_ids:
        # make the API call to get data about product with this ID
        data = apiCall(ID)

        print(ID)
        jprint(data)
        sku = str(data['variant']['sku'])
        id_to_sku[ID] = sku
        
    print(id_to_sku)
    '''


#extractData(data)

#jprint(data)

readInNikoPredictions()

























