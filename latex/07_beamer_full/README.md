# 07 - Full Beamer Presentation with Metropolis

## What You'll Learn

- The Metropolis theme for modern presentations
- Progress bars and professional styling
- Columns layout for side-by-side content
- PGFPlots for charts directly in LaTeX
- Multiple block styles
- Appendix slides that don't count toward total
- Standout frames for emphasis

## Key Concepts

### Metropolis Theme

```latex
\documentclass{beamer}
\usetheme[progressbar=frametitle]{metropolis}
```

Features:
- Minimal, clean design
- Progress bar showing position in presentation
- Professional typography

### Columns

```latex
\begin{columns}[T,onlytextwidth]
    \column{0.5\textwidth}
    Left content

    \column{0.5\textwidth}
    Right content
\end{columns}
```

### PGFPlots

Create plots directly in LaTeX:
```latex
\begin{tikzpicture}
    \begin{axis}[...]
        \addplot {sin(deg(x))};
    \end{axis}
\end{tikzpicture}
```

### Appendix Slides

```latex
\usepackage{appendixnumberbeamer}
...
\appendix
\begin{frame}{Backup}
    These slides don't count in "slide X of Y"
\end{frame}
```

### Standout Frame

```latex
{\setbeamercolor{palette primary}{fg=black, bg=yellow}
\begin{frame}[standout]
    Questions?
\end{frame}
}
```

### Fragile Frames

Use `[fragile]` for frames with verbatim content:
```latex
\begin{frame}[fragile]{Code Example}
    \begin{verbatim}
    code here
    \end{verbatim}
\end{frame}
```

## Files in This Example

- `slides_full.tex` - The main presentation
- `bibliography.bib` - References

## How to Compile

For best results with Metropolis (proper fonts):
```bash
xelatex slides_full.tex
bibtex slides_full
xelatex slides_full.tex
xelatex slides_full.tex
```

Or with pdflatex (works but fonts may differ):
```bash
pdflatex slides_full.tex
bibtex slides_full
pdflatex slides_full.tex
pdflatex slides_full.tex
```

## Try It

1. Change the progress bar: `progressbar=foot` or `progressbar=none`
2. Add slide animations with `\pause`
3. Create a frame with an included image
4. Change the standout frame color
5. Add more backup slides in the appendix
