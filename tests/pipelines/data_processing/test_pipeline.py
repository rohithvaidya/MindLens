import json

import pandas as pd
import pytest
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.report import Report
from evidently.tests import *
from sklearn.model_selection import train_test_split



# Data Quality Checks

@pytest.fixture
def dummy_data():
    return pd.read_csv("data/01_raw/dataset_id_T01_V3_106.csv")


def test_missing_values(dummy_data):
    var = False
    for i in dummy_data.isna().keys():
        for j in dummy_data.isna()[i]:
            if(j):
                var = True
    assert not (var)