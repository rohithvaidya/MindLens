import json
import os
import matplotlib.pyplot as plt
import shap
import pandas as pd
from mapie.classification import MapieClassifier

def xplain_model_prediction(sklearn_model, user_df, userid):
    """
    Explains a model's prediction for a specific user using SHAP values.

    This function computes the SHAP values for a given user's data, identifying the top features 
    that contributed to the predicted label and the features that detracted from it.

    Args:
        sklearn_model: A trained scikit-learn model (compatible with SHAP's TreeExplainer).
        user_df (pd.DataFrame): DataFrame containing user data with columns:
            - 'id': Unique identifier for each user.
            - 'Name', 'City', 'Depression': Columns to exclude during prediction explanation.
        userid: The unique identifier of the user whose prediction is to be explained.

    Returns:
        Tuple:
            - features_to_predicted_label (pd.DataFrame): A DataFrame containing the top 5 features 
              contributing most to the predicted label. Includes columns:
                - 'name': Feature name.
                - 'value': Feature value.
                - 'contribution': SHAP value (positive contribution to the prediction).
            - features_away_predicted_label (pd.DataFrame): A DataFrame containing the top 2 features 
              detracting most from the predicted label. Includes the same columns as above.

    Workflow:
        1. Extracts the input data for the specified `userid` by filtering `user_df` on the 'id' column.
           If no matching `userid` is found, it defaults to the last entry in the DataFrame.
        2. Drops non-predictive columns ('id', 'Name', 'City', 'Depression').
        3. Initializes a SHAP TreeExplainer with the trained model and computes SHAP values.
        4. Creates a DataFrame (`waterfall_df`) containing feature names, their values, and SHAP contributions.
        5. Identifies:
            - Top 5 features contributing positively to the prediction.
            - Top 2 features detracting negatively from the prediction.

    Notes:
        - Ensure the `sklearn_model` is compatible with SHAP's TreeExplainer.
        - The input `user_df` must include the required columns.
        - Returns empty DataFrames if no meaningful SHAP values are calculated.

    Example:
        Given a user's data and model:
        ```python
        features_to_label, features_away_label = xplain_model_prediction(
            sklearn_model, user_df, userid="12345"
        )
        print(features_to_label)
        print(features_away_label)
        ```

    Raises:
        - ValueError: If the required columns are missing from `user_df`.
    """
    
    x_pred = user_df.loc[user_df['id']==userid].drop(columns=["id", "Name", "City", "Depression"])

    if(x_pred.empty):
        x_pred = user_df.iloc[[-1]].drop(columns=["id", "Name", "City", "Depression"])
   
    explainer = shap.TreeExplainer(sklearn_model)
    print(x_pred)
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

def prediction_confidence(user_df, userid, model_selection_name, conformal_logistic_regression, conformal_random_forest, conformal_xg_boost, conformal_decision_tree):
    model = model_selection_name["model"]
    if model == "logistic_regression":
        regressor = conformal_logistic_regression
    elif model == "decision_tree":
        regressor = conformal_decision_tree
    elif model == "random_forest":
        regressor = conformal_random_forest
    elif model == "xg_boost":
        regressor = conformal_xg_boost

    x_pred = user_df.loc[user_df['id']==userid].drop(columns=["id", "Name", "City", "Depression"])

    if(x_pred.empty):
        x_pred = user_df.iloc[[-1]].drop(columns=["id", "Name", "City", "Depression"])

    y_pred_conf, y_conf_interval = regressor.predict(x_pred, alpha=0.1) #90% confidence

    print((json.dumps({"y_pred_conf_interval":str(y_conf_interval)})))

    return json.dumps({"y_pred_conf_interval":str(y_conf_interval)})