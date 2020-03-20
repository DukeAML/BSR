import requests
import json
import pandas as pd

'''
    "due_date": "2019-05-06"    -- date BSR is paid
    "payment_total": "270"
    "item_total": "270"           -- doesn't include shipping
    "line_items": [
                {
                    "id": 508247,
                    "name": "WHOLESALE-INACTIVE",
                    "price": 54.0,
                    "quantity": 5.0,
                    "variant_id": 15544,
                    "weight_in_ounces": 192.0
                }
            ]
'''

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
payload = {'token': API_KEY}
URL = 'https://app.getsweet.com/api/v1/orders.json'

r = requests.get(url=URL, headers=headers, params=payload)
data = r.json()

columns = ["Due Date", "Invoice Date", "Order #", "Company Name", "Company ID", "Money Paid", "Items"]


def extractData():
    data



def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(data)


























