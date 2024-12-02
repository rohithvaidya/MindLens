from evidently.metrics import *
from evidently.tests import *
import os
import json

def compare_trained_models(sklearn_model):
    # We will load the previous model and compare metrics, if the current metrics are not good, we will raise error
    # Open and read the JSON file
    
    with open("data/07_model_output/data_drift.json/"+os.listdir("data/07_model_output/data_drift.json")[-2]+"/data_drift.json", 'r') as file:
        old_data_drift = json.load(file)
    with open("data/07_model_output/pred_drift.json/"+os.listdir("data/07_model_output/pred_drift.json")[-2]+"/pred_drift.json", 'r') as file:
        old_pred_drift = json.load(file)
    with open("data/07_model_output/metrics.json/"+os.listdir("data/07_model_output/metrics.json")[-2]+"/metrics.json", 'r') as file:
        old_score = json.load(file)

    with open("data/07_model_output/metrics.json/"+os.listdir("data/07_model_output/metrics.json")[-1]+"/metrics.json", 'r') as file:
        new_score = json.load(file)
    print(new_score, old_score)

    if(new_score["score"] < old_score["score"]):
        raise Exception("Model Accuracy has gone down compared to the previous version")

    return

    
