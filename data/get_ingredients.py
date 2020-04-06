import pandas as pd

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


