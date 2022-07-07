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
# =============================================================================
lpi_data= pd.read_csv("data/IPBES Europe-Central Asia.csv")

lpi_data["Title"]= [f"{title.split()[1]} {title.split()[2]}" 
                    for title in lpi_data["Title"]]

lpi_data= lpi_data.query('Year>= 1990')

lpi_data["LPI_final"]= [value/lpi_data["LPI_final"].iloc[0]
                        for value in lpi_data["LPI_final"]]


lpi_data["CI_low"]= [np.nan]*len(lpi_data)
lpi_data["CI_high"]= [np.nan]*len(lpi_data)

lpi_data_NLD= pd.read_excel("data/c-1569-001g-clo-07-nl.xlsx").drop("Waarneming", axis= 1)

lpi_data_NLD["Title"]= ["Netherlands"]*len(lpi_data_NLD)

lpi_data_NLD= lpi_data_NLD.iloc[:, [1,2,3,4,0]]
lpi_data_NLD.columns= lpi_data.columns

for column in ["LPI_final", "CI_low", "CI_high"]:
    lpi_data_NLD[column]= [value/100 for value in lpi_data_NLD[column]]
    
lpi_data_EU= pd.concat([lpi_data, lpi_data_NLD], axis= 0)

lpi_data_EU.to_csv(f"{os.pardir}/data/lpi_data_EU.csv", index= False)
# =============================================================================
# IUCN redlist data
# =============================================================================
rli_data= pd.read_csv("data/Indicator_15.5.1%3A_Red_List_Index.csv")

europe= ["Eastern Europe", "Southern Europe", "Western Europe", "Northern Europe"]
rli_data= rli_data.query(f'parentName in {europe}')

relevant_columns= [14,17,21]+ list(range(33,62))

rli_data= rli_data.iloc[:, relevant_columns]
rli_data= pd.melt(rli_data, id_vars= ["geoAreaName", "parentName", "ISO3"], 
                  var_name= "year", value_name= "RLI")

rli_data["year"]= [int(entry.split("_")[1])
                   for entry in rli_data["year"]]

rli_data_EU= rli_data.groupby(by= ["parentName", "year"]).mean().reset_index(drop= False)

rli_data.drop(["parentName", "ISO3"], axis= 1, inplace= True)

rli_data_EU= pd.concat([rli_data, rli_data_EU.rename(columns= {"parentName": "geoAreaName"})])

rli_data_EU.to_csv(f"{os.pardir}/data/rli_data_EU.csv", index= False)
# =============================================================================
# Dutch Nitrogen (and Phosphate) emission- and loss data
# =============================================================================
emission_data= pd.read_csv('data/83983NED_UntypedDataSet_24022022_122525.csv', 
                           sep= ';', index_col= "ID")

emission_data.rename(columns= {"Perioden": "Jaar"}, inplace= True)



emission_data["RegioS"]= [region.strip()
                          for region in emission_data["RegioS"]]
emission_data["Jaar"]= [re.sub('(\d{4})\w*', "\\1" , period)
                        for period in emission_data["Jaar"]]

emission_data["Jaar"]= emission_data.Jaar.astype(int)     

emission_data["PercentageStikstofverliezen"]= [round(losses/total * 100,2) if total> 0
                                               else 0
                                               for total, losses in zip(emission_data["TotaalStikstofuitscheiding_5"],
                                                                        emission_data["TotaalStikstofverliezenN_6"])]

region_meta= pd.read_table("data/83983NED_metadata_regio.txt", sep= " ", header= None)
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



emission_data["RegioS"]= [region_meta.query(f'RegioS== "{code}"')["NatuurlijkeTerm_NL"].item()
                          for code in emission_data["RegioS"]]

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

CBS_NHx= pd.read_csv("data/CBS_NHx.csv")
CBS_NHx.columns= [column.strip()
                  for column in CBS_NHx.columns]

CBS_NHx["Percentage"]= [float(value.replace(",", "."))
                        for value in CBS_NHx["Percentage"]]

CBS_NHx["Source"]= ["Agriculture", "Private housholds",
                    "Services, waste and water", "Road traffic",
                    "Industry", "Energy sector",
                    "Other sources", "Shipping",
                    "Railway traffic", "Air traffic"]

CBS_NOx= pd.read_csv("data/CBS_NOx.csv")
CBS_NOx.columns= [column.strip()
                  for column in CBS_NOx.columns]

CBS_NOx["Percentage"]= [float(value.replace(",", "."))
                        for value in CBS_NOx["Percentage"]]

CBS_NOx["Source"]= ["Road traffic", "Other sources",  
                    "Shipping", "Industry", 
                    "Energy sector", "Agriculture", 
                    "Air traffic"]

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

netherlands_geojson["features"][2]["properties"]["name"]= "Friesland"

try:
    with open(f"{os.pardir}/data/netherlands.json", "x") as new_file:
        new_file.write(json.dumps(netherlands_geojson))
except Exception as err:
    print(err)


