import requests
import json
import pandas as pd

#URL = 'https://app.getsweet.com/api/v1/products/:product_id/variants/:id'
#URL = 'https://app.getsweet.com/api/v1/orders/:order_id/line_items'
# 214153
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
# NB-MPC-13OZ maple cinnamon peanut & pecan butter with sea salt - single jar, order #R26418
#URL = 'https://app.getsweet.com/api/v1/products/850405/variants/161944'
URL = 'https://app.getsweet.com/api/v1/orders/214153/line_items' #R26418
payload = {'token': API_KEY, 'page': 1, 'line_item[variant_id]': '161944', 'line_item[quantity]': '3.0'}
#payload = {'token': API_KEY, 'page': 1}
r = requests.get(URL, headers=headers, params=payload)
data = r.json()

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


#extractData(data)

jprint(data)
