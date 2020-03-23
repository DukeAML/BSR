import requests
import json
import pandas as pd
import time
from csv import writer
import pathlib
import numpy as np

def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def main():
    # filter the csv so it contains purchases only ("Big Spoon Roasters Production Facility Quantity" > 0)
    PATH = pathlib.Path(__file__).parent
    df = pd.read_csv(PATH.joinpath("Detail_Inventory_Report_2020-03-22.csv"), low_memory=False)
    
    dfP = df[(df["Big Spoon Roasters Production Facility Quantity"].isna()) | (df["Big Spoon Roasters Production Facility Quantity"] > 0)]
    dfP = dfP.drop(columns=["Transaction Type", "Number", "Customer / Reason", "Customer Type", "Big Spoon Roasters Production Facility QOH", "Quantity Total", "QOH Total"])
    
    # go through every element in date column & get indices of beginning balance
    sku_indices = []
    for i in range(len(dfP.index)):
        if (dfP.iat[i, 0] == "Beginning Balance"):
            sku_indices.append(i-1)
        elif(str(dfP.iat[i, 0]).startswith("Total for")):
            sku_indices.append(i)

    # add a new column
    dfP["sku"] = ""
    dfP["money spent"] = np.nan

    for i in range(0, len(sku_indices), 2):
        skuIndex = sku_indices[i]
        endIndex = sku_indices[i+1]
        # clean up sku number
        sku = str(dfP.iat[skuIndex, 0])
        sku = sku.split(" ")[0]
        for j in range(skuIndex+2, endIndex):
            dfP.iat[j, 2] = sku

    # filter so each row is only date, amount, sku
    dfP = dfP[dfP["sku"] != ""]

    # rename columns
    dfP.columns = ['date', 'amount bought', 'sku', 'money spent']
    dfP.to_csv (r'purchases.csv', index = False, header=True)
    
    dfInfo = pd.read_csv(PATH.joinpath("product_info.csv"), low_memory=False)

    skuNums = dfInfo['sku'].tolist()
    unitPrices = dfInfo['cost_price'].tolist()
    dictionary = dict(zip(skuNums, unitPrices))

    print(dictionary)
    
    for i in range(len(dfP.index)):
        sku = dfP.iat[i, 2]

        #unitPrice = float(dfP.at[str(sku), "cost_price"])
        #newDF = dfInfo.loc[dfInfo['sku'] == sku]
        #print(newDF)
        
        #unitPrice = newDF.iat[0, 1]
        #unitPrice = dictionary[sku]
        unitPrice = dictionary.get(sku, 'not here')
        
        amountBought = float(dfP.iat[i, 1])
        if(unitPrice != 'not here'):
            dfP.iat[i, 3] = amountBought * unitPrice

    dfP.to_csv (r'purchases.csv', index = False, header=True)
    
if __name__ == '__main__':
    main()





