import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the input dataset by performing a series of cleaning and transformation steps to prepare it for analysis or modeling.

    The preprocessing steps include:
    1. Removing the "id" column.
    2. Filtering out cities with fewer than 5 cases of depression.
    3. Cleaning and grouping categorical variables:
        - "Profession": Grouping less frequent professions into an "Other" category.
        - "Sleep Duration": Categorizing uncommon sleep durations into "1-8".
        - "Dietary Habits": Grouping rare dietary habits into a "Moderate" category.
        - "Degree": Consolidating less frequent degrees into an "Other" category.
    4. Filling missing values with zero.
    5. Encoding categorical variables using `LabelEncoder`.
    6. Renaming the column "Have you ever had suicidal thoughts ?" to "suicidal_thoughts".

    Args:
        dataset (pd.DataFrame): The input dataset containing survey data. 
            Must include the following columns:
            - "id"
            - "City"
            - "Profession"
            - "Sleep Duration"
            - "Dietary Habits"
            - "Degree"
            - "Have you ever had suicidal thoughts ?"
            - "Depression" (binary, 0 or 1)

    Returns:
        pd.DataFrame: The preprocessed dataset ready for further analysis or modeling.

    Note:
        - Ensure that the input dataset has all required columns before calling this function.
        - The function modifies categorical variables to handle sparsity and reduce dimensionality.
    """
    # Removing ID column
    dataset = dataset.drop(["id"], axis=1)

    # Removing cities which have less than 5 depressed people
    unique_cities = dataset["City"].unique()

    # Remove fraud entries
    for city in unique_cities:
        num_depressed_people = dataset[dataset["City"] == city][
            dataset["Depression"] == 1.0
        ].count()[0]
        if num_depressed_people < 5:
            dataset = dataset[dataset["City"] != city]
    # Cleaning profession feature
    pro = (
        dataset["Profession"].value_counts()[1:35].reset_index()["Profession"].to_list()
    )
    dataset["Profession"] = np.where(
        dataset["Profession"].isin(pro), dataset["Profession"], "Other"
    )

    # Categorising sleep duration
    sd = (
        dataset["Sleep Duration"]
        .value_counts()[0:4]
        .reset_index()["Sleep Duration"]
        .to_list()
    )
    dataset["Sleep Duration"] = np.where(
        dataset["Sleep Duration"].isin(sd), dataset["Sleep Duration"], "1-8"
    )

    dh = (
        dataset["Dietary Habits"]
        .value_counts()[0:3]
        .reset_index()["Dietary Habits"]
        .to_list()
    )
    dataset["Dietary Habits"] = np.where(
        dataset["Dietary Habits"].isin(dh), dataset["Dietary Habits"], "Moderate"
    )

    deg = dataset["Degree"].value_counts()[:27].reset_index()["Degree"].to_list()
    dataset["Degree"] = np.where(
        dataset["Degree"].isin(deg), dataset["Degree"], "Other"
    )

    dataset = dataset.fillna(0)

    object_cols = [col for col in dataset.columns if dataset[col].dtype == "object"]
    le = LabelEncoder()

    # Apply LabelEncoder to each categorical column and replace it in the DataFrame
    for col in object_cols:
        dataset[col] = le.fit_transform(dataset[col])

    # Renaming a column suicidal_thoughts

    dataset = dataset.rename(
        columns={"Have you ever had suicidal thoughts ?": "suicidal_thoughts"}
    )

    return dataset


def preprocess_user_predictions_log(dataset: pd.DataFrame, survey_inputs_log: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses user prediction logs by aligning the survey inputs with the characteristics of the training dataset.

    This function cleans and transforms the input `survey_inputs_log` dataset based on the distribution and properties of the training `dataset`. 
    The preprocessing steps ensure consistency between the datasets for predictions.

    Steps performed:
    1. Filters cities in `survey_inputs_log` that are not present in the training dataset with at least 5 depressed cases.
    2. Standardizes categorical variables in `survey_inputs_log`:
        - "Profession": Keeps only the top 35 professions from the training dataset; others are grouped into "Other."
        - "Sleep Duration": Retains top 4 durations from the training dataset; others are grouped into "1-8."
        - "Dietary Habits": Keeps the top 3 habits from the training dataset; others are grouped into "Moderate."
        - "Degree": Retains the top 27 degrees from the training dataset; others are grouped into "Other."
    3. Fills missing values in all columns except "Depression" with zeros.
    4. Applies `LabelEncoder` to all categorical columns in `survey_inputs_log`.
    5. Renames the column "Have you ever had suicidal thoughts ?" to "suicidal_thoughts."

    Args:
        dataset (pd.DataFrame): The training dataset used as a reference for preprocessing.
            Must include the following columns:
            - "City"
            - "Profession"
            - "Sleep Duration"
            - "Dietary Habits"
            - "Degree"
            - "Depression" (binary, 0 or 1)
        survey_inputs_log (pd.DataFrame): The dataset containing new survey inputs for prediction.
            Should have similar column structure to `dataset`.

    Returns:
        pd.DataFrame: The cleaned and transformed `survey_inputs_log` dataset ready for predictions.

    Note:
        - The function aligns the distribution of categorical features in `survey_inputs_log` with `dataset`.
        - Ensure `survey_inputs_log` has the required columns before calling this function.
        - The "Depression" column in `survey_inputs_log` (if present) is not used during preprocessing.
    """
    
    training_dataset = dataset
    test_dataset = survey_inputs_log

   # Remove cities with less than 5 depressed people from the training dataset
    unique_cities = training_dataset["City"].unique()
    city_counts = training_dataset[training_dataset["Depression"] == 1.0]["City"].value_counts()
    cities_to_keep = city_counts[city_counts >= 5].index
    test_dataset = test_dataset[test_dataset["City"].isin(cities_to_keep)]
    
    # Clean the "Profession" feature
    top_professions = training_dataset["Profession"].value_counts()[1:35].index.tolist()
    test_dataset["Profession"] = np.where(
        test_dataset["Profession"].isin(top_professions), test_dataset["Profession"], "Other"
    )
    
    # Categorize "Sleep Duration"
    top_sleep_durations = training_dataset["Sleep Duration"].value_counts()[0:4].index.tolist()
    test_dataset["Sleep Duration"] = np.where(
        test_dataset["Sleep Duration"].isin(top_sleep_durations), test_dataset["Sleep Duration"], "1-8"
    )
    
    # Categorize "Dietary Habits"
    top_dietary_habits = training_dataset["Dietary Habits"].value_counts()[0:3].index.tolist()
    test_dataset["Dietary Habits"] = np.where(
        test_dataset["Dietary Habits"].isin(top_dietary_habits), test_dataset["Dietary Habits"], "Moderate"
    )
    
    # Categorize "Degree"
    top_degrees = training_dataset["Degree"].value_counts()[:27].index.tolist()
    test_dataset["Degree"] = np.where(
        test_dataset["Degree"].isin(top_degrees), test_dataset["Degree"], "Other"
    )
    
    # Fill missing values
    test_dataset.loc[:, test_dataset.columns != "Depression"] = test_dataset.loc[:, test_dataset.columns != "Depression"].fillna(0)
    
    # Label encoding for object columns
    object_cols = [col for col in test_dataset.columns if test_dataset[col].dtype == "object"]
    le = LabelEncoder()
    for col in object_cols:
        test_dataset[col] = le.fit_transform(test_dataset[col])
    
    # Rename the column "Have you ever had suicidal thoughts ?"
    test_dataset = test_dataset.rename(
        columns={"Have you ever had suicidal thoughts ?": "suicidal_thoughts"}
    )
    
    return test_dataset