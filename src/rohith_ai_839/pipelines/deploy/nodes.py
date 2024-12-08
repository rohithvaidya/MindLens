import matplotlib.pyplot as plt
import os
from evidently.metrics import *
from evidently.tests import *
import mlflow
import json


def get_run_id(sklearn_model):
    runs = mlflow.search_runs()
    current_run = runs["run_id"][0]
    return {"run_id":str(current_run)}
    
def serve_model(current_run_id):
    #Use in windows only
    os.system("""start /B mlflow models serve -m "runs:/{}/model" -p 8001 --no-conda > mlflow_log.txt 2>&1""".format(current_run_id["run_id"]))
    print("Serve instance running")
