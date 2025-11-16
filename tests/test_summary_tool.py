"""Basic tests for summary_tool functions."""

import pandas as pd
from src.summary_tool import summarize_totals


def test_summarize_totals_basic():
    data = {
        "amount": [100, -50, 200, -25],
    }
    df = pd.DataFrame(data)
    result = summarize_totals(df)

    assert result["total_income"] == 300
    assert result["total_expenses"] == -75
    assert result["net_balance"] == 225
