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


df_13oz.to_csv('products_to_base.csv', index = False)

