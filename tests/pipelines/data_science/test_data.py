import json

import pandas as pd
import pytest
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.report import Report
from evidently.tests import *
from sklearn.model_selection import train_test_split


@pytest.fixture
def dummy_data():
    return pd.read_csv("data/05_model_input/preprocessed_dataset_id_106.csv")


@pytest.fixture
def dummy_parameters():
    parameters = {
        "model_options": {
            "test_size": 0.2,
            "random_state": 3,
            "features": ["X_1", "X_2", "X_3"],
        }
    }
    return parameters


def test_split_data(dummy_data, dummy_parameters):
    X = dummy_data[dummy_parameters["model_options"]["features"]]
    y = dummy_data["y"]
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=dummy_parameters["model_options"]["test_size"],
        random_state=dummy_parameters["model_options"]["random_state"],
    )
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )
    report.run(reference_data=X_train, current_data=X_test)
    report_json = json.loads(report.json())

    assert not (
        report_json["metrics"][1]["result"]["drift_by_columns"]["X_1"]["drift_detected"]
    )
    assert not (
        report_json["metrics"][1]["result"]["drift_by_columns"]["X_2"]["drift_detected"]
    )
    assert not (
        report_json["metrics"][1]["result"]["drift_by_columns"]["X_3"]["drift_detected"]
    )
