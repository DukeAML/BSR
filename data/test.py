
import pandas as pd 

base = pd.read_csv('base.csv')  
base = pd.DataFrame(base)

pbase = pd.read_csv('products_to_base.csv')  
pbase = pd.DataFrame(pbase)

skus = base["sku"]
skus = [item[1] for item in skus.items()]
skus = [item.strip(" '' ") for item in skus]

for sku in skus:
    one = base.loc[base['sku'] == sku]["Level Down"]
    one = one.reset_index().drop(columns = ["index"])
    one = one.lookup(row_labels =[0], col_labels=["Level Down"])
    one = one[0]
    one = one.strip(" '' ")


    two = pbase.loc[pbase['sku'] == sku]["Level Down"]
    two = two.reset_index().drop(columns = ["index"])
    
    try:
        two = two.lookup(row_labels =[0], col_labels=["Level Down"])
        two = two[0]
        two = two.strip(" '' ")
    except:
        print("bad")
        print(sku)
        print(two)

    

    if one != two:
        print(sku)
        print(one)
        print(two)