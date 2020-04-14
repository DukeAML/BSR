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

def read_in_IDtoSKU(option=1, csvname="id_to_sku.csv"):
    ''' Reads in the ID to SKU dictionary
        Parameters:     option : 1 {id:sku} or 2 {sku:id} '''
    # read in csv of id_to_sku to create a dataframe
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath(csvname), low_memory=False)

    # convert everything to strings & turn into list
    df = df.astype(str)
    IDs = df['id'].tolist()
    SKUs = df['sku'].tolist()

    # zip together the 2 lists & turn it into a dictionary
    if option == 1:
        return dict(zip(IDs, SKUs))
    else:
        return dict(zip(SKUs, IDs))

def readInNikoPredictions():
    # read in the id to sku dictionary
    id_to_sku = read_in_IDtoSKU()

    # read in Niko's csv of predictions to create a dataframe
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("../two-week-predictions.csv"), low_memory=False)

    # rename Niko's ID's column, convert to strings, & turn to list of id's
    df = df.rename(columns = {'Unnamed: 0' : 'id'})
    df['id'] = df['id'].astype(str)
    prediction_ids = df['id'].tolist()

    # go through each prediction id & match up it's sku & predicted amount
    prediction_skus = []
    invalid = []
    for ID in prediction_ids:
        if ID in id_to_sku:
            sku = id_to_sku[ID]
            prediction_skus.append(sku)
        else: # if ID is not in the dictionary, make an API call to variants to get the sku instead
            invalid.append(ID)
            data = apiCall(ID)
            if 'variant' in data:
                sku = data['variant']["sku"]
                prediction_skus.append(sku)
                # write it to the csv containing ID -> sku dictionary
                append_list_as_row('id_to_sku.csv', [ID, sku])
    print(invalid)

    # make new dataframe with sku, id, & projected sales for next 2 weeks
    data = {'sku':prediction_skus, 'id':prediction_ids, 'proj_sales':df['yhat'].tolist()}
    df = pd.DataFrame(data)
    df.sort_values(by=['sku'], inplace=True)
    df.to_csv (r'two_week_proj_withSKU.csv', index = False, header=True)


if __name__=="__main__":
    readInNikoPredictions()



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


















