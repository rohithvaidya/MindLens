from pathlib import PurePath
from typing import Dict, Any

import pandas as pd
import arff
import fsspec

from kedro.io import AbstractVersionedDataset
from kedro.io.core import get_filepath_str, get_protocol_and_path, Version


class JSONVersionDataset(AbstractVersionedDataset):
    """
    A dataset class use to get specific version of the model_output

    Attributes:
    -----------
        _protocol (str): The protocol extracted from the file path (e.g., 'file', 's3').
        _filepath (PurePath): The path to the ARFF file, excluding the protocol.
        _fs (fsspec.AbstractFileSystem): The file system handler based on the protocol.

    Methods:
    --------
        _load() -> pd.DataFrame:
            Loads the ARFF file into a pandas DataFrame.

        _save():
            Placeholder for saving functionality, if needed.

        _describe() -> Dict[str, Any]:
            Provides a description of the dataset, including the file path, version,
            and protocol used.
    """

    def __init__(self, filepath: str, version: Version = None):
        """
        Initializes the ARFFDataset with a specified file path and optional versioning.

        Parameters:
        -----------
            filepath (str): The path to the ARFF dataset file.
            version (Version, optional): Version identifier for tracking different versions
            of the dataset. Defaults to None.
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
        """
        Loads the ARFF dataset into a pandas DataFrame.

        This method reads the ARFF file, extracts the attributes (columns) from the
        file, and converts the data into a pandas DataFrame for further use.

        Returns:
        --------
            pd.DataFrame: The data from the ARFF file as a DataFrame, with columns
                          named after the attributes defined in the ARFF file.
        """
        # Get load path
        load_path = get_filepath_str(self._get_load_path(), self._protocol)

        # Read path as string/text file
        with self._fs.open(load_path, "r") as f:
            raw_data = arff.load(f)

        # Get columns list
        columns_list = [col[0] for col in raw_data["attributes"]]

        # Return pd.DataFrame
        return pd.DataFrame(raw_data["data"], columns=columns_list)

    def _save(self):
        """
        Placeholder method for saving functionality.

        Currently, this method does not implement any saving logic but is provided for
        future extensions where saving the dataset might be required.
        """
        pass

    def _describe(self) -> Dict[str, Any]:
        """
        Describes the ARFF dataset, including file path, version, and protocol.

        Returns:
        --------
            Dict[str, Any]: A dictionary containing metadata about the dataset, such as
                            the file path, protocol, and version.
        """
        return dict(
            filepath=self._filepath, version=self._version, protocol=self._protocol
        )
