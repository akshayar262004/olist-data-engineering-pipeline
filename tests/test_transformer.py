
import pandas as pd
from src.transformer import apply_column_mapping


def test_apply_column_mapping():

    data = {
        "olist_orders_dataset": pd.DataFrame({
            "order_purchase_timestamp": ["2026-01-01"]
        })
    }

    config = {
        "column_mapping": {
            "olist_orders_dataset": {
                "order_purchase_timestamp": "purchase_timestamp"
            }
        }
    }

    result = apply_column_mapping(data, config)

    assert "purchase_timestamp" in result[
        "olist_orders_dataset"
    ].columns
