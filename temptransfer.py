import pandas as pd
import requests
import json


API_KEY = '44ea3bf2fd0d37eb6d39b576846c69187ffe34fd39177373'
headers = {'Content-Type': 'application/json'}

def jprint(obj):
    ''' Converts retrieved json files into legible print format '''
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def pullProduct(id, pg=1):
    URL = 'https://app.getsweet.com/api/v1/variants/' + str(id)
    payload = {'token': API_KEY, 'page':pg}
    r = requests.get(url=URL, headers=headers, params=payload)
    data = r.json()
    return data


# set up
relprodf = pd.read_csv("data\sold_id_to_sku.csv")
prodinfodf1 = pd.read_csv("data\PRODUCTS-forsale.csv")
prodinfodf2 = pd.read_csv("data\PRODUCTS-not_forsale.csv")


# part 1
halfprod = pd.merge(relprodf, prodinfodf1[["sku", "cost_price", "fully_qualified_name", "active"]], on="sku", how="left")

leftover = halfprod[halfprod['cost_price'].isnull()][["id", "sku"]]


# part 2
halfprod2 = pd.merge(leftover, prodinfodf2[["sku", "cost_price", "fully_qualified_name", "active"]], on="sku", how="left")

leftover2 = halfprod2[halfprod2['cost_price'].isnull()][["id", "sku"]]


# part 3
halfprod3 = pd.DataFrame(columns=halfprod2.columns)
leftover3 = pd.DataFrame(columns=['id', 'sku'])

for index, row in leftover2.iterrows():
    print(row['id'])
    pid = row['id']
    di = pullProduct(pid)


    if 'variant' not in di:
        print("Missing: ", str(pid))
        insert = {'id':pid, 'sku':leftover2.loc[leftover2['id']==pid]['sku'].item()}
        leftover3.append(insert, ignore_index=True)
        continue


    insert = {'id':pid, 'sku':di['variant']['sku'], 'cost_price':di['variant']['cost_price'], 'fully_qualified_name':di['variant']['fully_qualified_name'], 'active':di['variant']['active']}
    print(insert)

    halfprod3 = halfprod3.append(insert, ignore_index=True)

print(halfprod3)

# final
finaldf = halfprod[halfprod['cost_price'].notna()]
finaldf.append(halfprod2[halfprod2['cost_price'].notna()])
finaldf.append(halfprod3[halfprod3['cost_price'].notna()])

finaldf.to_csv(r'products_for_db.csv', index=False, header=True)

