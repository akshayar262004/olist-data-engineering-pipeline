
import pandas as pd
import pytest

from src.validator import validate_data
from src.exceptions import MissingRequiredColumnsError


def test_validate_data_success():
    data = {
        "olist_orders_dataset": pd.DataFrame({
            "order_id": ["101", "102"],
            "customer_id": ["C1", "C2"],
            "order_status": ["delivered", "shipped"],
            "purchase_timestamp": ["2026-01-01", "2026-01-02"]
        })
    }

    config = {
        "validation": {
            "olist_orders_dataset": {
                "required_columns": [
                    "order_id",
                    "customer_id",
                    "order_status",
                    "purchase_timestamp"
                ],
                "unique_columns": ["order_id"]
            }
        }
    }

    valid_data, bad_records = validate_data(data, config)

    assert len(valid_data["olist_orders_dataset"]) == 2
    assert len(bad_records) == 0


def test_validate_data_missing_columns():
    data = {
        "olist_orders_dataset": pd.DataFrame({
            "customer_id": ["C1"],
            "order_status": ["delivered"]
        })
    }

    config = {
        "validation": {
            "olist_orders_dataset": {
                "required_columns": ["order_id", "customer_id"],
                "unique_columns": ["order_id"]
            }
        }
    }

    with pytest.raises(MissingRequiredColumnsError):
        validate_data(data, config)
