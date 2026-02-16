"""Custom docstring parser: NumPy-style docstrings → MyST Markdown.

autodoc2's built-in "myst" parser treats docstrings as plain Markdown,
so NumPy sections (Parameters, Returns, …) render as flat text.
This parser uses numpydoc to convert them into structured Markdown
before handing off to MystParser.

See: https://github.com/sphinx-extensions2/sphinx-autodoc2/issues/33
"""

from __future__ import annotations

import textwrap

from docutils import nodes
from myst_parser.parsers.sphinx_ import MystParser
from numpydoc.docscrape import NumpyDocString, Parameter

_PARAM_SECTIONS = (
    "Parameters",
    "Returns",
    "Yields",
    "Receives",
    "Other Parameters",
    "Raises",
    "Warns",
    "Attributes",
)

_TEXT_SECTIONS = (
    "Warnings",
    "Notes",
    "References",
    "Examples",
)


def _render_param(p: Parameter) -> str:
    parts = ""
    if p.name:
        parts += f"**{p.name.replace('*', chr(92) + '*')}**"
    if p.type:
        parts += f" (_{p.type.replace('_', chr(92) + '_')}_)"
    if p.desc:
        parts += ": " + " ".join(p.desc)
    return parts


def _numpy_to_markdown(doc: str) -> str:
    parsed = NumpyDocString(doc)
    result = ""

    if summary := parsed["Summary"]:
        result += textwrap.dedent("\n".join(summary))

    if extended := parsed["Extended Summary"]:
        result += "\n\n" + textwrap.dedent("\n".join(extended))

    for title in _PARAM_SECTIONS:
        section = parsed[title]
        if not section:
            continue
        result += f"\n\n**{title}**\n\n"
        result += "\n".join("- " + _render_param(p) for p in section)

    for title in _TEXT_SECTIONS:
        section = parsed[title]
        if not section:
            continue
        result += f"\n\n**{title}**\n\n"
        result += textwrap.dedent("\n".join(section))

    return result


class NumpyMystParser(MystParser):
    """Parse NumPy-style docstrings, converting to MyST before rendering."""

    def parse(self, inputstring: str, document: nodes.document) -> None:
        inputstring = _numpy_to_markdown(inputstring)
        return super().parse(inputstring, document)


# autodoc2 looks for a ``Parser`` attribute in the module.
Parser = NumpyMystParser
