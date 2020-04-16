import pandas as pd 
import ast

temp = pd.read_csv('base-map.csv')  
products = pd.DataFrame(temp)

class Order:
    """
    Class attributes:
    order: the order itself, represented as a dict of sku's and amts
    length: length of order, how many products did they order?
    base: dictionary corresponding to order: keys = base products (sku) the order requires, 
                                             values = num of each base product
    """

    # Constructor method.
    def __init__(self, dictionary):
        self.order = dictionary
        self.skus = dictionary.keys()
        self.amts = dictionary.values()
        # self.length = len(lst_skus)
        self.level_one = None

    def get_level_one(self):
        '''
        get_base: this method gets the base products for the order

        '''
        base = {}
        for sku in self.skus: # for product in order get base products
            bp = products.loc[products['sku'] == sku]["Level One"]
            bp = bp.reset_index().drop(columns = ["index"])
            
            if bp.empty == True:
                print("unknown sku")
                print(sku)
                
            else:
                bp = bp.lookup(row_labels =[0], col_labels=["Level One"])

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

        self.level_one = base
        return
    
 