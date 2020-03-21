import requests
import json
import pandas as pd

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/orders.json'

columns = ["Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]
allOrders = []

def extractData(data):
    global allOrders
    orders = data["orders"]   #orders is a list of every order
    
    for order in orders:        # order is a dict
        # get "Company Name" & "Company ID"
        accountInfo = order["account"]
        company_name = accountInfo["fully_qualified_name"]
        company_id = accountInfo["id"]
        # get "Due Date", "Invoice Date", "Order #", & "Money Paid"
        due_date = order["due_date"]
        invoice_date = order["invoice_date"]
        order_num = order["number"]
        payment_total = order["payment_total"]
        # get "Items"
        itemsInfo = order["line_items"]
        items = []
        for item in itemsInfo:
            ID = item["id"]
            variantID = item["variant_id"]
            quantity = item["quantity"]
            items.append({ID : [variantID, quantity]})

        # zip together the columns with the values
        values = [due_date, invoice_date, order_num, company_name, company_id, payment_total, items]
        allOrders.append(dict(zip(columns, values)))


def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def apiCall_orders(pageNum):
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def main():
    global allOrders

    data = apiCall_orders(1)
    meta = data['meta']
    totalPages = meta['total_pages']

    print(totalPages)
    totalPages = 1
    
    for pageNum in range(1, totalPages+1):
        data = apiCall_orders(pageNum)

        #jprint(data)
        extractData(data)

    # create pandas dataframe
    df = pd.DataFrame(allOrders)
    df.to_csv (r'income_data.csv', index = False, header=True)
    print(len(df.index))    #tells you how many orders there are


if __name__ == '__main__':
    main()






