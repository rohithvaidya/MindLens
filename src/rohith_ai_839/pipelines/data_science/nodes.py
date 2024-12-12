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
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from mapie.classification import MapieClassifier



def split_data(data: pd.DataFrame, parameters: Dict) -> Tuple:
    """Splits data into features and targets training and test sets.

    Args:
        data: Data containing features and target.
        parameters: Parameters defined in parameters/data_science.yml.
    Returns:
        Split data.
    """
    X = data[parameters["features"]]
    y = data["Depression"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=parameters["test_size"], random_state=parameters["random_state"]
    )
    return X_train, X_test, y_train, y_test


def train_logistic_regression(
    X_train: pd.DataFrame, y_train: pd.Series
) -> LogisticRegression:
    """Trains the Logistic regression model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for target decision.

    Returns:
        Trained model.
    """
    regressor = LogisticRegression(penalty="l2", C=0.01, max_iter=1000)
    mapie = MapieClassifier(regressor, method="score")
    regressor.fit(X_train, y_train)
    mapie.fit(X_train, y_train)

    return regressor, mapie


def train_random_forest(X_train: pd.DataFrame, y_train: pd.Series):
    """Trains the Random Forest model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for target decision.

    Returns:
        Trained model.
    """
    regressor = RandomForestClassifier(random_state=42)
    mapie = MapieClassifier(regressor, method="score")
    regressor.fit(X_train, y_train)
    mapie.fit(X_train, y_train)

    return regressor, mapie


def train_decision_tree(
    X_train: pd.DataFrame, y_train: pd.Series
) -> DecisionTreeClassifier:
    """Trains the Decision Tree model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for target decision.

    Returns:
        Trained model.
    """

    regressor = DecisionTreeClassifier(max_depth=10, random_state=42)
    mapie = MapieClassifier(regressor, method="score")
    regressor.fit(X_train, y_train)
    mapie.fit(X_train, y_train)

    return regressor, mapie


def train_xg_boost(X_train: pd.DataFrame, y_train: pd.Series):
    """Trains the Decision Tree model.

    Args:
        X_train: Training data of independent features.
        y_train: Training data for target decision.

    Returns:
        Trained model.
    """

    regressor = XGBClassifier(random_state=42)
    mapie = MapieClassifier(regressor, method="score")
    regressor.fit(X_train, y_train)
    mapie.fit(X_train, y_train)

    return regressor, mapie



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


def evaluate_all_models(
    regressor_logistic_regression,
    regressor_random_forest,
    regressor_xg_boost,
    regressor_decision_tree,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> pd.Series:
    """
    Evaluates multiple machine learning models on test data and selects the best model based on the F1 score.

    This function calculates the accuracy, precision, recall, and F1 score for each provided model. 
    It logs the performance metrics and determines the best model based on the highest F1 score. 
    Additionally, it returns the predictions, metrics, and the selected model.

    Args:
        regressor_logistic_regression: Trained Logistic Regression model.
        regressor_random_forest: Trained Random Forest model.
        regressor_xg_boost: Trained XGBoost model.
        regressor_decision_tree: Trained Decision Tree model.
        X_test (pd.DataFrame): Test dataset features.
        y_test (pd.Series): Test dataset target labels.

    Returns:
        Tuple:
            - y_pred (np.ndarray): Predictions from the best-performing model.
            - metrics (dict): A dictionary of evaluation metrics for the selected model:
                - "value_1": Accuracy score.
                - "value_2": Precision score.
                - "value_3": Recall score.
                - "value_4": F1 score.
            - regressor: The best-performing model object.
            - regressor: Duplicate reference to the best-performing model object for consistency.

    Logs:
        - The accuracy, precision, recall, and F1 score for each model.
        - The algorithm name of the selected best model.

    Notes:
        - The function assumes all models implement the `predict` method.
        - The `y_test` must be binary for the `precision_score`, `recall_score`, and `f1_score` metrics to work correctly.
    """
    metrics = {}

    y_pred = regressor_logistic_regression.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Logistic Regression Model has accuracy of %.3f on test data.", score)
    logger.info(
        "Logistic Regression Model has precision of %.3f on test data.", precision
    )
    logger.info("Logistic Regression Model has recall of %.3f on test data.", recall)
    logger.info("Logistic Regression Model has f1_Score of %.3f on test data.", f1)
    metrics["logistic_regression"] = [score, precision, recall, f1, y_pred]

    y_pred = regressor_random_forest.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Random Forest Model has accuracy of %.3f on test data.", score)
    logger.info("Random Forest Model has precision of %.3f on test data.", precision)
    logger.info("Random Forest Model has recall of %.3f on test data.", recall)
    logger.info("Random Forest Model has f1_Score of %.3f on test data.", f1)
    metrics["random_forest"] = [score, precision, recall, f1, y_pred]

    y_pred = regressor_xg_boost.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("XG Boost Model has accuracy of %.3f on test data.", score)
    logger.info("XG Boost Model has precision of %.3f on test data.", precision)
    logger.info("XG Boost Model has recall of %.3f on test data.", recall)
    logger.info("XG Boost Model has f1_Score of %.3f on test data.", f1)
    metrics["xg_boost"] = [score, precision, recall, f1, y_pred]

    y_pred = regressor_decision_tree.predict(X_test)
    
    score = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    logger = logging.getLogger(__name__)
    logger.info("Decision Tree Model has accuracy of %.3f on test data.", score)
    logger.info("Decision Tree Model has precision of %.3f on test data.", precision)
    logger.info("Decision Tree Model has recall of %.3f on test data.", recall)
    logger.info("Decision Tree Model has f1_Score of %.3f on test data.", f1)
    metrics["decision_tree"] = [score, precision, recall, f1, y_pred]

    best_f1_score = 0
    model = None
    y_pred = []

    for i in metrics.keys():
        if metrics[i][3] > best_f1_score:
            best_f1_score = metrics[i][3]
            model = i
            y_pred = metrics[i][-1]

    for i in metrics.keys():
        del metrics[i][-1]

    logger.info("Selected Model Algorithm: " + model)

    if model == "logistic_regression":
        regressor = regressor_logistic_regression
    elif model == "decision_tree":
        regressor = regressor_decision_tree
    elif model == "random_forest":
        regressor = regressor_random_forest
    elif model == "xg_boost":
        regressor = regressor_xg_boost

    metrics = {f"value_{i+1}": value for i, value in enumerate(metrics[model])}

    return y_pred, metrics, regressor, regressor, {"model":model}


def prediction_drift_check(user_df, y_test: pd.Series):
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
        current_data=pd.DataFrame(user_df["Depression"]),
    )

    if json.loads(report.json())["metrics"][1]["result"]["drift_by_columns"][
        "Depression"
    ]["drift_detected"]:
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
