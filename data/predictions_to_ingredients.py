import requests
import json
import pandas as pd
from csv import writer
import pathlib
import numpy as np

'''
        Main file that will take Niko's predictions, and break them down into batches
        & ingredients using products' components
'''

def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def apiCall(productID, pageNum=1):
    ''' Returns the product with specified ID '''
    URL = 'https://app.getsweet.com/api/v1/variants/' + productID
    payload = {'token': API_KEY, 'page':pageNum}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data

def read_in_proj_sales():
    ''' Reads in the projected sales file '''
    # read in csv of id_to_sku to create a dataframe
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("two_week_proj_withSKU.csv"), low_memory=False)
    # convert sku's & id's to strings & projected sales to floats
    df['sku'] = df['sku'].astype(str)
    df['id'] = df['id'].astype(str) #to_numeric
    df['proj_sales'] = pd.to_numeric(df['proj_sales'])
    return df

def main():
    # read in Niko's projected sales (csv of product ID's and amount predicted to sell)
    #-------- do what the file retrievedata.py does (which outputs two_week_proj_withSKU.csv)
    
    # take the new csv of projections that includes SKU's and make a df
    # -------- in the meantime, just read in two_week_proj_withSKU.csv
    df = read_in_proj_sales()

    # break down each product in df['sku'] into it's ingredients, mu




