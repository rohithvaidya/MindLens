import json
import os
import matplotlib.pyplot as plt
import shap
import pandas as pd

def xplain_model_prediction(sklearn_model, user_df, userid):
    
    x_pred = user_df.loc[user_df['id']==userid].drop(columns=["id", "Name", "City", "Depression"])
    
    explainer = shap.TreeExplainer(sklearn_model)
    shap_values = explainer(x_pred)
    
    print("shap_values: ", shap_values)
    
    shap_data = shap_values[0]
    waterfall_data = [
            {
                "name": shap_data.feature_names[i],
                "value": shap_data.data[i].item(),  # Feature value
                "contribution": shap_data.values[i].item()  # SHAP value
            }
            for i in range(len(shap_data.feature_names))
        ]
    waterfall_df = pd.DataFrame(waterfall_data)
    
    features_to_predicted_label = waterfall_df.nlargest(columns='contribution', n=5)
    features_away_predicted_label = waterfall_df.nsmallest(columns='contribution', n=2)
    
    return features_to_predicted_label, features_away_predicted_label