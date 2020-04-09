import pandas as pd 
import ast

temp = pd.read_csv('base.csv')  
products = pd.DataFrame(temp)

class Order:
    """
    Class attributes:
    order: the order itself, represented as a list of sku's.
    length: length of order, how many products did they order?
    base: dictionary corresponding to order: keys = base products (sku) the order requires, 
                                             values = num of each base product
    """

    # Constructor method.
    def __init__(self, lst_skus):
        self.order = lst_skus
        # self.length = len(lst_skus)
        self.base = None

    def get_base(self):
        '''
        get_base: this method gets the base products for the order

        '''
        base = {}
        for sku in self.order: # for product in order get base products
            bp = products.loc[products['sku'] == sku]["Level Down"]
            bp = bp.reset_index().drop(columns = ["index"])
            bp = bp.lookup(row_labels =[0], col_labels=["Level Down"])
            temp = str(bp)
            a = temp.strip(' [] ').strip(' " ')
            b = a.strip('[]')
            c = b.split(",")

            l = len(c) 
            r = l //2  
            n=0

            for ii in range(r):
                t = c[n:(2*ii)+2]
                
                sku = t[0].strip(' () ')
                num = int(t[1].strip(' () '))
                n +=2

                if sku not in base:
                    base[sku] = num #add to dict
                else: 
                    base[sku] += num

        self.base = base
        return

order = Order(['NB-ALM-13OZ-1PACK', 'NB-ALM-13OZ-2PACK', 'NB-CASH-13OZ-1PACK','NB-CHAI-13OZ-2PACK'])
order.get_base()
base = order.base

new_amt = pd.DataFrame()
new_amt["sku"] = base.keys()
new_amt["amt"] = base.values()



temp2 = pd.read_csv('base-products.csv')  
base_products = pd.DataFrame(temp2)

skus = base_products["sku"]
skus = [item[1] for item in skus.items()]
skus = [item.strip(" '' ") for item in skus]

helperA ={}
helperB= {}

for sku in skus: 
    stock = base_products.loc[base_products['sku'] == sku]["stock"]
    stock = stock.reset_index().drop(columns = ["index"])
    stock = stock.lookup(row_labels =[0], col_labels=["stock"])
    stock = stock.tolist()[0]
    stock = stock.strip("[]")
    stock = ast.literal_eval(stock)

    have = float(stock["on_hand"]) #should this be available or on hand?
    committed = float(stock["committed"])

    helperA[sku] = have
    helperB[sku] = committed

df = pd.DataFrame()
df["sku"] = helperA.keys()
df["available"] = helperA.values()
df["prev committed"] = helperB.values()

new_amt = []
for sku in skus:
    if sku in base:
        new_amount = base[sku]
    elif sku not in base:
        new_amount = helperB[sku]
    new_amt.append(new_amount)

df["updated committed"] = new_amt
df["left over"] = df["available"] - df["updated committed"]
df["name"] = base_products["fully_qualified_name"]
df.to_csv('updated_baseinventory.csv', index = False)



