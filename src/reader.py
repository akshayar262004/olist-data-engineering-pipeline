
import pandas as pd
from pathlib import Path

from src.exceptions import DatasetNotFoundError


def read_all_csv(dataset_path, file_names=None):

    dataset_path = Path(dataset_path)

    if not dataset_path.exists():
        raise DatasetNotFoundError(
            f"Dataset folder not found: {dataset_path}"
        )

    if file_names is None:
        csv_files = list(dataset_path.glob("*.csv"))
    else:
        csv_files = [
            dataset_path / name
            for name in file_names
        ]

    if not csv_files:
        print("No new CSV files to process.")
        return {}

    data = {}

    for file in csv_files:

        if not file.exists():
            raise DatasetNotFoundError(
                f"Dataset file not found: {file.name}"
            )

        df = pd.read_csv(file)

        file_name = file.stem

        data[file_name] = df

        print("File loaded:", file.name)
        print("Total rows:", df.shape[0])
        print("Total columns:", df.shape[1])
        print("---------------------------")

    return data

