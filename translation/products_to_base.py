import pandas as pd 

temp = pd.read_csv('products_to_base.csv')  
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
            bp = bp.to_list()
            
            #accumulate all base products needed and amt 
            for product in bp:
                tmp = product.split(" () ")
                tmp2 = tmp[0]
                tmp3 = tmp2.strip("[,],(,)")
                tmp4 = tmp3.split(',')

                sku = tmp4[0].strip("''")
                num = int(tmp4[1].strip('""'))

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