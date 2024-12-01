import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import metrics
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)
from sklearn.model_selection import (
    KFold,
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier


def preprocess_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    # Removing ID column
    dataset = dataset.drop(["id"], axis=1)

    """We have to clean the columns 
    City
    Profession
    Sleep Duration
    Dietary Habits
    Degree """

    # Removing cities which have less than 5 depressed people
    unique_cities = dataset['City'].unique()

    # Remove fraud entries
    for city in unique_cities:
        num_depressed_people = dataset[dataset['City']==city][dataset['Depression'] == 1.0].count()[0]
        if num_depressed_people < 5:
            dataset = dataset[dataset['City'] != city]
    # Cleaning profession feature
    pro = dataset["Profession"].value_counts()[1:35].reset_index()["Profession"].to_list()
    dataset["Profession"] = np.where(dataset["Profession"].isin(pro), dataset["Profession"], "Other")
    
    #Categorising sleep duration
    sd = dataset["Sleep Duration"].value_counts()[0:4].reset_index()['Sleep Duration'].to_list()
    dataset["Sleep Duration"] = np.where(dataset["Sleep Duration"].isin(sd), dataset["Sleep Duration"], "1-8")
        
    dh = dataset['Dietary Habits'].value_counts()[0:3].reset_index()['Dietary Habits'].to_list()
    dataset['Dietary Habits'] = np.where(dataset['Dietary Habits'].isin(dh), dataset['Dietary Habits'], 'Moderate')

    deg = dataset['Degree'].value_counts()[:27].reset_index()['Degree'].to_list()
    dataset['Degree'] = np.where(dataset['Degree'].isin(deg), dataset['Degree'], "Other")

    dataset = dataset.fillna(0)

    object_cols = [col for col in dataset.columns if dataset[col].dtype == "object"]
    le = LabelEncoder()

    # Apply LabelEncoder to each categorical column and replace it in the DataFrame
    for col in object_cols:
        dataset[col] = le.fit_transform(dataset[col])
        

    return dataset
