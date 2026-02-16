# Sphinx Documentation Examples

This directory contains progressive examples for learning
[Sphinx](https://www.sphinx-doc.org/), the Python documentation generator
used throughout the course projects.

## Prerequisites

Install Sphinx (included in most course environments):

```bash
pip install sphinx
```

## Contents

| Directory | Description |
|-----------|-------------|
| [01_quickstart/](01_quickstart/) | Bootstrap a Sphinx project with `sphinx-quickstart` |
| [02_autodoc2_myst/](02_autodoc2_myst/) | Add autodoc2, MyST Markdown, and the Book theme |

## Progression

1. **01_quickstart**: Run `sphinx-quickstart` to create a project from scratch,
   build with `make html`, and view the default alabaster-themed site.
2. **02_autodoc2_myst**: Modify `conf.py` to use `myst-parser` (Markdown instead
   of reStructuredText), `autodoc2` (auto-generate API docs from Python docstrings),
   and `sphinx-book-theme` (the theme used in course projects).
