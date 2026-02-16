"""Collection of miscellaneous tools useful in a variety of situations."""

import datetime

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta


def weighted_average(data_col=None, weight_col=None, data=None):
    """Simple calculation of weighted average."""

    def weights_function(row):
        return data.loc[row.index, weight_col]

    def wm(row):
        return np.average(row, weights=weights_function(row))

    result = wm(data[data_col])
    return result


def get_most_recent_quarter_end(d):
    """Take a datetime and find the most recent quarter end date."""
    quarter_month = (d.month - 1) // 3 * 3 + 1
    quarter_end = datetime.datetime(d.year, quarter_month, 1) - relativedelta(days=1)
    return quarter_end
