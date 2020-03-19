import requests
import json
import pandas as pd

API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
payload = {'token': API_KEY}
#URL = 'https://app.getsweet.com/api/v1/products.json'
URL = 'https://app.getsweet.com/api/v1/orders.json'

#r = requests.get('https://app.getsweet.com/api/v1/products.json', params=payload)
r = requests.get(url=URL, params=payload)
data = r.json()

def jprint(obj):
    """Converts retrieved json files into legible print format
    """
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(r.json())
