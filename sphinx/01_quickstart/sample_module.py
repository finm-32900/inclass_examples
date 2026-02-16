"""Simple financial calculations for Sphinx documentation demo."""


def present_value(cash_flow, rate, periods):
    """Calculate the present value of a future cash flow.

    Parameters
    ----------
    cash_flow : float
        The future cash flow amount.
    rate : float
        The discount rate per period (e.g., 0.05 for 5%).
    periods : int
        The number of periods until the cash flow is received.

    Returns
    -------
    float
        The present value of the cash flow.

    Examples
    --------
    >>> present_value(100, 0.05, 2)
    90.70294784580498
    """
    return cash_flow / (1 + rate) ** periods


def annuity_factor(rate, periods):
    """Calculate the annuity factor (present value of $1 per period).

    Parameters
    ----------
    rate : float
        The discount rate per period.
    periods : int
        The number of periods.

    Returns
    -------
    float
        The annuity factor.

    Examples
    --------
    >>> round(annuity_factor(0.05, 10), 4)
    7.7217
    """
    if rate == 0:
        return float(periods)
    return (1 - (1 + rate) ** -periods) / rate
