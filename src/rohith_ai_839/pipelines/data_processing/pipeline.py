from kedro.pipeline import Pipeline, node, pipeline

from .nodes import preprocess_dataset


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=preprocess_dataset,
                inputs=["dataset"],
                outputs="model_input_dataset",
                name="preprocess_dataset_node",
            )
        ]
    )
