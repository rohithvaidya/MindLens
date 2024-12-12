from kedro.pipeline import Pipeline, node, pipeline

from .nodes import xplain_model_prediction, prediction_confidence


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=xplain_model_prediction,
                inputs=["sklearn_model", "user_accounts_predictions_log", "params:userid"],
                outputs=["shap_instance_features_to_prediction", "shap_instance_features_away_prediction"],
                name="xplain_model_prediction",
            ),
            node(
                func=prediction_confidence,
                inputs=["user_accounts_predictions_log", "params:userid", "model_selection_name", "conformal_logistic_regression",
                    "conformal_decision_tree",
                    "conformal_xg_boost",
                    "conformal_random_forest"],
                outputs="prediction_confidence",
                name="prediction_confidence",
            )
        ]
    )
