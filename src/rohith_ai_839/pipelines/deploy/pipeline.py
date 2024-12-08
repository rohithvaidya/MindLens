from kedro.pipeline import Pipeline, node, pipeline

from .nodes import get_run_id, serve_model


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=get_run_id,
                inputs="sklearn_model",
                outputs="current_run_id",
                name="get_run_id",
            ), 
            node(
                func=serve_model,
                inputs="current_run_id",
                outputs=None,
                name="serve_model",
            )
        ]
    )
