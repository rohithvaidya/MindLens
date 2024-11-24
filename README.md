# Decision based on Credit history ML Ops Pipeline

## Overview

This project implements an end-to-end machine learning pipeline to predict credit risk, leveraging the Kedro framework for reproducibility, modularity, and scalability. The dataset contains various features about credit applicants, including demographic information, financial details, and existing credit history. The goal is to classify applicants as low or high credit risk, using a logistic regression model as the core algorithm.

Methodology:
The project is built using Kedro, a structured framework that helps organize the data pipeline in a modular fashion. The process begins with data ingestion, followed by preprocessing, feature engineering, model training, and evaluation.

Data Ingestion: The dataset, which includes features like checking_status, duration, credit_amount, and numerical indicators (X_1 to X_10), is loaded into the pipeline using Kedro's DataCatalog. The target variable (y) represents the credit risk classification.

Data Preprocessing: Preprocessing includes handling missing values, encoding categorical variables (e.g., checking_status, credit_history), and scaling numerical features. Standardization is applied to ensure logistic regression performs optimally across all features.

Feature Engineering: Feature transformations, such as one-hot encoding for categorical variables and normalization for numerical variables, are applied. New features were created based on domain knowledge, such as interactions between financial and demographic factors.

Model Training: The logistic regression model is implemented using sklearn with an L2 penalty for regularization. Cross-validation is employed to tune hyperparameters, ensuring robust model performance.

Model Evaluation: Model performance is evaluated on key metrics like accuracy, precision, recall, and AUC-ROC to assess the classification of credit risk. These metrics are tracked and logged using MLflow for experiment management.

Results:
The logistic regression model achieved a balanced accuracy with meaningful separation between low and high-risk applicants. Model performance was enhanced through feature scaling and the careful selection of categorical features. The implementation of MLOps practices ensured that the project is fully reproducible, scalable, and production-ready.

Conclusion:
This Kedro-based MLOps project successfully demonstrates the application of logistic regression for credit risk classification. Kedro’s pipeline-driven approach ensured clear separation of concerns, from data preprocessing to model training, while enabling robust experiment tracking with MLflow. This workflow can be easily extended to incorporate new data, algorithms, or deployment to production environments, making it a reliable foundation for continuous improvement in credit risk modeling.

## Build Pipeline Docs Quarto

```
cd quarto
quartodoc build
quarto preview
```

## Visualise ML Ops Pipeline

```
kedro viz run
``` 

## API endpoint for the model

The model can be served using mlflow and is accessible using, 

```
import requests

url = "http://127.0.0.1:8001/invocations"

data = {"instances": [list(X_test.values[5])]}

response = requests.post(
    url, headers={"Content-Type": "application/json"}, data=json.dumps(data)
)

print(response.json())
``` 

## Distribution Shifts

This project is centered around data and prediction drift detection in machine learning pipelines, with the primary goal of tracking how data distributions and model predictions evolve over time. By identifying these changes (or "drifts"), the system ensures that models remain robust and continue to perform accurately when confronted with new data.
Key Components

    Drift Detection:
        The project includes two types of drift detection:
            Data Drift: Compares the features in the training data (X_train) and the incoming test data (X_test) to detect changes in feature distributions.
            Prediction Drift: Compares the true labels (y_test) and predicted labels (y_pred) to check for deviations in the distribution of predictions.
        The drift detection is handled using the Evidently library’s DataDriftPreset, which automatically computes metrics for detecting drift.
        The results of these drift analyses are saved both as JSON and HTML reports for further examination.

    Distribution Plotting:
        The project generates visual plots of feature distributions for both the current and reference data, allowing a visual understanding of the drift.
        The function plot_and_save uses Plotly to create and save these plots as PNG files.
        These plots show the probability density distributions for each feature in both the current (new) data and the reference (original) data.

    Integration and Reporting:
        The report_plotly function integrates the drift reports (from both data and predictions), extracts the drift information for each feature or column, and generates the distribution plots for each feature.
        The final output is a set of saved PNG images for each feature, visually comparing how the distributions of the feature in the reference data and current data differ.

## How to install dependencies

Declare any dependencies in `requirements.txt` for `pip` installation.

To install them, run:

```
pip install -r requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

## How to test your Kedro project

Have a look at the files `src/tests/test_run.py` and `src/tests/pipelines/data_science/test_pipeline.py` for instructions on how to write your tests. Run the tests as follows:

```
pytest
```


To configure the coverage threshold, look at the `.coveragerc` file.

## Project dependencies

To see and update the dependency requirements for your project use `requirements.txt`. You can install the project requirements with `pip install -r requirements.txt`.

[Further information about project dependencies](https://docs.kedro.org/en/stable/kedro_project_setup/dependencies.html#project-specific-dependencies)

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter
To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```
