import pandas as pd 

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
                print(t)
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


implied_base = pd.DataFrame()
implied_base["sku"] = base.keys()
implied_base["amt"] = base.values()
print(implied_base)

for sku in implied_base["sku"]:
    #look up in csv with their current stock -- make this analogous to products.csv
    #get col of how many we have
    #subtract from amt col here make a new col --> amt we have left 

    #final df
    #sku  amt_need  amt_have  amt_left

