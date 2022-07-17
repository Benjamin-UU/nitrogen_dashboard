# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:29:52 2022

@author: BRSch
"""


# =============================================================================
# 
# =============================================================================

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

# =============================================================================
# IUCN redlist data
# =============================================================================
redlist= pd.read_csv("data/Indicator_15.5.1%3A_Red_List_Index.csv")

print(redlist.dtypes)
description= redlist.describe()
for column in description:
    print(description[column],"\n")

print(f"Number of different countries: {len(set(redlist.geoAreaName))}")
print(f"Number of different greater geographical regions: {len(set(redlist.parentName))}")

redlist.columns[33]
redlist.iloc[:, 33]
redlist.columns[61]
# =============================================================================
# Dutch Nitrogen (and Phosphate) emission- and loss data
# =============================================================================
emission_data= pd.read_csv('data/83983NED_UntypedDataSet_24022022_122525.csv', sep= ';')

print(emission_data.dtypes)
description= emission_data.describe()
for column in description:
    print(description[column],"\n")
print(f"Dutch fertilizer emission data:\n{emission_data.info()}")

print(F"Number of different business types: {len(set(emission_data.Bedrijfstype))}")
print(F"Number of different regions: {len(set(emission_data.RegioS))}")
print(F"Number of datapoints per business type: {len(emission_data.Bedrijfstype)/len(set(emission_data.Bedrijfstype))/len(set(emission_data.RegioS))}")


emission_contribution_NHx= pd.read_csv("data/CBS_NHx.csv")
emission_contribution_NOx= pd.read_csv("data/CBS_NOx.csv")

# =============================================================================
# Global living planet index
# =============================================================================
lp_EU= pd.read_csv('data/IPBES Europe-Central Asia.csv', sep= ",", encoding= 'latin-1')
lp_NL= pd.read_excel('data/c-1569-001g-clo-07-nl.xlsx')

print(lp_EU.dtypes)
description= lp_EU.describe()
for column in description:
    print(description[column],"\n")
    
print(lp_NL.dtypes)
description= lp_NL.describe()
for column in description:
    print(description[column],"\n")
    
