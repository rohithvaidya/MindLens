"""``AbstractDataset`` implementations that produce pandas DataFrames."""

from typing import Any

import lazy_loader as lazy

# https://github.com/pylint-dev/pylint/issues/4300#issuecomment-1043601901
ARFFDataset: Any
EvidentlyReportHTML: Any

__getattr__, __dir__, __all__ = lazy.attach(
    __name__,
    submod_attrs={
        "arff_dataset": ["ARFFDataset"],
        "evidently_report_html_dataset": ["EvidentlyReportHTML"],
    },
)
