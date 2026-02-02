# 01 - Minimal LaTeX Document

## What You'll Learn

- The absolute minimum required for a LaTeX document
- The two required parts: document class and document body

## Key Concepts

A LaTeX document needs only two things:

1. **Document class**: `\documentclass{article}` - tells LaTeX what type of document
2. **Document body**: Everything between `\begin{document}` and `\end{document}`

That's it. Four lines total.

## How to Compile

```bash
pdflatex minimal.tex
```

This creates `minimal.pdf`.

## Try It

1. Compile the document and open the PDF
2. Change "Hello, World!" to something else
3. Try changing `article` to `report` or `book` - what changes?
