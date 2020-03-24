import requests
import json
import pandas as pd
import time
from csv import writer
import pathlib
from datetime import date

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
        add_new_row('income_data2.csv', values)
        newOrders.append(dict(zip(columns, values)))


def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum, startDate):
    #{"_changed":{"$gt":{"$date":"2016-08-01"},"$lt":{"$date":"2016-08-05"}}}
    #'id_gt' > shopifyMaxOrderNum ||  companyMaxOrderNum < 'id_gt' < 'R'
    #currentDate = '2020-03-25'
    #payload = {'token': API_KEY, 'page': pageNum, 'q[invoice_date_gteq]': startDate, 'q[invoice_date_lteq]': endDate}
    #payload = {'token': API_KEY, 'page': pageNum, 'q[number_gt]': shopifyMaxOrderNum}
    payload = {'token': API_KEY, 'page': pageNum, 'q[invoice_date_gteq]': startDate}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def getRecentDate():
    # get most recent order# from csv file (greatest one) & most recent shopify (R+greatest) 20553 & R26203
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("income_data.csv"), low_memory=False)
    mostRecentDate = df["Invoice Date"].max()
    mostRecentDate = '2020-03-18'

    df_noShopify = df[df['Order #'] < 'B']  # also gets rid of order numbers starting with BSR
    shopifyMaxOrderNum = df["Order #"].max()
    companyMaxOrderNum = df_noShopify["Order #"].max()
    return (mostRecentDate, shopifyMaxOrderNum, companyMaxOrderNum)


def main():
    start = time.time()
    #(shopifyMaxOrderNum, companyMaxOrderNum) = getMaxOrderNums()
    #(startDate, shopifyMaxOrderNum, companyMaxOrderNum) = getRecentDate()

    # query only the orders where order number > max order num (bc max is the last order you read from last update)
    #q = {'$or': [{'number_gt':shopifyMaxOrderNum}, {'number_gt': companyMaxOrderNum, 'number_lt':'R'}]}
    #data = apiCall(1, shopifyMaxOrderNum, companyMaxOrderNum)    #returns JSON of only new orders that you have to put into csv
    #mostRecentDate =
    #currentDate = '2020-03-25'
    today = date.today()
    startDate = date(today.year, today.month, today.day-7)
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = today.strftime("%Y-%m-%d")
    
    data = apiCall(1, startDate)
    totalPages = data['meta']['total_pages']

    print(totalPages)
    
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum, startDate)
        #jprint(data)
        extractData(data) #inserts every order on this page into the csv

    # post processing: delete duplicates
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("income_data2.csv"), low_memory=False)
    df.drop_duplicates(subset="Order #", keep='last', inplace=True)

    df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
    df.sort_values(by=['Invoice Date'], inplace=True)

    df.to_csv (r'income_data2.csv', index = False, header=True)

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()







