import requests
import json
import pandas as pd
from csv import writer
import pathlib
import numpy as np
import time

'''
    Make a dictionary of {id : sku} key value pairs in file id_to_sku.csv 
'''

# ----- GLOBAL -----
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/variants'
#URL = 'https://app.getsweet.com/api/v1/products'

# ----- HELPER FUNCTIONS -----
def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def apiCall(pageNum=1):
    ''' Returns ALL products '''
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data

def main():
    # make one call to API to find how many total pages there are
    data = apiCall()
    totalPages = data['meta']['total_pages']
    
    pairs = []
    
    # go through every page, where each page contains a list of variants
    for page in range(1, totalPages+1):
        data = apiCall(page)
        
        variants = data['variants']
        pairs += [[variant['id'], variant['sku']] for variant in variants]

    # create pandas dataframe
    df = pd.DataFrame(pairs, columns=['id', 'sku'])

    # drop duplicates & sort the dataframe by the date they bought more ingredients
    df.drop_duplicates(subset='id', keep='first', inplace=True)
    df['id'] = df['id'].astype(int)
    df.sort_values(by=['id'], inplace=True)

    # write to csv
    df.to_csv (r'id_to_sku.csv', index = False, header=True)
    
main()


# implementation using products
'''
    # go through every page, where each page contains a list of variants
    for page in range(1, totalPages+1):
        data = apiCall(page)
        
        products = data['products']
        pairs += [[variant['id'], variant['sku']] for product in products for variant in product['variants']]
        #pairs += [[variant['id'], variant['sku']] for variant in variants]

    # create pandas dataframe
    df = pd.DataFrame(pairs, columns=['id', 'sku'])

    # sort the dataframe by the date they bought more ingredients             
    df['id'] = df['id'].astype(int)
    df.sort_values(by=['id'], inplace=True)

    # write to csv
    df.to_csv (r'id_to_sku1.csv', index = False, header=True)
'''
    
