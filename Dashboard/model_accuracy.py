# -*- coding: utf-8 -*-

import pandas as pd

from data_loading import regional_rli_data, regional_lpi_data
from data_loading import regional_emission_data

from emission_modelling import predict_rli, predict_lpi
from emission_modelling import predict_emission

# =============================================================================
# Emission model evaluation
# =============================================================================

emission_results= pd.DataFrame(columns = ["Region", "BusinessType", "LagValue", "MSE", "R2"])
for region in regional_emission_data:
    for business_type in set(regional_emission_data[region]["Bedrijfstype"]):
        prediction= predict_emission(regional_emission_data, region, business_type, "TotaalStikstofuitscheiding_5")
        result= pd.DataFrame({"Region": region, 
                              "BusinessType": business_type, 
                              "LagValue": prediction["Lag"], 
                              "R2": prediction["R2"],
                              "MSE": prediction["MSE"]}, index=[0])
        emission_results= pd.concat([emission_results, result])

print(len(emission_results.query("R2> 0")), len(emission_results.query("R2<= 0")))

emission_results.to_csv("data/evaluation/emission_evaluation   .csv", index= False)


losses_results= pd.DataFrame(columns = ["Region", "BusinessType", "LagValue", "R2"])
for region in regional_emission_data:
    for business_type in set(regional_emission_data[region]["Bedrijfstype"]):
        prediction= predict_emission(regional_emission_data, region, business_type, "PercentageStikstofverliezen")
        result= pd.DataFrame({"Region": region, 
                              "BusinessType": business_type, 
                              "LagValue": prediction["Lag"], 
                              "R2": prediction["R2"]}, index=[0])
        losses_results= pd.concat([losses_results, result])

print(len(losses_results.query("R2> 0")), len(losses_results.query("R2<= 0")))

losses_results.to_csv("data/evaluation/losses_evaluation.csv", index= False)

# =============================================================================
# LPI model evaluation
# =============================================================================

lpi_results= pd.DataFrame(columns = ["Region", "LagValue", "R2"])
for region in regional_lpi_data:
    prediction= predict_lpi(regional_lpi_data, region)
    result= pd.DataFrame({"Region": region, 
                          "LagValue": prediction["Lag"], 
                          "R2": prediction["R2"],
                          "MSE": prediction["MSE"]}, index=[0])
    lpi_results= pd.concat([lpi_results, result])

print(len(lpi_results.query("R2> 0")), len(lpi_results.query("R2<= 0")))

lpi_results.to_csv("data/evaluation/lpi_evaluation.csv", index= False)

# =============================================================================
# RLI model evaluation
# =============================================================================

rli_results= pd.DataFrame(columns = ["Region", "LagValue", "R2"])
for region in regional_rli_data:
    prediction= predict_rli(regional_rli_data, region)
    result= pd.DataFrame({"Region": region, 
                          "LagValue": prediction["Lag"], 
                          "R2": prediction["R2"],
                          "MSE": prediction["MSE"]}, index=[0])
    rli_results= pd.concat([rli_results, result])

print(len(rli_results.query("R2> 0")), len(rli_results.query("R2<= 0")))

rli_results.to_csv("data/evaluation/rli_evaluation.csv", index= False)