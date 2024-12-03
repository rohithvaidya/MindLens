import json
import os

import matplotlib.pyplot as plt
import shap
from evidently.metrics import *
from evidently.tests import *


def compare_trained_models(sklearn_model):
    # We will load the previous model and compare metrics, if the current metrics are not good, we will raise error
    # Open and read the JSON file

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
        raise Exception("Model Accuracy has gone down compared to the previous version")


def aggregate_shap_explanations(X_train, sklearn_model):
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
