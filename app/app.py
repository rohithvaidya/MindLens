import os
import random
import json
import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import requests

mlflow_url = "http://127.0.0.1:8001/invocations"

app = Flask(__name__)
CORS(
    app, origins=["http://localhost:4869", "http://127.0.0.1:4869", "*"]
)  # Enable CORS for all routes

STATIC_DIR = "static"
USERS_CSV_FILE = "users.csv"
USERS_CSV_PATH = os.path.join(STATIC_DIR, USERS_CSV_FILE)
USERS_COLUMNS = [
    "id",
    "Name",
    "Gender",
    "Age",
    "City",
    "Working Professional or Student",
    "Profession",
    "Academic Pressure",
    "Work Pressure",
    "CGPA",
    "Study Satisfaction",
    "Job Satisfaction",
    "Sleep Duration",
    "Dietary Habits",
    "Degree",
    "Have you ever had suicidal thoughts ?",
    "Work/Study Hours",
    "Financial Stress",
    "Family History of Mental Illness",
    "Depression",
]


@app.route("/login", methods=["POST"])
@cross_origin()
def login():
    # Get the JSON data sent in the request
    print(request)
    data = request.get_json()

    print(data)
    # Extract the ID from the JSON data
    user_name = data.get("name")
    user_id = int(data.get("id"))

    print("user_name: ", user_name)
    print("user_id: ", user_id)

    user_df = pd.read_csv(USERS_CSV_PATH)

    print(user_df[user_df["id"] == user_id]["Name"] == user_name)

    if (user_df[user_df["id"] == user_id]["Name"] == user_name).any():
        print("1st")
        return jsonify(
            {
                "message": "Login Successful",
                "success": True,
                "name": user_name,
                "id": user_id,
            }
        )
    else:
        print("3rd")
        return jsonify({"message": "ID or Name is wrong", "success": False})


# Utility function to generate a random 6-digit ID
def generate_random_id():
    return str(random.randint(100000, 999999))


# API endpoint for user registration
@app.route("/register", methods=["POST"])
@cross_origin()
def register_user():
    # Get the user's name from the request
    data = request.get_json()
    user_name = data.get("name")

    if not user_name:
        return jsonify({"error": "Name is required"}), 400

    user_df = pd.read_csv(USERS_CSV_PATH)

    try:
        while True:
            # Generate a random 6-digit ID
            user_id = generate_random_id()
            if user_id not in user_df["id"]:
                # user_df.append([user_id, name, ])
                new_user = {}
                new_user["id"] = user_id
                new_user["Name"] = user_name

                for col in USERS_COLUMNS[2:]:
                    new_user[col] = pd.NA
                user_df = pd.concat([user_df, pd.DataFrame([new_user])])
                user_df.to_csv(USERS_CSV_PATH, index=False)
                break
    except Exception as e:
        return jsonify({"error": "Failed to save user data", "details": str(e)}), 500

    # Return success response with user ID
    return jsonify(
        {
            "message": "User registered successfully",
            "id": user_id,
            "name": user_name,
            "success": True,
        }
    ), 201


# API endpoint for survey submission
@app.route("/submit-survey", methods=["POST"])
@cross_origin()
def submit_survey():
    # Get the user's name from the request
    data = request.get_json()

    user_df = pd.read_csv(USERS_CSV_PATH)

    location = user_df.loc[user_df["id"] == int(data["id"])].index[0]

    print("location: ", location)

    userid = data["id"]
    username = data["Name"]

    data.pop("id", None)
    data.pop("Name", None)

    for k, v in data.items():
        user_df.at[location, k] = v

    user_df.to_csv(USERS_CSV_PATH, index=False)

    print(data)
    return jsonify({"message": "data_received", "success": True}), 201


@app.route("/right_to_erase")
def right_to_erasure():
    
    data = request.get_json()

    # Removing info from source dataset
    df = pd.read_csv("../data/01_raw/depression_synthetic.csv")
    df = df[
        ~(df['Name'] == data["Name"])
    ]
    df.to_csv("../data/01_raw/depression_synthetic.csv")

    # Running complete training after change in dataset
    os.system("kedro run")

    response = {"message": "Your personal data has been removed and the model has been retrained!"}
    return jsonify(response), 200

@app.route("/update_predictions")
def update_predictions():
    df = pd.read_csv("../data/user_accounts_predictions_log.csv")
    x_pred = df.drop(columns=["id", "Name", "City", "Depression"]).iloc[0].tolist()
    ml_flow_response = requests.post(
        mlflow_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(json.loads(x_pred)),  # Assuming x_pred is JSON string
    )

        # Get the predicted value (assuming it's in the JSON response)
    y_pred = ml_flow_response.json()
    print(y_pred)

if __name__ == "__main__":
    if not os.path.exists(USERS_CSV_PATH):
        with open(USERS_CSV_PATH, mode="w+", newline="", encoding="utf-8") as csvfile:
            csvfile.writelines(",".join(USERS_COLUMNS))

    if os.stat(USERS_CSV_PATH).st_size == 0:
        print("USERS.CSV IS EMPTY")
        with open(USERS_CSV_PATH, mode="w+", newline="", encoding="utf-8") as csvfile:
            csvfile.writelines(",".join(USERS_COLUMNS))
    else:
        print("USERS.CSV IS NOT EMPTY")

    app.run(debug=True)
