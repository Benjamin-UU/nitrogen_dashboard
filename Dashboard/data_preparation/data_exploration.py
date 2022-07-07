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
import numpy as np
import plotly.express as px
import regex as re
import json
# =============================================================================
# Dutch provincial geojson data
# =============================================================================
with open("data/netherlands.json") as json_file:
    netherlands_geojson= json.load(json_file)

# =============================================================================
# IUCN redlist data
# =============================================================================
redlist= pd.read_csv('data/Indicator_15.5.1%3A_Red_List_Index.csv')

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




# =============================================================================
# Global living planet index
# =============================================================================
lp_EU= pd.read_csv('data/IPBES Europe-Central Asia.csv', sep= ",", encoding= 'latin-1')
lp_NL= pd.read_csv('data/clo-lpi-NL.csv', sep= ";")
