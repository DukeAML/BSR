import pandas as pd 

#build df with all products for sale
pi = pd.read_csv('product_info.csv')  
to_sell = pd.DataFrame(pi)

#create nb recipes df
nbr = pd.read_csv('nb_recipes.csv')  
nb_recipes = pd.DataFrame(nbr)
nb_recipes = nb_recipes.drop([0,1,28,29,30,31,32,33,34,43,44]).drop(columns = ['Unnamed: 0', 'Unnamed: 1'])
columns = ['Peanut', 'Peanut Pecan', 'Peanut Almond', 'Cashew Butter', 'Peanut Cocoa', 'Chai Spice', 'Almond Butter', 'Fiji Ginger', 'GGET Espresso', 'Chocolate Sea Salt', 'Mamba', 'Toasted Coconut', 'Just Peanut', 'Just Almond', 'Maple Cinnamon', 'PCASH', 'WAG', 'LCASH', 'CCCG', 'Twalk']
index = ['Kosher Sea Salt (lb)', 'Organic Honey (lb)', 'Organic Coconut Oil (lb)', 'RPS- Conventional roasted split peanuts (lb)', 'Pecans - Large Pieces (lb)', 'Dry Roasted Mission Type Almonds (lb)', 'Organic Cashew Kernels LWP (lb)', 'Chai Spice Mix - No Sugar (lb)', 'TCHO Chocolate - 81% Drops (lb)',  'Lemon Powder (lb)','Cocoa Nibs, Bulk (lb)', 'Minor Monuments Espresso (lb)', 'Crystallized Ginger Mini Chips 2-5 mm (lb)', 'Guajillo Chile Powder (lb)', 'Habanero Chile Powder (lb)',  'Ancho Chile Powder, Bulk (lb)', 'Unsweetened Coconut Chips (lb)',  'Coconut Crystals (lb)', 'Sugar, Raw Demerara (lb)', 'Vanilla Powder, Bulk (lb)', 'Hazelnut Kernels (lb)', 'Vietnamese Cinnamon, Ground (lb)', 'Organic Maple Powder (lb)', 'Organic Maple Granules (lb)', 'TCHO Chocolate - 81% Drops (lb)', 'Organic Chia Seeds (lb)', 'Total Weight (lbs)', 'Total Weight (oz)', '13oz', '10oz', '3oz', '1lb', '4lb', '8lb']
nb_recipes.columns = columns
nb_recipes.index = index


#build df with base products each product implies
#columns = [product_name, sku, level_down = [(base product, sku, num_needed)]]
#products = df

#build df with ingredients each base product implies
#columns = [base_prodct_name, sku, level_down = [(ingredient name, sku, amt_needed)]]
#base_products = df


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



