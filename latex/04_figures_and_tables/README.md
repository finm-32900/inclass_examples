# 04 - Figures and Tables

## What You'll Learn

- Including external images with `\includegraphics`
- The `figure` environment for floating figures
- Creating tables with `tabular`
- The `table` environment for floating tables
- Cross-referencing with `\ref`

## Key Concepts

### Figures

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=0.6\textwidth]{filename.png}
    \caption{Description of the figure.}
    \label{fig:mylabel}
\end{figure}
```

**Size options:**
- `width=0.6\textwidth` - 60% of text width
- `height=5cm` - specific height
- `scale=0.5` - scale factor

### Tables

```latex
\begin{table}[htbp]
    \centering
    \begin{tabular}{l|r|r}
        Header1 & Header2 & Header3 \\
        \hline
        Data1 & Data2 & Data3 \\
    \end{tabular}
    \caption{Table description.}
    \label{tab:mylabel}
\end{table}
```

### Floats and Placement

LaTeX "floats" figures and tables to optimal positions. The `[htbp]` specifier
is a preference, not a command:
- `h` - here
- `t` - top
- `b` - bottom
- `p` - float page

### Cross-References

Always use `\label` after `\caption`, then reference with:
- `Figure~\ref{fig:name}`
- `Table~\ref{tab:name}`

## Files in This Example

- `figures_tables.tex` - The main document
- `example_plot.png` - You need to provide this (or comment out the figure)

## How to Compile

```bash
pdflatex figures_tables.tex
pdflatex figures_tables.tex   # Run twice for references
```

## Try It

1. Create a simple plot with Python/matplotlib and save as PNG
2. Change the figure width to `0.8\textwidth`
3. Add a third column to the stock table
4. Try removing vertical lines from tables (modern style)
