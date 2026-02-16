# Doctests: Unit Tests in Docstrings

Doctests embed tests directly in a function's docstring, serving as both documentation and tests.

## Doctest Syntax

- **`>>>`** — prompt lines where you call your function
- The line immediately after — the expected output
- A blank line ends a test

Example:

```python
def weighted_average(data_col=None, weight_col=None, data=None):
    """Simple calculation of weighted average.

    Examples
    --------
    >>> df = pd.DataFrame({'rate': [2, 3, 2], 'weight': [100, 200, 100]})
    >>> weighted_average(data_col='rate', weight_col='weight', data=df)
    2.5
    """
```

## Files

- `misc_tools.py` — Module with doctests embedded in docstrings

## How to Run

```sh
pytest --doctest-modules misc_tools.py
```

`pytest --doctest-modules` searches for `>>>` prompts in all docstrings and runs them as tests.
