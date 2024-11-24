from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
   compare_trained_models
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=compare_trained_models,
                inputs="sklearn_model",
                outputs=None,
                name="compare_trained_models",
            )
        ]
    )
