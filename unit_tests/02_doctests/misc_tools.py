"""Collection of miscellaneous tools useful in a variety of situations."""

import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


def weighted_average(data_col=None, weight_col=None, data=None):
    """Simple calculation of weighted average.

    Examples
    --------
    >>> df_nccb = pd.DataFrame({
    ...     'rate': [2, 3, 2],
    ...     'start_leg_amount': [100, 200, 100]},
    ... )
    >>> result = weighted_average(data_col='rate', weight_col='start_leg_amount', data=df_nccb)
    >>> float(result)
    2.5
    """

    def weights_function(row):
        return data.loc[row.index, weight_col]

    def wm(row):
        return np.average(row, weights=weights_function(row))

    result = wm(data[data_col])
    return result


def get_most_recent_quarter_end(d):
    """Take a datetime and find the most recent quarter end date.

    Examples
    --------
    >>> d = pd.to_datetime('2019-10-21')
    >>> get_most_recent_quarter_end(d)
    datetime.datetime(2019, 9, 30, 0, 0)
    """
    quarter_month = (d.month - 1) // 3 * 3 + 1
    quarter_end = datetime.datetime(d.year, quarter_month, 1) - relativedelta(days=1)
    return quarter_end
