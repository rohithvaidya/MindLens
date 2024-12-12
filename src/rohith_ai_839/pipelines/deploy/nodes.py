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
    """
    Serves a machine learning model using MLflow in a Windows environment.

    This function starts a background MLflow model serving instance for the specified run ID. 
    The server runs on port 8001 and logs output to a file named `mlflow_log.txt`.

    Args:
        current_run_id (dict): A dictionary containing the `run_id` of the MLflow model to be served.
            Example: {"run_id": "123456789abcdef"}

    Notes:
        - This function is intended for use on Windows systems only.
        - The `mlflow` command-line interface must be installed and accessible in the system's PATH.
        - The server runs without using a conda environment (`--no-conda`).

    Output:
        - Logs from the MLflow server are written to `mlflow_log.txt`.
        - A message "Serve instance running" is printed to indicate successful initiation.
    """
    #Use in windows only
    os.system("""start /B mlflow models serve -m "runs:/{}/model" -p 8001 --no-conda > mlflow_log.txt 2>&1""".format(current_run_id["run_id"]))
    print("Serve instance running")
