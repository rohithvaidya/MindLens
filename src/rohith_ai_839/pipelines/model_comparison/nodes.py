import json
import os
import shap
import matplotlib.pyplot as plt
from evidently.metrics import *
from evidently.tests import *


def compare_trained_models(sklearn_model):
    """
    Compares metrics of the current trained model with those of the previous version and raises an error 
    if the performance of the current model is worse.

    This function loads the metrics, data drift, and prediction drift from the last two saved model versions 
    and compares the accuracy (`value_1`) of the current model with the previous one. If the current model's 
    accuracy is lower, an exception can be raised to indicate the regression in performance.

    Args:
        sklearn_model: The current trained scikit-learn model object (not directly used in this implementation).

    Workflow:
        1. Load the latest and previous `data_drift.json`, `pred_drift.json`, and `metrics.json` files 
           from their respective directories.
        2. Compare the "value_1" (accuracy) metric from the `metrics.json` files of the latest and previous models.
        3. Optionally raise an exception if the accuracy of the new model is lower than the previous one.

    Notes:
        - File paths must point to valid JSON files stored in directories under `data/07_model_output/`.
        - The `metrics.json` file should contain a "value_1" key representing model accuracy.
        - This implementation currently passes without raising an exception when accuracy decreases, 
          but the `raise Exception` statement can be uncommented to enforce the check.

    Example JSON Structure:
        metrics.json:
        {
            "value_1": 0.85,
            "value_2": 0.80,
            ...
        }

    Raises:
        Exception: If the current model's accuracy ("value_1") is lower than the previous model's.

    Output:
        - Prints the metrics of the current and previous models for comparison.
    """

    with open(
        "data/07_model_output/data_drift.json/"
        + os.listdir("data/07_model_output/data_drift.json")[-2]
        + "/data_drift.json"
    ) as file:
        old_data_drift = json.load(file)
    with open(
        "data/07_model_output/pred_drift.json/"
        + os.listdir("data/07_model_output/pred_drift.json")[-2]
        + "/pred_drift.json"
    ) as file:
        old_pred_drift = json.load(file)
    with open(
        "data/07_model_output/metrics.json/"
        + os.listdir("data/07_model_output/metrics.json")[-2]
        + "/metrics.json"
    ) as file:
        old_score = json.load(file)

    with open(
        "data/07_model_output/metrics.json/"
        + os.listdir("data/07_model_output/metrics.json")[-1]
        + "/metrics.json"
    ) as file:
        new_score = json.load(file)
    print(new_score, old_score)

    if new_score["value_1"] < old_score["value_1"]:
        pass
        # raise Exception("Model Accuracy has gone down compared to the previous version")


def aggregate_shap_explanations(X_train, sklearn_model):
    """
    Generates SHAP dependency plots for each feature in the training dataset and saves them as PNG images.

    This function uses the SHAP library to calculate SHAP values for a given trained scikit-learn model 
    and the training dataset. For each feature, it creates a scatter plot showing the relationship 
    between feature values and their corresponding SHAP values, and saves the plots in a specified directory.

    Args:
        X_train (pd.DataFrame): The training dataset used for generating SHAP explanations. 
            Each column corresponds to a feature.
        sklearn_model: A trained scikit-learn model for which SHAP values will be computed.

    Workflow:
        1. Initializes a SHAP explainer for the model using the training dataset.
        2. Computes SHAP values for all features in the dataset.
        3. For each feature:
            - Extracts feature values and their corresponding SHAP values.
            - Creates a scatter plot of feature values against SHAP values.
            - Saves the plot as a PNG image in the `data/08_reporting/` directory.

    File Naming Convention:
        - Output plots are saved as `shap_dependency_scatter_<feature_name>.png`.
        - Special characters (e.g., '/') in feature names are replaced or ignored in file names.

    Notes:
        - The directory `data/08_reporting/` must exist prior to calling this function.
        - The function closes each plot after saving to free up memory.

    Dependencies:
        - The `shap` library for computing SHAP values.
        - The `matplotlib` library for generating plots.

    Output:
        - Scatter plots are saved as PNG files in the specified directory.
        - No values are returned.

    Example:
        If `X_train` contains features `age`, `income`, and `education`, the function will create:
        - `shap_dependency_scatter_age.png`
        - `shap_dependency_scatter_income.png`
        - `shap_dependency_scatter_education.png`
    """
    model = sklearn_model
    X = X_train
    explainer = shap.Explainer(model, X)

    # Compute SHAP values
    shap_values = explainer(X)

    for feature_name in X.columns:
        # Get feature values and SHAP values
        feature_values = X[feature_name]
        shap_feature_values = shap_values.values[:, X.columns.get_loc(feature_name)]

        # Create scatter plot
        plt.figure(figsize=(8, 6))
        plt.scatter(
            feature_values,
            shap_feature_values,
            alpha=0.6,
            edgecolors="w",
            linewidth=0.5,
        )
        plt.title(f"SHAP Dependency Plot for {feature_name}")
        plt.xlabel(feature_name)
        plt.ylabel("SHAP Value")

        # Save the plot as a PNG image
        scatter_plot_path = f"data/08_reporting/shap_dependency_scatter_{feature_name.split('/')[0]}.png"
        plt.savefig(scatter_plot_path)
        plt.close()  # Close the plot to free up memory
