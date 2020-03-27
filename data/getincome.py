import requests
import json
import pandas as pd
import time

# Constants for API call
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/orders.json'

columns = ["Order Date", "Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]
allOrders = []  #list that will contain all orders after extractData is called

def extractData(data):
    ''' Parses the info from the API call & adds all orders to the list allOrders.
        Each order is a list of {key:value} pairs where
        key = column name & value = corresponding value '''
    global allOrders
    orders = data["orders"]   #orders is a list of every order
    
    for order in orders:        # order is a dict
        # get each attribute of an order from the data
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
            
        # zip together the columns with the values & add it to allOrders
        values = [order_date, due_date, invoice_date, order_num, company_name, company_id, payment_total, items]
        #allOrders.append(dict(zip(columns, values)))
        allOrders.append(values)
    


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
    global allOrders
    start_time = time.time()

    # make an API call to the first page of results in order to get # of total pages 
    data = apiCall(1)
    totalPages = data['meta']['total_pages']

    #totalPages = 1

    # loop thru every page, making a new API call every time
    for pageNum in range(1, totalPages+1):
        data = apiCall(pageNum)
        extractData(data)

    # create pandas dataframe
    df = pd.DataFrame(allOrders, columns = columns)
    
    # sort the dataframe by the order date
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Money Paid'] = pd.to_numeric(df['Money Paid'])
    df.sort_values(by=['Order Date', 'Money Paid'], inplace=True, ascending=False)

    # turn dataframe into a csv
    df.to_csv (r'income_data.csv', index=False, header=True)
    
    print(len(df.index))    #tells you how many orders there are
    
    # prints total time the program took to run
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':
    main()


