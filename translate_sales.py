
#build df with all products for sale
to_sell = df

#build df with base products each product implies
#columns = [product_name, sku, level_down = [(base product, sku, num_needed)]]
products = df

#build df with ingredients each base product implies
#columns = [base_prodct_name, sku, level_down = [(ingredient name, sku, amt_needed)]]
base_products = df


#pull orders 
#transform orders ->  to lists of sku's

class Order:
    """
    Class attributes:
    order: the order itself, represented as a list of sku's.
    length: length of order, how many products did they order?
    base: dictionary corresponding to order: keys = base products (sku) the order requires, 
                                             values = num of each base product
    """

    # Constructor method.
    def __init__(self, order):
        self.order = order
        self.length = len(order)
        self.base = None

    def get_base(self):
        '''
        get_base: this method gets the dictionary base 

        '''
        base = {}
        for sku in self.order: # for product in order get base products
            base_products = products[products['sku'] == sku]['level_down'] 
            
            #accumulate all base products needed and amt 
            for product in base_products:
                name = product[0]
                sku = product[1]
                num = product[2]

                base[sku] = num #add to dict

        self.base = Order(self.base)
        return

def baseproducts_needed(orders):
    '''
    order --> base products

    '''
        
    needed ={}
    for order in orders:
        A = Order(order)
        get_base(A)
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
        ingredients = base_products[base_products['sku'] == sku]['level_down'] 

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



