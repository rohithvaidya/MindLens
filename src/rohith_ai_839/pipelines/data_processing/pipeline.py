from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_dataset, preprocess_user_predictions_log


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_dataset,
                inputs=["dataset"],
                outputs="model_input_dataset",
                name="preprocess_dataset_node",
            ), 
            node(
                func=preprocess_user_predictions_log,
                inputs=["dataset", "survey_inputs_log"],
                outputs="user_accounts_predictions_log",
                name="preprocess_user_predictions_log_node",
            ), 
        ]
    )
