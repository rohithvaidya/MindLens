import json
import logging
from typing import Dict, Tuple

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from evidently.metric_preset import DataDriftPreset
from evidently.metrics import *
from evidently.report import Report
from evidently.tests import *
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
import shap


def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data["y"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_model(X_train: pd.DataFrame, y_train: pd.Series) -> LogisticRegression:
    """Trains the Logistic regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for target decision.

    Returns:
        Trained model.
    """
    print(X_train)
    regressor = LogisticRegression(penalty="l2", C=0.01)
    regressor.fit(X_train, y_train)
    sklearn_model = regressor

    return regressor, sklearn_model


def quality_drift_check(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
):
    """
    Checks for data drift between training and test datasets using predefined metrics.

    This function runs a data drift analysis between the provided training (`X_train`)
    and test (`X_test`) datasets. It generates a drift report using the `Report` class
    with the `DataDriftPreset` metrics and returns the report in JSON format.

    Parameters
    ----------
    X_train : pd.DataFrame
        The reference dataset (usually the training dataset) to check for data drift.
    X_test : pd.DataFrame
        The current dataset (usually the test dataset) to compare against the reference dataset.

    Returns
    -------
    dict
        A dictionary containing the drift report results in JSON format.
    """

    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )
    report.run(reference_data=X_train, current_data=X_test)
    report.save_html("data/08_reporting/data_drift.html")
    data_drift_str = str(report.json)
    
    return json.loads(report.json())


def evaluate_model(
    regressor: LogisticRegression, X_test: pd.DataFrame, y_test: pd.Series
) -> pd.Series:
    """Calculates and logs the coefficient of determination.

    Args:
        regressor: Trained model.
        X_test: Testing data of independent features.
        y_test: Testing data for target decision.
    """
    y_pred = regressor.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Model has accuracy of %.3f on test data.", score)
    logger.info("Model has precision of %.3f on test data.", precision)
    logger.info("Model has recall of %.3f on test data.", recall)

    metrics = {"score":score, "precision":precision, "recall":recall}

    return y_pred, metrics


def prediction_drift_check(y_test: pd.Series, y_pred: pd.Series):
    """
    Checks for prediction drift between the true and predicted values.

    This function runs a data drift analysis between the provided true values (`y_test`)
    and predicted values (`y_pred`). It generates a drift report using the `Report` class
    with the `DataDriftPreset` metrics, saves the report as an HTML file, and returns the
    drift report in JSON format.

    Parameters
    ----------
    y_test : pd.Series
        The reference true values (ground truth) to check for prediction drift.
    y_pred : pd.Series
        The predicted values to compare against the reference true values.

    Returns
    -------
    dict
        A dictionary containing the drift report results in JSON format.

    Side Effects
    ------------
    An HTML file named 'evidently_plot.html' is saved to 'data/08_reporting/' containing the visual report.
    """
    report = Report(
        metrics=[
            DataDriftPreset(),
        ]
    )

    report.run(
        reference_data=y_test,
        current_data=pd.DataFrame(y_pred, columns=["y"]),
    )

    if json.loads(report.json())["metrics"][1]["result"]["drift_by_columns"]["y"][
        "drift_detected"
    ]:
        raise Exception("Prediction Variable Drift Detected. Pipeline Failure")
    else:
        report.save_html("data/08_reporting/evidently_plot.html")
        return json.loads(report.json())


def plot_and_save(column_name, current_data, reference_data):
    """
    Plots and saves the probability density distribution for a specified column.

    This function compares the probability density distribution between the current and
    reference datasets for a specified column. It creates a line plot for both datasets and saves
    the plot as a PNG file to a predefined location.

    Parameters
    ----------
    column_name : str
        The name of the column for which the distribution plot is generated.
    current_data : pd.DataFrame
        The current dataset containing columns 'x' (values) and 'y' (probability densities).
    reference_data : pd.DataFrame
        The reference dataset containing columns 'x' (values) and 'y' (probability densities).

    Returns
    -------
    None
        This function does not return any value, but saves the generated plot as a PNG file.

    Side Effects
    ------------
    A PNG file named after the column is saved to 'data/08_reporting/' containing the
    distribution plot for the specified column.
    """
    current_x = current_data["x"]
    current_y = current_data["y"]

    reference_x = reference_data["x"]
    reference_y = reference_data["y"]

    # Create the plot
    fig = go.Figure()

    # Add trace for current data
    fig.add_trace(
        go.Scatter(
            x=current_x, y=current_y, mode="lines+markers", name="Current Distribution"
        )
    )

    # Add trace for reference data
    fig.add_trace(
        go.Scatter(
            x=reference_x,
            y=reference_y,
            mode="lines+markers",
            name="Reference Distribution",
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Distributions for {column_name}",
        xaxis_title="X values",
        yaxis_title="Probability Density",
        legend=dict(x=0.02, y=0.98),
        template="plotly_dark",
    )

    # Show the plot
    pio.write_image(
        fig,
        file="data/08_reporting/{}_distribution.png".format(
            column_name.replace("/", "_")
        ),
    )


def report_plotly(data_drift, pred_drift):
    """
    Generates and saves distribution plots for data and prediction drift using Plotly.

    This function processes the drift reports from the data drift and prediction drift analyses,
    extracts the small distribution data for each column, and generates distribution plots using
    the `plot_and_save` function. It handles both data drift and prediction drift reports, saving
    the resulting plots as PNG files.

    Parameters
    ----------
    data_drift : dict
        A dictionary containing the data drift report, including metrics and drift results
        by columns.
    pred_drift : dict
        A dictionary containing the prediction drift report, including metrics and drift results
        by columns.

    Returns
    -------
    None
        This function does not return any value, but saves the generated distribution plots
        as PNG files for each column.

    Side Effects
    ------------
    PNG files are saved to 'data/08_reporting/' for each column's distribution plot based
    on the drift reports.
    """
    data_drift_by_columns = data_drift["metrics"][1]["result"]["drift_by_columns"]
    pred_drift_by_columns = pred_drift["metrics"][1]["result"]["drift_by_columns"]
    for column, data in data_drift_by_columns.items():
        current_distribution = data["current"]["small_distribution"]
        reference_distribution = data["reference"]["small_distribution"]
        plot_and_save(column, current_distribution, reference_distribution)
    for column, data in pred_drift_by_columns.items():
        current_distribution = data["current"]["small_distribution"]
        reference_distribution = data["reference"]["small_distribution"]
        plot_and_save(column, current_distribution, reference_distribution)
