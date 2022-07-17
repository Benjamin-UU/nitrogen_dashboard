# -*- coding: utf-8 -*-

import pandas as pd
import json
# =============================================================================
# Emission data
# =============================================================================
emission_data= pd.read_csv("data/emission_data_NL.csv")

# Creates a list of all province names (excluding the other geographical regions 
# from the emission dataset)
province_list= ['Groningen',
                'Friesland', 'Drenthe',
                'Overijssel', 'Flevoland',
                'Gelderland', 'Utrecht',
                'Noord-Holland', 'Zuid-Holland',
                'Zeeland', 'Noord-Brabant',
                'Limburg']

# Creates a dictionary of the emission data for easier access in functions
regional_emission_data= {}
for region in set(emission_data["RegioS"]):
    regional_emission_data[region]= emission_data.query(f'RegioS== "{region}"')

CBS_NHx= pd.read_csv("data/CBS_NHx.csv")
CBS_NOx= pd.read_csv("data/CBS_NOx.csv")
# =============================================================================
# Emission meta data
# These dictionaries are only very sparsely used, but can, in the future, be
# used for showing content in both Dutch and English
# =============================================================================
business_meta= pd.read_csv('data/83983NED_metadata_bedrijfstypen.csv')
code2business_ENG= {}
code2business_NL= {}
for code in business_meta["Bedrijfstype"]:
    code2business_NL[code]= business_meta.query(f'Bedrijfstype== "{code}"')["NatuurlijkeTerm_NL"].item()
    code2business_ENG[code]= business_meta.query(f'Bedrijfstype== "{code}"')["NatuurlijkeTerm_ENG"].item()

region_meta= pd.read_csv('data/83983NED_metadata_regio.csv')
code2region_ENG= {}
code2region_NL= {}
for code in region_meta["RegioS"]:
    code2region_NL[code]= region_meta.query(f'RegioS== "{code}"')["NatuurlijkeTerm_NL"].item()
    code2region_ENG[code]= region_meta.query(f'RegioS== "{code}"')["NatuurlijkeTerm_ENG"].item()

variable_data= pd.read_csv('data/83983NED_metadata_variabelen.csv', sep= ';')
colname2NL= {}
colname2ENG= {}
for colname in variable_data["KolomNaam"]:
    colname2NL[colname]= variable_data.query(f'KolomNaam== "{colname}"')["NatuurlijkeTerm_NE"].item()
    colname2ENG[colname]= variable_data.query(f'KolomNaam== "{colname}"')["NatuurlijkeTerm_ENG"].item()

# =============================================================================
# Red list index data
# =============================================================================

rli_data_EU= pd.read_csv("data/rli_data_EU.csv")
# Creates a dictionary of the RLI data for easier access in functions
regional_rli_data= {}
for country in set(rli_data_EU["geoAreaName"]):
    regional_rli_data[country]= rli_data_EU.query(f'geoAreaName== "{country}"').reset_index(drop= True)

# =============================================================================
# Living planet index data
# =============================================================================

lpi_data_EU= pd.read_csv("data/lpi_data_EU.csv")
# Creates a dictionary of the LPI data for easier access in functions
regional_lpi_data= {}
for region in set(lpi_data_EU["Title"]):
    regional_lpi_data[region]= lpi_data_EU.query(f'Title== "{region}"').reset_index(drop= True)

# =============================================================================
# GeoJSON data
# =============================================================================
with open("data/netherlands.json") as json_file:
    netherlands_geojson= json.load(json_file)
