from kedro.pipeline import Pipeline, node, pipeline

from .nodes import compare_trained_models, aggregate_shap_explanations


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=compare_trained_models,
                inputs="sklearn_model",
                outputs=None,
                name="compare_trained_models",
            ), 
            node(
                func=aggregate_shap_explanations,
                inputs=["X_train", "sklearn_model"],
                outputs=None,
                name="aggregate_shap"
            )
        ]
    )
