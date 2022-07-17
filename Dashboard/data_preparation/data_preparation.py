# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:29:52 2022

@author: BRSch
"""


# =============================================================================
# Imports
# =============================================================================

import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os
import regex as re
import json
import numpy as np

# =============================================================================
# Living Planet Index
#
# The living planet index data is retreived from two datasets, one for Dutch data,
# one for European data. These two datasets are merged into one. For this, two 
# major transformations were required:
#    - European data used reference year 1970, has been transformed to match
#      the reference year used in Dutch data (1990). CI's are removed.
#    - Dutch data was on a scale of 0 to 100, has been set to scale of 0 to 1,
#      matching European data.
# =============================================================================
lpi_data= pd.read_csv("data/IPBES Europe-Central Asia.csv")

# Removed the "IPBES" part of geographical region
lpi_data["Title"]= [f"{title.split()[1]} {title.split()[2]}" 
                    for title in lpi_data["Title"]]

# Selected for data from 1990 onwards
lpi_data= lpi_data.query('Year>= 1990')

# Scaled data to use reference year 1990 and set that value to 1
lpi_data["LPI_final"]= [value/lpi_data["LPI_final"].iloc[0]
                        for value in lpi_data["LPI_final"]]

# Removed confidence intervals
lpi_data["CI_low"]= [np.nan]*len(lpi_data)
lpi_data["CI_high"]= [np.nan]*len(lpi_data)

lpi_data_NLD= pd.read_excel("data/c-1569-001g-clo-07-nl.xlsx").drop("Waarneming", axis= 1)

# Added geographical region column
lpi_data_NLD["Title"]= ["Netherlands"]*len(lpi_data_NLD)

# Reordered columns and renamed them to same as European data
lpi_data_NLD= lpi_data_NLD.iloc[:, [1,2,3,4,0]]
lpi_data_NLD.columns= lpi_data.columns

# Set values to scale 0 to 1
for column in ["LPI_final", "CI_low", "CI_high"]:
    lpi_data_NLD[column]= [value/100 for value in lpi_data_NLD[column]]

# Merged datasets
lpi_data_EU= pd.concat([lpi_data, lpi_data_NLD], axis= 0)

# Write to csv in app data folder
lpi_data_EU.to_csv(f"{os.pardir}/data/lpi_data_EU.csv", index= False)
# =============================================================================
# IUCN redlist data
#
#   - The relevant columns were identified as 14, 17 and 21 (country, greater 
#     geographical region), and 33 through 62 (RLI values).
#   - The selection of relevant columns was transformed into long format.
#   - Data was filtered to only include countries in Europe.
#   - Mean values of the greater geographical regions were added.
# =============================================================================
rli_data= pd.read_csv("data/Indicator_15.5.1%3A_Red_List_Index.csv")

# Filtering for European data
europe= ["Eastern Europe", "Southern Europe", "Western Europe", "Northern Europe"]
rli_data= rli_data.query(f'parentName in {europe}')

# Selecting relevant columns
relevant_columns= [14,17]+ list(range(33,62))
rli_data= rli_data.iloc[:, relevant_columns]

# Transform dataset from wide to long format
rli_data= pd.melt(rli_data, id_vars= ["geoAreaName", "parentName", "ISO3"], 
                  var_name= "year", value_name= "RLI")

# Remove leading "year_" part of year string and change string entry of year into integer
rli_data["year"]= [int(entry.split("_")[1])
                   for entry in rli_data["year"]]

# Create European dataset with mean RLI values across the greater geographical regions
rli_data_EU= rli_data.groupby(by= ["parentName", "year"]).mean().reset_index(drop= False)

# Drop parentName column
rli_data.drop(["parentName"], axis= 1, inplace= True)

# Merge main dataset with European mean values
rli_data_EU= pd.concat([rli_data, rli_data_EU.rename(columns= {"parentName": "geoAreaName"})])

# Write to csv in app data folder
rli_data_EU.to_csv(f"{os.pardir}/data/rli_data_EU.csv", index= False)
# =============================================================================
# Dutch Nitrogen (and Phosphate) emission- and loss data
# =============================================================================
emission_data= pd.read_csv('data/83983NED_UntypedDataSet_24022022_122525.csv', 
                           sep= ';', index_col= "ID")

# Rename column
emission_data.rename(columns= {"Perioden": "Jaar"}, inplace= True)


# Strip trailing whitespaces
emission_data["RegioS"]= [region.strip()
                          for region in emission_data["RegioS"]]

# Remove trailing "JJ00" part of year string and change string entry of year into integer
emission_data["Jaar"]= [re.sub('(\d{4})\w*', "\\1" , period)
                        for period in emission_data["Jaar"]]
emission_data["Jaar"]= emission_data.Jaar.astype(int)     

# Add column with percentage losses values.
emission_data["PercentageStikstofverliezen"]= [round(losses/total * 100,2) if total> 0
                                               else 0
                                               for total, losses in zip(emission_data["TotaalStikstofuitscheiding_5"],
                                                                        emission_data["TotaalStikstofverliezenN_6"])]

region_meta= pd.read_table("data/83983NED_metadata_regio.txt", sep= " ", header= None)

# Create dataset with English terms for region
region_meta.columns= ["RegioS", "NatuurlijkeTerm_NL"]
region_meta["NatuurlijkeTerm_ENG"]= ["Netherlands", "North-Netherlands",
                                     "East-Netherlands", "West-Netherlands",
                                     "South-Netherlands", "Groningen",
                                     "Friesland", "Drenthe", 
                                     "Overijssel", "Flevoland",
                                     "Gelderland", "Utrecht",
                                     "Noord-Holland", "Zuid-Holland",
                                     "Zeeland", "Noord-Brabant",
                                     "Limburg", "Concentration region-East",
                                     "Concentration region-South", "Non concentration region"]

# Change region code to english term
emission_data["RegioS"]= [region_meta.query(f'RegioS== "{code}"')["NatuurlijkeTerm_NL"].item()
                          for code in emission_data["RegioS"]]

# Create dataset with English terms for business type
business_meta= pd.read_table("data/83983NED_metadata_bedrijfstypen.txt", sep= ";", header= None)
business_meta.columns= ["Bedrijfstype", "NatuurlijkeTerm_NL"]
business_meta["NatuurlijkeTerm_ENG"]= ["Total all business types", 
                                       "Total grazing animal businesses",
                                       "Dairy businesses", 
                                       "Meat calve businesses",
                                       "Other cattle businesses", 
                                       "Goat- and other grazer businesses",
                                       "Total cage animal businesses", 
                                       "Pig businesses", 
                                       "Poultry businesses", 
                                       "Other cage animal businesses",
                                       "Total other agricultural businesses", 
                                       "Total livestock combinations",
                                       "Crop/livestock combinations", 
                                       "Agriculture, horticulture and crop combinations"]

# =============================================================================
# Dutch percentage contribution to nitrogen emission data
# =============================================================================
CBS_NHx= pd.read_csv("data/CBS_NHx.csv")

# Strip trailing whitespaces
CBS_NHx.columns= [column.strip()
                  for column in CBS_NHx.columns]

# Replace "," with "." as decimal point and make percentage float
CBS_NHx["Percentage"]= [float(value.replace(",", "."))
                        for value in CBS_NHx["Percentage"]]

# Change source names to English
CBS_NHx["Source"]= ["Agriculture", "Private housholds",
                    "Services, waste and water", "Road traffic",
                    "Industry", "Energy sector",
                    "Other sources", "Shipping",
                    "Railway traffic", "Air traffic"]

CBS_NOx= pd.read_csv("data/CBS_NOx.csv")

# Strip trailing whitespaces
CBS_NOx.columns= [column.strip()
                  for column in CBS_NOx.columns]


# Replace "," with "." as decimal point and make percentage float
CBS_NOx["Percentage"]= [float(value.replace(",", "."))
                        for value in CBS_NOx["Percentage"]]

# Change source names to English
CBS_NOx["Source"]= ["Road traffic", "Other sources",  
                    "Shipping", "Industry", 
                    "Energy sector", "Agriculture", 
                    "Air traffic"]

# Write to csv in app data folder
business_meta.to_csv(f"{os.pardir}/data/83983NED_metadata_bedrijfstypen.csv", index= False)

region_meta.to_csv(f"{os.pardir}/data/83983NED_metadata_regio.csv", index= False)

emission_data.to_csv(f"{os.pardir}/data/emission_data_NL.csv", index= False)

CBS_NHx.to_csv(f"{os.pardir}/data/CBS_NHx.csv", index= False)

CBS_NOx.to_csv(f"{os.pardir}/data/CBS_NOx.csv", index= False)
# =============================================================================
# GeoJSON data
# =============================================================================
with open("data/netherlands.json") as json_file:
    netherlands_geojson= json.load(json_file)

# Change province name in local language to Dutch name
netherlands_geojson["features"][2]["properties"]["name"]= "Friesland"

try:
    with open(f"{os.pardir}/data/netherlands.json", "x") as new_file:
        new_file.write(json.dumps(netherlands_geojson))
except Exception as err:
    print(err)


