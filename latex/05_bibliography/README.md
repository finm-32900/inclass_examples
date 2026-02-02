# 05 - Bibliography and Citations

## What You'll Learn

- BibTeX bibliography files (`.bib`)
- Citing references with `\cite{}`
- Creating the bibliography section
- Hyperlinks with the `hyperref` package
- The abstract environment

## Key Concepts

### BibTeX Files

Bibliography entries are stored in `.bib` files:

```bibtex
@article{sharpe1964capital,
  title={Capital asset prices: A theory of ...},
  author={Sharpe, William F},
  journal={The Journal of Finance},
  volume={19},
  year={1964},
}
```

The first field (`sharpe1964capital`) is the **citation key**.

### Citation Commands

| Command | Output |
|---------|--------|
| `\cite{key}` | [Sha64] or [1] depending on style |
| `\cite{key1, key2}` | Multiple citations |

### Bibliography Styles

Common styles:
- `alpha` - [FF92] format (author initials + year)
- `plain` - [1] format (numbered)
- `abbrv` - Abbreviated author names
- `apalike` - APA-style

### Hyperref

The `hyperref` package makes citations and references clickable:
```latex
\usepackage[colorlinks=true, allcolors=blue]{hyperref}
```

## Files in This Example

- `article_with_bib.tex` - The main document
- `bibliography.bib` - BibTeX database

## How to Compile

BibTeX requires multiple passes:

```bash
pdflatex article_with_bib.tex   # First pass - finds citations
bibtex article_with_bib          # Process bibliography (no .tex extension!)
pdflatex article_with_bib.tex   # Second pass - inserts citations
pdflatex article_with_bib.tex   # Third pass - fixes references
```

Or use `latexmk` for automatic compilation:
```bash
latexmk -pdf article_with_bib.tex
```

## Try It

1. Add a new entry to the `.bib` file and cite it
2. Change `\bibliographystyle{alpha}` to `plain` and recompile
3. Add `\tableofcontents` after `\maketitle`
4. Try citing a book instead of an article
