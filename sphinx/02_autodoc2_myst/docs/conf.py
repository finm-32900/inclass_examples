# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

# -- Project information -----------------------------------------------------

project = "My First Docs"
copyright = "2025, Student Name"
author = "Student Name"
release = "0.1"

# -- Extensions --------------------------------------------------------------

extensions = [
    "myst_parser",  # Markdown instead of reStructuredText
    "autodoc2",     # Auto-generate API docs from Python source
]

# -- autodoc2 settings -------------------------------------------------------

autodoc2_packages = [
    "../sample_module.py",
]
autodoc2_render_plugin = "myst"
autodoc2_docstring_parser_regexes = [
    (r".*", "numpy_myst_parser"),  # Parse NumPy-style docstrings → MyST
]

# -- HTML output --------------------------------------------------------------

html_theme = "sphinx_book_theme"

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
