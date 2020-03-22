import requests
import json
import pandas as pd
import time


API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/products.json'

#columns = ["Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]
allOrders = []

def extractData(data):
    global allOrders
    products = data["products"]   #orders is a list of every order
    
    for product in products:        # order is a dict
        active = product["active"]
        if(active == "false"):
            .
        
        due_date = order["due_date"]
        invoice_date = order["invoice_date"]
        order_num = order["number"]
        company_name = order["account"]["fully_qualified_name"]
        company_id = order["account"]["id"]
        payment_total = order["payment_total"]
        items = []
        for item in order["line_items"]:
            items.append([item["id"], item["variant_id"], item["quantity"]])
        # zip together the columns with the values
        values = [due_date, invoice_date, order_num, company_name, company_id, payment_total, items]
        allOrders.append(dict(zip(columns, values)))


def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def apiCall(pageNum):
    #'q[name_eq]': "INGREDIENTS"
    # 17669
    payload = {'token': API_KEY, 'page':pageNum, 'q[name_eq]': "INGREDIENTS"}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


def main():
    global allOrders
    
    data = apiCall(1)
    totalPages = data['meta']['total_pages']

    totalPages = 1
    
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum)

        #jprint(data)
        extractData(data)

    # create pandas dataframe
    df = pd.DataFrame(allOrders)
    #df.to_csv (r'income_data1.csv', index = False, header=True)
    print(len(df.index))    #tells you how many orders there are
    

if __name__ == '__main__':
    main()

