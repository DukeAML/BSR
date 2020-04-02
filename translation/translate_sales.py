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
            
            #accumulate all base products needed and amt 
            for product in bp:
                print(product)
                name = product[0]
                sku = product[1]
                num = product[2]

                base[sku] = num #add to dict

        print(base)

        self.base = base
        return

order = Order(['NB-ALM-13OZ-1PACK'])
order.get_base()
base = order.base
print(base)

def baseproducts_needed(orders):
    '''
    order --> base products

    '''
        
    needed ={}
    for order in orders:
        A = Order(order)
        A.get_base()
        to_add = A.base

        for sku in to_add.keys():
            if sku in needed:
                needed[sku] += to_add[sku]
            else:
                needed[sku] = to_add[sku]

    return needed

def ingredients_needed(base_products):
    '''
    base products --> ingredients 

    '''

    ingredients_final ={}
    for base_pr in base_products.keys():
        num = base_products[base_pr]
        ingredients = base_products[base_products['sku'] == sku]['level_down'].strip("")

        for ingredient in ingredients:
            name  = ingredient[0] 
            sku = ingredient[1]
            amt = ingredient[2] 
            new_amt = amt*num #need to check units on these ...

            if sku in ingredients_final:
                ingredients_final[sku] += new_amt 

            elif sku not in ingredients_final:
                ingredients_final[sku] = new_amt

    return ingredients_final



