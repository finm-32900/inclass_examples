import pandas as pd

from misc_tools import (
    get_most_recent_quarter_end,
    weighted_average,
)


def test_weighted_average():
    # Arrange: set up test data
    df_nccb = pd.DataFrame({"rate": [2, 3, 2], "start_leg_amount": [100, 200, 100]})
    # Act: call the function
    result = weighted_average(
        data_col="rate", weight_col="start_leg_amount", data=df_nccb
    )
    # Assert: check the result
    expected = 2.5
    assert result == expected


def test_get_most_recent_quarter_end():
    d = pd.to_datetime("2019-10-21")
    result = get_most_recent_quarter_end(d)
    expected = pd.Timestamp("2019-09-30")
    assert result == expected
