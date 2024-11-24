import pandas as pd
from sklearn.preprocessing import LabelEncoder


def preprocess_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    # If Null values detected initialise to 0
    dataset = dataset.fillna(0)

    le = LabelEncoder()
    dataset["own_telephone"] = le.fit_transform(dataset["own_telephone"])
    dataset["foreign_worker"] = le.fit_transform(dataset["foreign_worker"])
    dataset["health_status"] = le.fit_transform(dataset["health_status"])

    dataset["savings_status"] = dataset["savings_status"].map(
        {
            "<100": 0,
            "no known savings": 1,
            "100<=X<500": 2,
            "500<=X<1000": 3,
            ">=1000": 4,
        }
    )

    dataset["employment"] = dataset["employment"].map(
        {"1<=X<4": 0, ">=7": 1, "4<=X<7": 2, "<1": 3, "unemployed": 4}
    )

    dataset["checking_status"] = dataset["checking_status"].map(
        {"no checking": 0, "0<=X<200": 1, "<0": 2, ">=200": 3}
    )

    dataset = pd.get_dummies(
        dataset,
        columns=[
            "purpose",
            "credit_history",
            "personal_status",
            "housing",
            "job",
            "other_payment_plans",
            "property_magnitude",
            "other_parties",
        ],
        drop_first=True,
    )

    

    return dataset
