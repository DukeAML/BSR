import pandas as pd 

#create 13 oz base products df
base13 = pd.read_csv('13oz_base.csv')  
base_13 = pd.DataFrame(base13)

#create 13 oz products df
pr13 = pd.read_csv('13oz_products.csv')  
pr_13 = pd.DataFrame(pr13)

helper = {}
for sku in pr_13['sku']:
    
    lst = sku.split("-")
    nb = lst[1]

    if '1PACK' in lst:
        if 'GIFT' in lst:
            helper[sku] = [('NB-%s-13OZ' %nb, 1)] #extras for gift ? 
        else:
            helper[sku] = [('NB-%s-13OZ'%nb, 1)]
    
    elif '2PACK' in lst and 'GIFT' in lst:
        if len(lst) == 5:
            helper[sku] = [('NB-%s-13OZ' %nb, 2)] #extras for gift ?
        elif len(lst) == 6:
            nb2 = lst[2]
            helper[sku] = [('NB-%s-13OZ' %nb, 1),('NB-%s-13OZ' %nb2, 1)] #extras for gift ?
        else:
            print('found unknown sku: %s' %sku)

    elif '2PACK' in lst and 'GIFT' not in lst:
        if len(lst) == 4:
            helper[sku] = [('NB-%s-13OZ' %nb, 2)] 
        elif len(lst) == 5:
            nb2 = lst[2]
            helper[sku] = [('NB-%s-13OZ' %nb, 1),('NB-%s-13OZ' %nb2, 1)] 
        else:
            print('found unknown sku: %s' %sku)
    elif 'SAMPLE' in lst:
        helper[sku] = [('NB-%s-13OZ' %nb, 1)] 
    
    elif 'CASE' in lst:
        helper[sku] = [('NB-%s-13OZ' %nb, 12)] 
    
    elif 'SUBSCR' in lst:
        helper[sku] = [('NB-%s-13OZ' %nb, 1)]  #is this right way of doing subscriptions?
    
    elif 'TRIO' in lst:
        if 'FW19' in lst:
            helper[sku] = [('NB-ALM-13OZ', 1), ('NB-CHAI-13OZ',1), ('NB-MPC-13OZ',1)]
        elif 'SS20' in lst:
            helper[sku] = [('NB-CASH-13OZ', 1), ('NB-PNUT-13OZ',1), ('NB-TCO-13OZ',1)]
        else:
            print('found unknown sku: %s' %sku)
    else:
        print('found unknown sku: %s' %sku)

df_13oz = pd.DataFrame()
df_13oz['sku'] = helper.keys()
df_13oz['Level Down'] = helper.values()
print(df_13oz)
df_13oz.to_csv('products_to_base.csv', index = False)

#create nb recipes df
nbr = pd.read_csv('nb_recipes.csv')  
nb_recipes = pd.DataFrame(nbr)
nb_recipes = nb_recipes.drop([26,27,28,29,30,39,40]).drop(columns = ['Ingredient', 'Unit'])
index = ['Kosher Sea Salt (lb)', 'Organic Honey (lb)', 'Organic Coconut Oil (lb)', 'RPS- Conventional roasted split peanuts (lb)', 'Pecans - Large Pieces (lb)', 'Dry Roasted Mission Type Almonds (lb)', 'Organic Cashew Kernels LWP (lb)', 'Chai Spice Mix - No Sugar (lb)', 'TCHO Chocolate - 81% Drops (lb)',  'Lemon Powder (lb)','Cocoa Nibs, Bulk (lb)', 'Minor Monuments Espresso (lb)', 'Crystallized Ginger Mini Chips 2-5 mm (lb)', 'Guajillo Chile Powder (lb)', 'Habanero Chile Powder (lb)',  'Ancho Chile Powder, Bulk (lb)', 'Unsweetened Coconut Chips (lb)',  'Coconut Crystals (lb)', 'Sugar, Raw Demerara (lb)', 'Vanilla Powder, Bulk (lb)', 'Hazelnut Kernels (lb)', 'Vietnamese Cinnamon, Ground (lb)', 'Organic Maple Powder (lb)', 'Organic Maple Granules (lb)', 'TCHO Chocolate - 81% Drops (lb)', 'Organic Chia Seeds (lb)', 'Total Weight (lbs)', 'Total Weight (oz)', '13oz', '10oz', '3oz', '1lb', '4lb', '8lb']
nb_recipes.index = index
print(nb_recipes)

#create bar recipes df
br = pd.read_csv('bar_recipes.csv')  
bar_recipes = pd.DataFrame(br)
bar_recipes = bar_recipes.drop(columns = ['Unnamed: 1','Unnamed: 11','NEW #1','Unnamed: 17' ,'Unnamed: 10','Unnamed: 2','Unnamed: 4','Unnamed: 5', 'Unnamed: 18','NEW #2','Unnamed: 16','Unnamed: 13','Unnamed: 19','Unnamed: 8' ,'Unnamed: 20', 'Unnamed: 7','Unnamed: 14'])
bar_recipes = bar_recipes.fillna(0)
