
import json
import logging
import yaml
from pathlib import Path

from src.reader import read_all_csv
from src.transformer import apply_column_mapping
from src.validator import validate_data
from src.exceptions import PipelineError


# Project paths
PROJECT_PATH = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_PATH / "dataset"
CONFIG_PATH = PROJECT_PATH / "config" / "config.yaml"
OUTPUT_PATH = PROJECT_PATH / "output"
LOG_PATH = PROJECT_PATH / "logs"
MANIFEST_PATH = PROJECT_PATH / "manifest.json"

# Create required folders
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)


# Configure logging
logging.basicConfig(
    filename=LOG_PATH / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logger = logging.getLogger(__name__)


# Load configuration
def load_config():

    with open(CONFIG_PATH, "r") as file:
        return yaml.safe_load(file)


# Load manifest
def load_manifest():

    if MANIFEST_PATH.exists():

        with open(MANIFEST_PATH, "r") as file:
            return json.load(file)

    return {"processed_files": []}


# Update manifest
def update_manifest(processed_files):

    manifest = {
        "processed_files": processed_files
    }

    with open(MANIFEST_PATH, "w") as file:
        json.dump(manifest, file, indent=4)


# Main pipeline
def run_pipeline():

    try:

        logger.info("Pipeline execution started")
        print("Pipeline execution started")

        # Load configuration
        config = load_config()

        # Load manifest
        manifest = load_manifest()
        processed_files = manifest["processed_files"]

        # Find new CSV files
        all_files = list(DATASET_PATH.glob("*.csv"))

        new_files = [
            file.name
            for file in all_files
            if file.name not in processed_files
        ]

        if not new_files:

            print("No new files to process.")
            logger.info("No new files to process")
            return

        # Read new CSV files
        data = read_all_csv(DATASET_PATH, new_files)

        # Apply column mapping
        transformed_data = apply_column_mapping(data, config)

        # Validate data
        valid_data, bad_records = validate_data(
            transformed_data,
            config
        )

        # Save bad records
        bad_records.to_csv(
            OUTPUT_PATH / "bad_records.csv",
            index=False
        )

        # Save valid datasets
        for name, df in valid_data.items():

            df.to_csv(
                OUTPUT_PATH / f"{name}_cleaned.csv",
                index=False
            )

        # Update manifest only after successful processing
        processed_files.extend(new_files)
        update_manifest(processed_files)

        logger.info("Pipeline completed successfully")
        print("Pipeline completed successfully")

    except PipelineError as error:

        logger.error("Pipeline failed: %s", error)
        print("Pipeline failed:", error)

    except Exception:

        logger.exception("Unexpected pipeline error")
        print("Unexpected pipeline error. Check pipeline.log")
