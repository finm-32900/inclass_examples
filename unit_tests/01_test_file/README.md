# Unit Tests in a Test File

The standard approach to unit testing: write tests in a separate file and run them with `pytest`.

## What Makes a Good Unit Test?

- **Specific**: Tests a single aspect of the function's behavior
- **Isolated**: Does not rely on external systems or complex setup
- **Repeatable**: Produces the same results every time
- **Readable**: Clearly conveys what is being tested

Use the **Arrange-Act-Assert** pattern in each test:

1. **Arrange** — set up test data
2. **Act** — call the function
3. **Assert** — check the result

## Files

- `misc_tools.py` — Module with functions to test (`weighted_average`, `get_most_recent_quarter_end`)
- `test_misc_tools.py` — Test file with `pytest`-style test functions

## How to Run

```sh
pytest test_misc_tools.py
```

or simply:

```sh
pytest
```

`pytest` automatically discovers and runs all functions named `test_*` in files named `test_*.py`.
