from pathlib import PurePath
from typing import Dict, Any

import pandas as pd
from evidently.report import Report
from evidently.utils.dashboard import SaveMode
import fsspec

from kedro.io import AbstractVersionedDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path, Version
import os


class EvidentlyReportHTML(AbstractVersionedDataset):
    """
    Dataset class for saving Evidently AI reports as HTML files.

    This class is responsible for managing the saving of Evidently reports in
    HTML format, utilizing versioning capabilities from `AbstractVersionedDataset`.

    Attributes:
    -----------
        _protocol : str
            The protocol (e.g., local or remote storage system)
            extracted from the filepath.
        _filepath : PurePath
            The path to the file without the protocol.
        _fs : fsspec.AbstractFileSystem
            The file system object, based on the protocol.

    Methods:
    --------
        _load():
            Placeholder for loading functionality, if needed.

        _save():
            Saves an Evidently AI report as a single HTML file to a specified location.

        _describe() -> Dict[str, Any]:
            Placeholder for describe functionality, if needed.
    """

    def __init__(self, filepath: str, version: Version = None, **kwargs):
        """
        Constructor for EvidentlyReportHTML

        Parameters:
        ------------
            filepath : str
                The file path where the Evidently report HTML will be saved.
            version : Union[Version, optional]
                Version identifier to track different versions of the report dataset. Defaults to None.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        protocol, path = get_protocol_and_path(filepath)
        self._protocol = protocol
        self._filepath = PurePath(path)
        self._fs = fsspec.filesystem(self._protocol)

        super().__init__(
            filepath=PurePath(path),
            version=version,
            exists_function=self._fs.exists,
            glob_function=self._fs.glob,
        )

    def _load(self) -> pd.DataFrame:
        # """
        # Loads the ARFF dataset to a Pandas DataFrame

        # Returns:
        #     pd.DataFrame
        # """
        # # Get load path
        # load_path = get_filepath_str(self._get_load_path(), self._protocol)

        # # Read path as string/text file
        # with self._fs.open(load_path, "r") as f:
        #     raw_data = arff.load(f)

        # # Get columns list
        # columns_list = [col[0] for col in raw_data['attributes']]

        # # Return pd.DataFrame
        # return pd.DataFrame(raw_data['data'], columns=columns_list)
        ...

    def _save(self, report: Report) -> None:
        """
        Saves an Evidently AI report as a single HTML file to a specified location.

        Parameters:
        -----------
            report : Report
                The Evidently `Report` object to be saved.

        The function constructs the save path using an internal method (`_get_save_path`),
        ensures that the target directory exists (creates it if not), and then saves
        the report as an HTML file in "singlefile" mode.

        Raises:
        -------
            OSError: If the target directory cannot be created.
        """
        save_path = get_filepath_str(self._get_save_path(), self._protocol)

        os.makedirs(os.path.dirname(save_path), exist_ok=False)

        report.save_html(filename=save_path, mode="singlefile")

    def _describe(self) -> Dict[str, Any]:
        """
        Describes the Evidently HTML dataset, including file path, version, and protocol.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing metadata about the dataset, such as
                            the file path, protocol, and version.
        """
        return dict(
            filepath=self._filepath, version=self._version, protocol=self._protocol
        )
