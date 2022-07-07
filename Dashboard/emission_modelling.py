# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 17:12:23 2022

@author: BRSch
"""
import numpy as np
import pandas as pd
from statsmodels.tsa.ar_model import AutoReg
from sklearn.metrics import r2_score

def predict_emission(dictionary, region, businessType, emission):
    full_series= dictionary[region].query(f'Bedrijfstype== "{businessType}"')[emission].reset_index(drop= True)
    split= int(0.8* len(full_series))
    
    train_series= full_series.iloc[:split]
    test_series= full_series.iloc[split:]
    
    R2_best= -np.inf
    
    forecast_steps= 10
    
    try:
    
        # Build a model for each lag value within the range 1:10, evaluate with R-squared
        for lag in range(1, 10):
            model= AutoReg(endog= train_series, lags= lag, old_names= False).fit()
            
            Y_pred= model.predict(start=len(train_series), end=len(full_series)-1)
            
            R2= r2_score(test_series, Y_pred)
            if R2> R2_best:
                # Only save and report back R2 and MAE if next model performs better than previous best
                best_lag= lag
                R2_best= R2
        emission_model= AutoReg(endog= full_series, lags= best_lag, old_names= False).fit()
        
        
        
        predicted_results= pd.DataFrame(
            {"RegioS": [region]*forecast_steps,
             "Jaar": range(dictionary[region]["Jaar"].max()+1, dictionary[region]["Jaar"].max()+forecast_steps+1)}
            ) 
        
        predicted_results["emission_values"]= list(emission_model.forecast(forecast_steps))
        predicted_results["Lower"]= list(emission_model.get_prediction(start= len(full_series), end= len(full_series)+ forecast_steps-1).conf_int()["lower"])
        predicted_results["Upper"]= list(emission_model.get_prediction(start= len(full_series), end= len(full_series)+ forecast_steps-1).conf_int()["upper"])
        predicted_results["Type"]= ["Predicted"]*len(predicted_results)

    except Exception as err:
        predicted_results= pd.DataFrame(
            {"RegioS": [region]*forecast_steps,
             "Jaar": range(dictionary[region]["Jaar"].max()+1, dictionary[region]["Jaar"].max()+forecast_steps+1)}
            ) 
        best_lag= None
        R2_best= None
    
    measured_data= dictionary[region].query(f'Bedrijfstype== "{businessType}"')[["RegioS", "Jaar"]]
    measured_data["emission_values"]= dictionary[region][emission]
    measured_data["Lower"]= [np.nan]*len(measured_data)
    measured_data["Upper"]= [np.nan]*len(measured_data)
    measured_data["Type"]= ["Measured"]*len(measured_data)    
    
    final_results= pd.concat([predicted_results, measured_data]).sort_values(by= "Jaar").reset_index(drop= True)
    
    return {"predicted_results": final_results, "R2": R2_best, "Lag": best_lag}


def predict_rli(dictionary, region):
       
    full_series= dictionary[region]["RLI"]
    split= int(0.8* len(full_series))    
    
    train_series= full_series.iloc[:split]
    test_series= full_series.iloc[split:]
    
    R2_best= -np.inf
    # Build a model for each lag value within the range 1:10, evaluate with R-squared
    for lag in range(1, 10):
        model= AutoReg(endog= train_series, lags= lag, old_names= False).fit()
        
        Y_pred= model.predict(start=len(train_series), end=len(full_series)-1)
        
        R2= r2_score(test_series, Y_pred)
        if R2> R2_best:
            # Only save and report back R2 and MAE if next model performs better than previous best
            best_lag= lag
            R2_best= R2
    emission_model= AutoReg(endog= full_series, lags= best_lag, old_names= False).fit()
    
    forecast_steps= 10
    
    predicted_results= pd.DataFrame(
        {"geoAreaName": [region]*forecast_steps,
         "year": range(dictionary[region]["year"].max()+1, dictionary[region]["year"].max()+forecast_steps+1)}
        )
    
    predicted_results["RLI"]= list(emission_model.forecast(forecast_steps))
    predicted_results["Lower"]= list(emission_model.get_prediction(start= len(full_series), end= len(full_series)+ forecast_steps-1).conf_int()["lower"])
    predicted_results["Upper"]= list(emission_model.get_prediction(start= len(full_series), end= len(full_series)+ forecast_steps-1).conf_int()["upper"])
    predicted_results["Type"]= ["Predicted"]*len(predicted_results)
    
    measured_data= dictionary[region]
    measured_data["Lower"]= [np.nan]*len(measured_data)
    measured_data["Upper"]= [np.nan]*len(measured_data)
    measured_data["Type"]= ["Measured"]*len(measured_data)
    
    final_results= pd.concat([predicted_results, measured_data]).sort_values(by= "year").reset_index(drop= True)
    
    return {"predicted_results":final_results, "R2":R2_best, "Lag": best_lag}






def predict_lpi(dictionary, region):
    full_series= dictionary[region]["LPI_final"]
    split= int(0.8* len(full_series))    
    
    train_series= full_series.iloc[:split]
    test_series= full_series.iloc[split:]
    
    R2_best= -np.inf
    # Build a model for each lag value within the range 1:30, evaluate with R-squared
    for lag in range(1, 10):
        model= AutoReg(endog= train_series, lags= lag, old_names= False).fit()
        
        Y_pred= model.predict(start=len(train_series), end=len(full_series)-1)
        
        R2= r2_score(test_series, Y_pred)
        if R2> R2_best:
            # Only save and report back R2 and MAE if next model performs better than previous best
            best_lag= lag
            R2_best= R2
    emission_model= AutoReg(endog= full_series, lags= best_lag, old_names= False).fit()
    
    forecast_steps= 2026- max(dictionary[region]["Year"])
    
    predicted_results= pd.DataFrame(
        {"Title": [region]*forecast_steps,
         "Year": range(dictionary[region]["Year"].max()+1, dictionary[region]["Year"].max()+forecast_steps+1)}
        )
    
    predicted_results["LPI_final"]= list(emission_model.forecast(forecast_steps))
    predicted_results["CI_low"]= list(emission_model.get_prediction(start= len(full_series), end= len(full_series)+ forecast_steps-1).conf_int()["lower"])
    predicted_results["CI_high"]= list(emission_model.get_prediction(start= len(full_series), end= len(full_series)+ forecast_steps-1).conf_int()["upper"])
    predicted_results["Type"]= ["Predicted"]*len(predicted_results)
    
    measured_data= dictionary[region]
    measured_data["CI_low"], measured_data["CI_high"]= [np.nan]*len(measured_data), [np.nan]*len(measured_data)
    measured_data["Type"]= ["Measured"]*len(measured_data)
    
    final_results= pd.concat([predicted_results, measured_data]).sort_values(by= "Year").reset_index(drop= True)
    
    return {"predicted_results":final_results, "R2":R2_best, "Lag": best_lag}



























