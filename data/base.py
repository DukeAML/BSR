import pandas as pd 

products = pd.read_csv('products.csv')  
all_products = pd.DataFrame(products)

print(all_products)

helper = {}
for sku in all_products['sku']:
  
    lst = sku.split("-")
    
    if "PANTRY" in lst:
        helper[sku] = [("NB-ALM-13OZ",1),("BAR-AP-SINGLE",1),("PKG-BAR-BOX",1),("NB-CASH-13OZ",1),("BAR-CP-SINGLE",1),("BAR-CC-SINGLE",1),("BAR-FC-SINGLE",1),("LABEL-BAR-BOX-VP",1),("S-13166",1),("NB-PNUT-13OZ",1)]

    #NUT BUTTERS
    elif "NB" in lst: 
        # 13 OZ
        if "13OZ" in lst or "130Z" in lst:
            nb = lst[1]
            #1 PACK GIFT/NO GIFT
            if '1PACK' in lst:
                if 'GIFT' in lst:
                    helper[sku] = [('NB-%s-13OZ' %nb, 1),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] 
                else:
                    helper[sku] = [('NB-%s-13OZ'%nb, 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs %s Label-1PACK" %nb] #nb label below
            # 2 PACK-GIFT
            elif '2PACK' in lst and 'GIFT' in lst:
                if len(lst) == 5:
                    helper[sku] = [('NB-%s-13OZ' %nb, 2),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] 
                elif len(lst) == 6:
                    nb2 = lst[2]
                    helper[sku] = [('NB-%s-13OZ' %nb, 1),('NB-%s-13OZ' %nb2, 1),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] 
                else:
                    print('found unknown sku: %s' %sku)
            # 2 PACK 
            elif '2PACK' in lst and 'GIFT' not in lst:
                if len(lst) == 4:
                    helper[sku] = [('NB-%s-13OZ' %nb, 2),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs %s Label-2PACK" %nb ] #nb label below
                elif len(lst) == 5:
                    nb2 = lst[2]
                    helper[sku] = [('NB-%s-13OZ' %nb, 1),('NB-%s-13OZ' %nb2, 1),("PKG-BOX-2PK-4PK",1),("S-13166",1)] #how to label this
                else:
                    print('found unknown sku: %s' %sku)
            #SAMPLE
            elif 'SAMPLE' in lst:
                helper[sku] = [('NB-%s-13OZ' %nb, 1)] #no other packaging?
            
            #CASE
            elif 'CASE' in lst:
                if "VP" in lst:
                    helper[sku] = [('NB-ALM-13OZ', 1), ('NB-CASH-13OZ',1), ('NB-CHAI-13OZ',1),('NB-CSS-13OZ', 1), ('NB-FGIN-13OZ',1), ('NB-GGET-13OZ',1),('NB-MAMBA-13OZ', 1), ('NB-MPC-13OZ',1), ('NB-PNUT-13OZ',1),('NB-PPEC-13OZ', 1), ('NB-TCO-13OZ',1), ('NB-LTD-CCAKE-10OZ',1)]
                else:
                    helper[sku] = [('NB-%s-13OZ' %nb, 12)] #no other packaging? 
            #WAG
            elif 'WAG' in lst:
                helper[sku] = [('BATCH-WAG',1),('WT161820CF',1),("WT161823CF",1),('S-13166',1),('G12-70-450ECO02-2',1),('C70G-450GGMLP-5',1)] 
                #this skips a level 
            
        #3 0z
        elif "3OZ" in lst or "30Z" in lst:
            lst = sku.split("-")
            nb = lst[1]
            #4 PACK
            if '4PACK' in lst:
                if 'AB' in lst:
                    if 'GIFT' in lst:
                        helper[sku] = [('NB-TCO-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-CSS-3OZ', 1),('NB-ALM-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), ("NB-LABEL-GIFT4U",1)] 
                    else:
                        helper[sku] = [('NB-TCO-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-CSS-3OZ', 1),('NB-ALM-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs Label-4PACK AB"] 

                else:
                    if 'GIFT' in lst:
                        helper[sku] = [('NB-CHAI-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-MPC-3OZ', 1),('NB-PNUT-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), ("NB-LABEL-GIFT4U",1)] 
                    else:
                        helper[sku] = [('NB-CHAI-3OZ', 1),('NB-FGIN-3OZ', 1),('NB-MPC-3OZ', 1),('NB-PNUT-3OZ', 1),("PKG-BOX-2PK-4PK",1),("S-13166",1), "ALERT Needs Label-4PACK"] 
            #CASE
            elif 'CASE' in lst:
                helper[sku] = [('NB-%s-13OZ' %nb, 12)]
            #SAMPLE
            elif "SAMPLE" in lst:
                helper[sku] = [('NB-%s-13OZ' %nb, 1)]
        # 6PACK 
        elif '6PACK' in lst:
                if "GH" in lst:
                    helper[sku] = [('NB-CHAI-13OZ',1),('NB-CSS-13OZ',1),('NB-FGIN-13OZ',1),('NB-MPC-13OZ',1),('NB-PPEC-13OZ',1),('NB-TCO-13OZ',1)] 
        #TRIO
        elif "TRIO" in lst:
            if 'FW19' in lst:
                helper[sku] = [('NB-ALM-13OZ', 1), ('NB-CHAI-13OZ',1), ('NB-MPC-13OZ',1)]
            elif 'SS20' in lst:
                helper[sku] = [('NB-CASH-13OZ', 1), ('NB-PNUT-13OZ',1), ('NB-TCO-13OZ',1)]
            else:
                print('found unknown trio: %s' %sku)
        
        elif "SUBSCR" in lst and len(lst) == 3:
            nb = lst[1]
            helper[sku] = [('NB-%s-13OZ' %nb, 1)] 
        
        elif "SUBSCR" in lst and len(lst) == 4:

            month = lst[3]
            name = lst[1]
            name = list(name)
            nb = name[0]
            jam = ("MERCH-JAM-%s" %month)

            # NB-ABJ-SUBSCR-month
            if nb == "A":
                if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                    helper[sku] = [jam, "unsure ab"]
                elif month == "MAR20":
                    helper[sku] = [jam, ("NB-FGIN-13OZ",1)]

                elif month == "APR20":
                    helper[sku] = [jam, ("NB-TCO-13OZ",1)]
        
            # NB-PBJ-SUBSCR-month
            elif nb == "P":
                if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                    helper[sku] = [jam, "unsure pb"]
                elif month == "MAR20":
                    helper[sku] = [jam, ("NB-PNUT-13OZ",1)]
                elif month == "APR20":
                    helper[sku] = [jam, ("NB-PPEC-13OZ",1)]
            
            # NB-RSTR-SUBSCR-month
            elif nb == "R":
                if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                    helper[sku] = ["unsure nb"]
                elif month == "MAR20":
                    helper[sku] = [("NB-PNUT-13OZ",1)]
                elif month == "APR20":
                    helper[sku] = [("NB-LTD-CCAKE-10OZ",1)]
        
        # NB-ABJ -month
        elif "ABJ" in lst and "SUBCR" not in lst:
            month = lst[2]
            name = lst[1]
            name = list(name)
            nb = name[0]
            jam = ("MERCH-JAM-%s" %month)
    
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                if 'GIFT':
                    helper[sku] = [jam, "unsure ab",("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    helper[sku] = [jam, "unsure ab"]
                
            elif month == "MAR20":
                if 'GIFT':
                    helper[sku] = [("MERCH-JAM-MAR20",1),("NB-FGIN-13OZ",1)]
                else:
                    helper[sku] = [("MERCH-JAM-MAR20",1),("NB-FGIN-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]

            elif month == "APR20":
                if 'GIFT':
                    helper[sku] = [("MERCH-JAM-APRIL20",1),("NB-TCO-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    helper[sku]= [("MERCH-JAM-APRIL20",1),("NB-TCO-13OZ",1)]
        
        # NB-PBJ -month
        elif "PBJ" in lst and "SUBCR" not in lst:
            month = lst[2]
            name = lst[1]
            name = list(name)
            nb = name[0]
            jam = ("MERCH-JAM-%s" %month)
            
            if month == "OCT19" or month == "NOV19" or month == "DEC19" or month == "JAN20" or month == "FEB20":
                if 'GIFT':
                    helper[sku] = [jam, "unsure pb",("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    helper[sku] = [jam, "unsure pb"]
                
            elif month == "MAR20":
                if 'GIFT':
                    helper[sku] = [("MERCH-JAM-MAR20",1),("NB-PNUT-13OZ",1)]
                else:
                    helper[sku] = [("MERCH-JAM-MAR20",1),("NB-PNUT-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]

            elif month == "APR20":
                if 'GIFT':
                    helper[sku] = [("MERCH-JAM-APRIL20",1),("NB-PPEC-13OZ",1),("NB-LABEL-GIFT4U",1), ("S-13166",1),("PKG-BOX-2PK-4PK",1)]
                else:
                    helper[sku] =[("MERCH-JAM-APRIL20",1),("NB-PPEC-13OZ",1)]
        
    #BARS 
    elif "BAR" in lst:
        lst = sku.split("-")
        bar = lst[1]

        if 'SUBSCR' in lst:
            helper[sku] = [("BAR-%s-CASE" %bar,1)]

        elif "SAMPLE" in lst:
            helper[sku] = [("BAR-%s-SINGLE" %bar,1)]
        
        elif "MASTERCASE" in lst:
            helper[sku] = [("BAR-%s-CASE" %bar,1),("15239",1)]
        
        elif "VP" in lst and 'SUBSCR' not in lst:
            if "CASE" in lst:
                helper[sku] = [("BAR-AP-SINGLE",1),("PKG-BAR-BOX",1),("BAR-CP-SINGLE",1),("BAR-CC-SINGLE",1),("BAR-FC-SINGLE",1),("LABEL-BAR-BOX-VP",1)]
            elif "GIFT" in lst:
                helper[sku] = [("BAR-AP-SINGLE",1),("BAR-CP-SINGLE",1),("BAR-CC-SINGLE",1),("BAR-FC-SINGLE",1),("NB-LABEL-GIFT4U",1),("PKG-BOX-2PK-4PK",1)]
        
    else:
        print('found unknown sku: %s' %sku)

df = pd.DataFrame()
df['sku'] = helper.keys()
df['Level Down'] = helper.values()

keys = ["ALERT Needs ALM Label-1PACK", "ALERT Needs CASH Label-1PACK", "ALERT Needs CHAI Label-1PACK", "ALERT Needs CSS Label-1PACK", "ALERT Needs FGIN Label-1PACK", "ALERT Needs GGET Label-1PACK", "ALERT Needs MAMBA Label-1PACK","ALERT Needs MPC Label-1PACK", "ALERT Needs PNUT Label-1PACK", "ALERT Needs PPEC Label-1PACK", "ALERT Needs TCO Label-1PACK", "ALERT Needs ALM Label-2PACK", "ALERT Needs CASH Label-2PACK", "ALERT Needs CHAI Label-2PACK", "ALERT Needs CSS Label-2PACK", "ALERT Needs FGIN Label-2PACK", "ALERT Needs GGET Label-2PACK", "ALERT Needs MAMBA Label-2PACK","ALERT Needs MPC Label-2PACK", "ALERT Needs PNUT Label-2PACK", "ALERT Needs PPEC Label-2PACK", "ALERT Needs TCO Label-2PACK","ALERT Needs Label-4PACK AB","ALERT Needs Label-4PACK"]
values= [("WT158151CF",1), ("CASH 1PACK label missing",1),("WT157272CF",1), ("WT159032CF",1),("WT157276CF",1),("WT159029CF",1),("WT158147CF",1),("WT157274CF",1),("WT157270CF",1),("WT158149CF",1),("WT158153CF",1), ("WT158152CF",1), ("CASH 2PACK label missing",1), ("WT157273CF",1),("WT159033CF",1),("WT157277CF",1),("WT159030CF",1),("WT158148CF",1),("WT157275CF",1),("WT157271CF",1),("WT158150CF",1),("WT158154CF",1),("WT157431CF",1),("WT157224CF",1)]

labels = {}
for ii in range(len(keys)):
    labels[keys[ii]] = values[ii]

for ii in range(len(df["Level Down"])): 
    for jj in range(len(df["Level Down"].iloc[ii])):
        if "ALERT" in df["Level Down"].iloc[ii][jj]:
            if "1PACK" in df["Level Down"].iloc[ii][jj]:
                df["Level Down"].iloc[ii][jj] = labels[df["Level Down"].iloc[ii][jj]]
            elif "2PACK" in df["Level Down"].iloc[ii][jj]:
                df["Level Down"].iloc[ii][jj] = labels[df["Level Down"].iloc[ii][jj]]
            elif "4PACK" in df["Level Down"].iloc[ii][jj]:
                df["Level Down"].iloc[ii][jj] = labels[df["Level Down"].iloc[ii][jj]]


df.to_csv('base-map.csv', index = False)




