
import pandas as pd

from src.exceptions import MissingRequiredColumnsError


def validate_data(data, config):

    valid_data = {}
    bad_records = []

    validation_config = config["validation"]

    for dataset_name, df in data.items():

        if dataset_name not in validation_config:
            valid_data[dataset_name] = df
            continue

        rules = validation_config[dataset_name]

        required_columns = rules["required_columns"]
        unique_columns = rules["unique_columns"]

        # Check required columns
        missing_columns = [
            col for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            raise MissingRequiredColumnsError(
                f"Missing required columns in {dataset_name}: {missing_columns}"
            )

        # Check missing values
        error_reasons = pd.Series("", index=df.index)

        null_mask = df[required_columns].isnull().any(axis=1)

        error_reasons.loc[null_mask] = "Missing required values"

        # Check duplicates
        duplicate_mask = df.duplicated(
            subset=unique_columns,
            keep=False
        )

        error_reasons.loc[duplicate_mask] = (
            error_reasons.loc[duplicate_mask]
            .apply(
                lambda x: x + "; Duplicate records"
                if x else "Duplicate records"
            )
        )

        # Identify bad records
        bad_mask = null_mask | duplicate_mask

        bad_df = df.loc[bad_mask].copy()

        if not bad_df.empty:

            bad_df["dataset_name"] = dataset_name

            bad_df["validation_error"] = (
                error_reasons.loc[bad_mask]
            )

            bad_records.append(bad_df)

        # Store valid records
        valid_data[dataset_name] = df.loc[~bad_mask].copy()

        print(
            f"{dataset_name}: "
            f"Valid = {(~bad_mask).sum()}, "
            f"Invalid = {bad_mask.sum()}"
        )

    # Combine bad records
    if bad_records:

        bad_records_df = pd.concat(
            bad_records,
            ignore_index=True,
            sort=False
        )

    else:
        bad_records_df = pd.DataFrame()

    return valid_data, bad_records_df
