# 02 - Autodoc2, MyST Parser, and Sphinx Book Theme

## What You'll Learn

- How to write Sphinx documentation in **Markdown** instead of reStructuredText
- How to auto-generate API documentation from Python docstrings using **autodoc2**
- How to change the Sphinx theme to **sphinx-book-theme** (used in course projects)

## Key Concepts

### MyST Parser

[MyST](https://myst-parser.readthedocs.io/) lets you write Sphinx docs in
Markdown. Sphinx directives use a fenced-code syntax:

````markdown
```{toctree}
:maxdepth: 2

api
```
````

### autodoc2

[sphinx-autodoc2](https://sphinx-autodoc2.readthedocs.io/) scans your Python
source files and generates API documentation pages automatically. Unlike the
older `sphinx.ext.autodoc`, it does not need to import your code.

### sphinx-book-theme

The [Sphinx Book Theme](https://sphinx-book-theme.readthedocs.io/) provides a
clean, modern look and is the theme used in all course projects.

## Setup

```bash
pip install -r requirements.txt
```

## How to Run

Build the HTML documentation:

```bash
sphinx-build -b html docs docs/_build/html
```

Open the result:

```bash
open docs/_build/html/index.html
```

## Project Structure

```
02_autodoc2_myst/
├── README.md
├── requirements.txt
├── sample_module.py       # Python module with docstrings
└── docs/
    ├── conf.py            # Sphinx config (the key file!)
    ├── index.md           # Root document in MyST Markdown
    ├── api.md             # Page linking to autodoc2 output
    └── _build/            # Generated output (git-ignored)
```

## What Changed From the Quickstart Defaults

The `docs/conf.py` in this example differs from a fresh `sphinx-quickstart`
output in three ways:

### 1. Extensions

```python
extensions = [
    "myst_parser",  # Markdown instead of reStructuredText
    "autodoc2",     # Auto-generate API docs from Python source
]
```

### 2. autodoc2 Configuration

```python
autodoc2_packages = [
    "../sample_module.py",
]
autodoc2_render_plugin = "myst"
```

### 3. Theme

```python
html_theme = "sphinx_book_theme"
```

The quickstart default is `"alabaster"`.

## Try It

1. Build and view the site. Compare the look to Example 01's alabaster output.
2. Navigate to the API Reference page — notice how autodoc2 renders the module
   docstrings automatically.
3. Add a new function to `sample_module.py` with a docstring, rebuild, and
   check that it appears in the API page.
4. Open `docs/index.md` — notice the MyST `{toctree}` directive syntax compared
   to the `.rst` syntax from Example 01.
