import requests
import json
import pandas as pd
from csv import writer
import pathlib
import numpy as np
import time

'''
    Make a dictionary of {id : sku} key value pairs in file id_to_sku.csv

    Makes one call to the API to get all the products, & one call to get all the variants
'''

# ----- GLOBAL -----
API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}
URL = 'https://app.getsweet.com/api/v1/'


# ----- HELPER FUNCTIONS -----
def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def apiCall(url_end='products', pageNum=1):
    ''' Returns ALL products '''
    payload = {'token': API_KEY, 'page':pageNum, 'q[active_true]':'True'}
    r = requests.get(url=URL+url_end, headers=headers, params=payload)
    data = r.json()
    return data

def generateUsingProducts(pairs):
    # make one call to API to find how many total pages there are
    data = apiCall('products')
    totalPages = data['meta']['total_pages']
    print(data['meta']['total_count'])
    #jprint(data)
    '''
    # go through every page, where each page contains a list of variants
    for page in range(1, totalPages+1):
        data = apiCall('products', page)
        
        products = data['products']
        pairs += [[variant['id'], variant['sku']] for product in products for variant in product['variants']]
    '''
    return pairs


def generateUsingVariants(pairs):
    # make one call to API to find how many total pages there are
    data = apiCall('variants')
    totalPages = data['meta']['total_pages']
    
    # go through every page, where each page contains a list of variants
    for page in range(1, totalPages+1):
        data = apiCall('variants', page)
        
        variants = data['variants']
        pairs += [[variant['id'], variant['sku']] for variant in variants]
    return pairs

def main():    
    pairs = []
    pairs = generateUsingProducts(pairs)
    #pairs = generateUsingVariants(pairs)
    '''
    # create pandas dataframe
    df = pd.DataFrame(pairs, columns=['id', 'sku'])

    # drop duplicates & sort the dataframe by the date they bought more ingredients
    df.drop_duplicates(keep='first', inplace=True)
    df['id'] = df['id'].astype(int)
    df.sort_values(by=['id'], inplace=True)

    # write to csv
    df.to_csv (r'id_to_sku.csv', index = False, header=True)
    #df.to_csv (r'id_to_sku.csv', index = False, header=True)
    '''
main()


    
