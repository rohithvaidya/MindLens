import json
import os
import sqlite3

import pandas as pd
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

# cur.execute("CREATE TABLE preds(x_pred TEXT, y_pred TEXT)")


mlflow_url = "http://127.0.0.1:8001/invocations"


@app.route("/", methods=["POST"])
def hello_world():
    data = request.get_json()

    ml_flow_response = requests.post(
        mlflow_url, headers={"Content-Type": "application/json"}, data=json.dumps(data)
    )

    con = sqlite3.connect("user_predictions.db")
    cur = con.cursor()

    cur.execute(
        "INSERT INTO preds (x_pred, y_pred) VALUES (?, ?)",
        (json.dumps(data), json.dumps(ml_flow_response.json())),
    )

    con.commit()

    # For demonstration, let's just return the data back as a response
    response = {
        "message": "Prediction Done! Your Prediction has been logged in the server",
        "data": ml_flow_response.json(),
    }

    return jsonify(response), 200


@app.route("/erase")
def right_to_erasure():
    # Get parameters from the URL, e.g., /?records=10
    records = request.args.get("records")

    # Removing info from source dataset
    df = pd.read_csv("data/01_raw/dataset_id_T01_V3_106.csv")
    df = df.iloc[int(records) :]
    df.to_csv("data/01_raw/dataset_id_T01_V3_106.csv")

    # Running complete training after change in dataset
    os.system("kedro run")

    response = {"message": "Removed your data and retrained model!"}
    return jsonify(response), 200


@app.route("/update_preds")
def update_predictions():
    # Connect to the SQLite database
    with sqlite3.connect("user_predictions.db") as con:
        cur = con.cursor()

        # Retrieve all x_pred values from the database
        cur.execute("SELECT x_pred FROM preds")
        rows = cur.fetchall()
        # Process each x_pred for predictions
        for row in rows:
            x_pred = row[0]
            # Send x_pred to the MLflow server for predictions
            ml_flow_response = requests.post(
                mlflow_url,
                headers={"Content-Type": "application/json"},
                data=json.dumps(json.loads(x_pred)),  # Assuming x_pred is JSON string
            )

            # Get the predicted value (assuming it's in the JSON response)
            y_pred = ml_flow_response.json()

            print(y_pred)

            # Update the corresponding y_pred in the database
            cur.execute(
                "UPDATE preds SET y_pred = ? WHERE x_pred = ?",
                (json.dumps(y_pred), json.dumps(x_pred)),
            )
        con.commit()

    # Prepare and return the response
    response = {"message": "Predictions updated successfully!"}
    return jsonify(response), 200
