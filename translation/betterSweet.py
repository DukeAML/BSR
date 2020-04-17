from OrderClass import Order
import pandas as pd
import ast

# this function is for taking current sweet data and updating info taking bundles into account 

def data_translation(data):
    '''
    order: csv of current sweet data in format sku - available
    returns df of sku w real available (taking into acct bundles)
    '''
    #current sweet data
    tmp = pd.read_csv(data)  
    data = pd.DataFrame(tmp)
    print(data)

    #get current skus and amounts 
    lst = {}
    for sku in data["sku"]:
        amt = data.loc[data['sku'] == sku]["on_hand"]
        amt = amt.reset_index().drop(columns = ["index"])
        amt = amt.lookup(row_labels =[0], col_labels=["on_hand"])
        amt  = float(amt[0])

        if sku not in lst:
            lst[sku] = amt
        elif sku in lst:
            lst[sku] += amt

    #get base using Order class
    order = Order(lst) #give dict to Order class
    order.get_level_one() #get base (first level down)
    base = order.level_one 

    #put new values for skus in df
    new_amt = pd.DataFrame()
    keys = [key.strip(" '' ") for key in base.keys()]
    new_amt["sku"] = keys
    new_amt["new amt"] = base.values()

    #merge with current data
    df = data.merge(new_amt, how ="outer", on ="sku", sort = False)
    #calc updated amt 
    df["updated avail"] = df["on_hand"] - df["new amt"]
   
    
    print(data.loc[data['sku'] == "NB-ALM-13OZ"])
    print(new_amt.loc[new_amt['sku'] == 'NB-ALM-13OZ'])
    print(df.loc[df['sku'] == "NB-ALM-13OZ"])

    df.to_csv('resultsBetterSweet.csv', index = False)

    return df


#  STATIC EXAMPLE 
temp = pd.read_csv('products.csv')  #later pull this straight from sweet
products = pd.DataFrame(temp)

# TRANSFORM DATA
products = products[["sku", "stock"]]

skus = products["sku"]
skus = [item[1] for item in skus.items()]
skus = [item.strip(" '' ") for item in skus]

on_hand =[]
committed= []
available =[]
for sku in skus: 
    stock = products.loc[products['sku'] == sku]["stock"]
    stock = stock.reset_index().drop(columns = ["index"])
    stock = stock.lookup(row_labels =[0], col_labels=["stock"])
    stock = stock.tolist()[0]
    stock = stock.strip("[]")
    stock = ast.literal_eval(stock)
    have = float(stock["on_hand"]) 
    comm = float(stock["committed"]) 
    avail = float(stock["available"]) 
    on_hand.append(have)
    committed.append(comm)
    available.append(avail)

products["on_hand"] = on_hand
products["committed"] = committed
products["available"] = available

#call function 
df = products[["sku","on_hand","available", "committed"]]
df.to_csv('test_betterSweet.csv', index = False)

print(data_translation('test_betterSweet.csv'))
