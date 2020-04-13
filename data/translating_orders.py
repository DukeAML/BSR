import requests
import json
import pandas as pd
from csv import writer
import pathlib
import numpy as np
import ast

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
#productID = '161955'
#URL = 'https://app.getsweet.com/api/v1/variants/' + productID
#payload = {'token': API_KEY, 'page': 1, 'line_item[variant_id]': '161944', 'line_item[quantity]': '3.0'}

columns = ["Order Date", "Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]

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

def append_list_as_row(file_name, list_of_elem):
    ''' Add a new row of data to the csv '''
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)

def apiCall(productID, pageNum=1):
    ''' Returns the product with specified ID '''
    #URL = 'https://app.getsweet.com/api/v1/products' + productID
    #payload = {'token': API_KEY, 'page':pageNum, 'q[variants_id_eq]': '161955'}
    URL = 'https://app.getsweet.com/api/v1/variants/' + productID
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data

def read_in_IDtoSKU(option=1):
    ''' Reads in the ID to SKU dictionary
        Parameters:     option : 1 {id:sku} or 2 {sku:id} '''
    # read in csv of id_to_sku to create a dataframe
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("id_to_sku.csv"), low_memory=False)

    # convert everything to strings & turn into list
    df = df.astype(str)
    IDs = df['id'].tolist()
    SKUs = df['sku'].tolist()

    # zip together the 2 lists & turn it into a dictionary
    if option == 1:
        return dict(zip(IDs, SKUs))
    else:
        return dict(zip(SKUs, IDs))

def readInOrders():
    #jprint(apiCall('171549'))
    # read in the id to sku dictionary
    id_to_sku = read_in_IDtoSKU()
    
    # read in orders csv to create a dataframe
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("income_data.csv"), low_memory=False)

    # rename orders ID's column, convert to strings, & turn to list of id's
    orders_skus = []
    invalid = []
    orders = df['Items'].tolist()
    for order in orders:
        orderList = ast.literal_eval(order)
        orderListSku = []
        for item in orderList:
            ID = str(item[1])
            quantity = item[3]
            if ID in id_to_sku:
                sku = id_to_sku[ID]
                #orderListSku.append(sku)
            else: # if ID is not in the dictionary, make an API call to variants to get the sku instead
                invalid.append(ID)
                data = apiCall(ID)
                if 'variant' in data:
                    sku = data['variant']["sku"]
            orders_skus.append([sku, quantity])

    # make dataframe for orders
    df = pd.DataFrame(orders_skus, columns=['sku', 'qty'])
    # combine duplicate dates so it sums up their 'money spent' column
    df = df.groupby(['sku'], as_index = False).sum()
    df.to_csv (r'orders_withSKU.csv', index = False, header=True)


#extractData(data)

#jprint(data)

readInOrders()



'162123'
'162124'
'162125'
'162126'
'162127'
'162128'
'162129'
'162130'
'162131'
'162132'
'162133'
'162135'
'162136'
'162138'

'163752'

'164232'
'164234'
'164236'
#---------
'162124'
'162127'
'162138'


















