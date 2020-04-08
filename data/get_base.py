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
            helper[sku] = [('NB-%s-13OZ' %nb, 1),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] 
        else:
            helper[sku] = [('NB-%s-13OZ'%nb, 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs %s Label-1PACK" %nb] #nb label below
    
    elif '2PACK' in lst and 'GIFT' in lst:
        if len(lst) == 5:
            helper[sku] = [('NB-%s-13OZ' %nb, 2),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] 
        elif len(lst) == 6:
            nb2 = lst[2]
            helper[sku] = [('NB-%s-13OZ' %nb, 1),('NB-%s-13OZ' %nb2, 1),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] 
        else:
            print('found unknown sku: %s' %sku)

    elif '2PACK' in lst and 'GIFT' not in lst:
        if len(lst) == 4:
            helper[sku] = [('NB-%s-13OZ' %nb, 2),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs %s Label-2PACK" %nb ] #nb label below
        elif len(lst) == 5:
            nb2 = lst[2]
            helper[sku] = [('NB-%s-13OZ' %nb, 1),('NB-%s-13OZ' %nb2, 1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] #how to label this
        else:
            print('found unknown sku: %s' %sku)
    elif 'SAMPLE' in lst:
        helper[sku] = [('NB-%s-13OZ' %nb, 1)] #no other packaging?
    
    elif 'CASE' in lst:
        helper[sku] = [('NB-%s-13OZ' %nb, 12)] #no other packaging? 
    
    elif 'SUBSCR' in lst:
        helper[sku] = [('NB-%s-13OZ' %nb, 1)]  #is this right way of doing subscriptions?
    
    elif '6PACK' in lst:
        if "GH" in lst:
            helper[sku] = [('NB-CHAI-13OZ',1),('NB-CSS-13OZ',1),('NB-FGIN-13OZ',1),('NB-MPC-13OZ',1),('NB-PPEC-13OZ',1),('NB-TCO-13OZ',1)] 
    elif 'WAG' in lst:
        helper[sku] = [('BATCH-WAG',1),('WT161820CF',1),("WT161823CF",1),('S-13166',1),('G12-70-450ECO02-2',1),('C70G-450GGMLP-5',1)] 
        #this skips a level 
    elif 'VP' in lst:
        helper[sku] = [('NB-ALM-13OZ', 1), ('NB-CASH-13OZ',1), ('NB-CHAI-13OZ',1),('NB-CSS-13OZ', 1), ('NB-FGIN-13OZ',1), ('NB-GGET-13OZ',1),('NB-MAMBA-13OZ', 1), ('NB-MPC-13OZ',1), ('NB-PNUT-13OZ',1),('NB-PPEC-13OZ', 1), ('NB-TCO-13OZ',1), ('NB-LTD-CCAKE-10OZ',1)]

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

keys1 =["ALERT Needs ALM Label-1PACK", "ALERT Needs CASH Label-1PACK", "ALERT Needs CHAI Label-1PACK", "ALERT Needs CSS Label-1PACK", "ALERT Needs FGIN Label-1PACK", "ALERT Needs GGET Label-1PACK", "ALERT Needs MAMBA Label-1PACK","ALERT Needs MPC Label-1PACK", "ALERT Needs PNUT Label-1PACK", "ALERT Needs PPEC Label-1PACK", "ALERT Needs TCO Label-1PACK"]
values1 = [("WT158151CF",1), ("CASH 1PACK label missing",1),("WT157272CF",1), ("WT159032CF",1),("WT157276CF",1),("WT159029CF",1),("WT158147CF",1),("WT157274CF",1),("WT157270CF",1),("WT158149CF",1),("WT158153CF",1)]

keys2 = ["ALERT Needs ALM Label-2PACK", "ALERT Needs CASH Label-2PACK", "ALERT Needs CHAI Label-2PACK", "ALERT Needs CSS Label-2PACK", "ALERT Needs FGIN Label-2PACK", "ALERT Needs GGET Label-2PACK", "ALERT Needs MAMBA Label-2PACK","ALERT Needs MPC Label-2PACK", "ALERT Needs PNUT Label-2PACK", "ALERT Needs PPEC Label-2PACK", "ALERT Needs TCO Label-2PACK"]
values2 = [("WT158152CF",1), ("CASH 2PACK label missing",1), ("WT157273CF",1),("WT159033CF",1),("WT157277CF",1),("WT159030CF",1),("WT158148CF",1),("WT157275CF",1),("WT157271CF",1),("WT158150CF",1),("WT158154CF",1)]

labels1 = {}
for ii in range(len(keys1)):
    labels1[keys1[ii]] = values1[ii]

labels2 = {}
for ii in range(len(keys2)):
    labels2[keys2[ii]] = values2[ii]


for ii in range(len(df_13oz["Level Down"])): 
    for jj in range(len(df_13oz["Level Down"].iloc[ii])):
        if "ALERT" in df_13oz["Level Down"].iloc[ii][jj]:
            if "1PACK" in df_13oz["Level Down"].iloc[ii][jj]:
                df_13oz["Level Down"].iloc[ii][jj] = labels1[df_13oz["Level Down"].iloc[ii][jj]]
            elif "2PACK" in df_13oz["Level Down"].iloc[ii][jj]:
                df_13oz["Level Down"].iloc[ii][jj] = labels2[df_13oz["Level Down"].iloc[ii][jj]]


pr3= pd.read_csv('3oz_products.csv')  
pr_3 = pd.DataFrame(pr3)

helper2= {}
for sku in pr_3['sku']:
    
    lst = sku.split("-")
    nb = lst[1]

    if '4PACK' in lst:
        if 'AB' in lst:
            if 'GIFT' in lst:
                helper2[sku] = [('NB-TCO-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-CSS-3OZ', 1),('NB-ALM-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), ("NB-LABEL-GIFT4U",1)] 
            else:
                helper2[sku] = [('NB-TCO-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-CSS-3OZ', 1),('NB-ALM-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs Label-4PACK AB"] 

        else:
            if 'GIFT' in lst:
                helper2[sku] = [('NB-CHAI-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-MPC-3OZ', 1),('NB-PNUT-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), ("NB-LABEL-GIFT4U",1)] 
            else:
                helper2[sku] = [('NB-CHAI-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-MPC-3OZ', 1),('NB-PNUT-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs Label-4PACK"] 

    elif 'CASE' in lst:
        helper2[sku] = [('NB-%s-13OZ' %nb, 12)]

    elif "SAMPLE" in lst:
        helper2[sku] = [('NB-%s-13OZ' %nb, 1)]

df_3oz = pd.DataFrame()
df_3oz['sku'] = helper2.keys()
df_3oz['Level Down'] = helper2.values()

labels3 ={}
labels3["ALERT Needs Label-4PACK AB"] = ("WT157431CF",1)
labels3["ALERT Needs Label-4PACK"] = ("WT157224CF",1)

for ii in range(len(df_3oz["Level Down"])): 
    for jj in range(len(df_3oz["Level Down"].iloc[ii])):
        if "ALERT" in df_3oz["Level Down"].iloc[ii][jj]:
            print(labels3[df_3oz["Level Down"].iloc[ii][jj]])
            df_3oz["Level Down"].iloc[ii][jj] = labels3[df_3oz["Level Down"].iloc[ii][jj]]

df = df_13oz.append(df_3oz, ignore_index=True)

# df.to_csv('products_to_base.csv', index = False)



pr_J= pd.read_csv('jam_products.csv')  
prJ = pd.DataFrame(pr_J,)
print(prJ)
helper3= {}
for sku in prJ['sku']:
    lst = sku.split("-")

    if 'SUBSCR' not in lst:
        month = lst[2]
        name = lst[1]
        name = list(name)
        nb = name[0]
        jam = ("MERCH-JAM-%s" %month)

        if nb == "A":
           
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                if 'GIFT':
                    helper3[sku] = [jam, "unsure ab",("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    helper3[sku] = [jam, "unsure ab"]
            
            elif month == "MAR20":
                if 'GIFT':
                    helper3[sku] = [("MERCH-JAM-MAR20",1),("NB-FGIN-13OZ",1)]
                else:
                    helper3[sku] = [("MERCH-JAM-MAR20",1),("NB-FGIN-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]

            elif month == "APR20":
                if 'GIFT':
                    helper3[sku] = [("MERCH-JAM-APRIL20",1),("NB-TCO-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    [("MERCH-JAM-APRIL20",1),("NB-TCO-13OZ",1)]
                    
        
        elif nb == "P":
    
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                if 'GIFT':
                    helper3[sku] = [jam, "unsure pb",("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    helper3[sku] = [jam, "unsure pb"]
            
            elif month == "MAR20":
                if 'GIFT':
                    helper3[sku] = [("MERCH-JAM-MAR20",1),("NB-PNUT-13OZ",1)]
                else:
                    helper3[sku] = [("MERCH-JAM-MAR20",1),("NB-PNUT-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]

            elif month == "APR20":
                if 'GIFT':
                    helper3[sku] = [("MERCH-JAM-APRIL20",1),("NB-PPEC-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    [("MERCH-JAM-APRIL20",1),("NB-PPEC-13OZ",1)]
        
    elif 'SUBSCR' in lst:
        month = lst[3]
        name = lst[1]
        name = list(name)
        nb = name[0]
        jam = ("MERCH-JAM-%s" %month)

        if nb == "A":
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                helper3[sku] = [jam, "unsure ab"]
            elif month == "MAR20":
                helper3[sku] = [jam, ("NB-FGIN-13OZ",1)]

            elif month == "APR20":
                helper3[sku] = [jam, ("NB-TCO-13OZ",1)]

        elif nb == "P":
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                helper3[sku] = [jam, "unsure pb"]
            elif month == "MAR20":
                helper3[sku] = [jam, ("NB-PNUT-13OZ",1)]
            elif month == "APR20":
                helper3[sku] = [jam, ("NB-PPEC-13OZ",1)]
           

        elif nb == "R":
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                helper3[sku] = ["unsure nb"]
            elif month == "MAR20":
                helper3[sku] = [("NB-PNUT-13OZ",1)]
            elif month == "APR20":
                helper3[sku] = [("NB-LTD-CCAKE-10OZ",1)]

dfJoz = pd.DataFrame()
dfJoz['sku'] = helper3.keys()
dfJoz['Level Down'] = helper3.values()

df = dfJoz.append(df, ignore_index=True)

print(df)

#10 oz
# subscriptions
# bars
# merch 



           