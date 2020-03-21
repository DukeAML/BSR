import requests
import json
import pandas as pd
import time
from csv import writer
import pathlib

'''
    ?page[after]=abcde

    BSR14154
    
'''

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/orders.json'

columns = ["Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]
newOrders = []


def add_new_row(file_name, elements):
    ''' Appends a list that contains a new order to the csv file '''
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        csv_writer.writerow(elements)


def extractData(data):
    global newOrders
    orders = data["orders"]   #orders is a list of every order
    
    for order in orders:        # order is a dict
        due_date = order["due_date"]
        invoice_date = order["invoice_date"]
        order_num = order["number"]
        company_name = order["account"]["fully_qualified_name"]
        company_id = order["account"]["id"]
        payment_total = order["payment_total"]
        items = []
        for item in order["line_items"]:
            items.append([item["id"], item["variant_id"], item["quantity"]])
        # add new row of values to csv
        values = [due_date, invoice_date, order_num, company_name, company_id, payment_total, items]
        #add_new_row('income_data2.csv', values)
        newOrders.append(dict(zip(columns, values)))


def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum, q):
    #{"_changed":{"$gt":{"$date":"2016-08-01"},"$lt":{"$date":"2016-08-05"}}}
    #'id_gt' > shopifyMaxOrderNum ||  companyMaxOrderNum < 'id_gt' < 'R'
    payload = {'token': API_KEY, 'page': pageNum, 'q': q}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def getMaxOrderNums():
    # get most recent order# from csv file (greatest one) & most recent shopify (R+greatest) 20553 & R26203
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("income_data2.csv"), low_memory=False)
    df_noShopify = df[df['Order #'] < 'B']  # also gets rid of order numbers starting with BSR
    
    shopifyMaxOrderNum = df["Order #"].max()
    companyMaxOrderNum = df_noShopify["Order #"].max()
    print(shopifyMaxOrderNum)
    print(companyMaxOrderNum)
    return (shopifyMaxOrderNum, companyMaxOrderNum)


def main():
    (shopifyMaxOrderNum, companyMaxOrderNum) = getMaxOrderNums()

    # query only the orders where order number > max order num (bc max is the last order you read from last update)
    #q = {'$or': [{'number_gt':shopifyMaxOrderNum}, {'number_gt': companyMaxOrderNum, 'number_lt':'R'}]}
    #q = {'number_gt': shopifyMaxOrderNum}
    q = {'number_not_start': "R"}
    data = apiCall(1, q)    #returns JSON of only new orders that you have to put into csv
    totalPages = data['meta']['total_pages']
    jprint(data)
    
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum, q)
        #jprint(data)
        extractData(data) #inserts every order on this page into the csv

    # print the orders
    jprint(newOrders)


if __name__ == '__main__':
    main()







