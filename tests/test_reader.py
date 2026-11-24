
import pandas as pd
from src.reader import read_all_csv


def test_read_all_csv(tmp_path):
    df = pd.DataFrame({
        "order_id": ["101", "102"],
        "status": ["delivered", "shipped"]
    })

    df.to_csv(tmp_path / "orders.csv", index=False)

    result = read_all_csv(tmp_path)

    assert "orders" in result
    assert len(result["orders"]) == 2


def test_read_all_csv_columns(tmp_path):
    df = pd.DataFrame({
        "order_id": ["101"],
        "status": ["delivered"]
    })

    df.to_csv(tmp_path / "orders.csv", index=False)

    result = read_all_csv(tmp_path)

    assert list(result["orders"].columns) == [
        "order_id", "status"
    ]
