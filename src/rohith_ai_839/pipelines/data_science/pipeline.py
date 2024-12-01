from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    evaluate_all_models,
    prediction_drift_check,
    quality_drift_check,
    report_plotly,
    split_data,
    train_logistic_regression,
    train_random_forest,
    train_xg_boost,
    train_decision_tree
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=split_data,
                inputs=["model_input_dataset", "params:model_options"],
                outputs=["X_train", "X_test", "y_train", "y_test"],
                name="split_data_node",
            ),
            node(
                func=train_logistic_regression,
                inputs=["X_train", "y_train"],
                outputs="regressor_logistic_regression",
                name="train_model_node_logistic_regression",
            ),
            node(
                func=train_random_forest,
                inputs=["X_train", "y_train"],
                outputs="regressor_random_forest",
                name="train_model_node_random_forest",
            ),
            node(
                func=train_xg_boost,
                inputs=["X_train", "y_train"],
                outputs="regressor_xg_boost",
                name="train_model_node_xg_boost",
            ),
            node(
                func=train_decision_tree,
                inputs=["X_train", "y_train"],
                outputs="regressor_decision_tree",
                name="train_model_node_decision_tree",
            ),
            node(
                func=evaluate_all_models,
                inputs=["regressor_logistic_regression", "regressor_decision_tree", "regressor_xg_boost", "regressor_random_forest","X_test", "y_test"],
                outputs=["y_pred", "metrics", "sklearn_model"],
                name="evaluate_all_models",
            ),
            node(
                func=quality_drift_check,
                inputs=["X_train", "X_test"],
                outputs="data_drift",
                name="data_quality_check",
            ),
            node(
                func=prediction_drift_check,
                inputs=["y_test", "y_pred"],
                outputs="pred_drift",
                name="pred_drift_check",
            ),
            node(
                func=report_plotly,
                inputs=["data_drift", "pred_drift"],
                outputs=None,
                name="report_plotly",
            ),
        ]
    )
