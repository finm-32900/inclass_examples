# LaTeX Examples

This directory contains progressive examples for learning LaTeX, from the absolute minimum to full articles and presentations.

## Prerequisites

Install [TeX Live](https://tug.org/texlive/) to compile these examples.

## Contents

| Directory | Description |
|-----------|-------------|
| [01_minimal/](01_minimal/) | Bare minimum LaTeX document (5 lines) |
| [02_basic_structure/](02_basic_structure/) | Document structure: title, sections, margins |
| [03_math_and_lists/](03_math_and_lists/) | Mathematical typesetting and lists |
| [04_figures_and_tables/](04_figures_and_tables/) | Including figures and creating tables |
| [05_bibliography/](05_bibliography/) | Citations and references (complete article) |
| [06_beamer_minimal/](06_beamer_minimal/) | Minimal presentation with Beamer |
| [07_beamer_full/](07_beamer_full/) | Full presentation with Metropolis theme |
| [08_handout/](08_handout/) | Custom handout template with sidebars |

## Compilation

Most examples compile with:
```bash
pdflatex filename.tex
```

For documents with bibliography using bibtex (05, 07):
```bash
pdflatex filename.tex
bibtex filename
pdflatex filename.tex
pdflatex filename.tex
```

For documents with bibliography using biblatex/biber (08):
```bash
pdflatex filename.tex
biber filename
pdflatex filename.tex
pdflatex filename.tex
```

For Beamer with Metropolis theme (07), you may need XeLaTeX for best font support:
```bash
xelatex filename.tex
```

## Progression

1. **01_minimal**: LaTeX compiles with almost nothing
2. **02_basic_structure**: Preamble vs body, packages, document metadata
3. **03_math_and_lists**: LaTeX's core strength - beautiful math
4. **04_figures_and_tables**: Floats, external content, cross-references
5. **05_bibliography**: Academic writing with citations
6. **06_beamer_minimal**: Presentations use frames, not pages
7. **07_beamer_full**: Professional presentations with themes
8. **08_handout**: Custom class files, sidebars, branding
