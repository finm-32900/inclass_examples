# 02 - Basic Document Structure

## What You'll Learn

- The preamble vs document body
- Loading packages with `\usepackage`
- Document metadata: title, author, date
- Sections and subsections

## Key Concepts

### Preamble vs Body

Everything before `\begin{document}` is the **preamble**:
- Document class declaration
- Package loading
- Custom commands and settings
- Title, author, date

Everything between `\begin{document}` and `\end{document}` is the **body**:
- The actual content of your document

### Packages

Packages extend LaTeX's capabilities:
- `babel` - Language support (hyphenation, localization)
- `geometry` - Page margins and size

Load packages with: `\usepackage[options]{packagename}`

### Sections

LaTeX provides automatic numbering:
- `\section{Title}` - Main sections (1, 2, 3...)
- `\subsection{Title}` - Subsections (1.1, 1.2...)
- `\subsubsection{Title}` - Sub-subsections (1.1.1...)

## How to Compile

```bash
pdflatex basic_article.tex
```

## Try It

1. Change the author name and recompile
2. Add a new section between Background and Conclusion
3. Try `\section*{Unnumbered}` - note the asterisk removes numbering
4. Change `\today` to a specific date like `January 1, 2025`
