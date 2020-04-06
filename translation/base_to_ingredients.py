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



