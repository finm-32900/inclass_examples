# 03 - Mathematics and Lists

## What You'll Learn

- Inline math with `$...$`
- Display math with `\[...\]`
- Numbered equations with `equation` environment
- Common mathematical notation
- Numbered and bulleted lists
- Text formatting

## Key Concepts

### Math Modes

| Syntax | Result | Use Case |
|--------|--------|----------|
| `$...$` | Inline | Math within text |
| `\[...\]` | Display | Standalone, centered |
| `\begin{equation}` | Numbered | Equations you'll reference |

### Common Math Commands

| Command | Output | Description |
|---------|--------|-------------|
| `\frac{a}{b}` | a/b | Fractions |
| `x^2` | x squared | Superscript |
| `x_i` | x sub i | Subscript |
| `\sqrt{x}` | square root | Square root |
| `\sum_{i=1}^{n}` | summation | Sum notation |
| `\int_a^b` | integral | Integration |
| `\alpha, \beta` | Greek | Greek letters |

### Cross-References

1. Label an equation: `\label{eq:name}`
2. Reference it: `Equation~\ref{eq:name}`

The tilde `~` creates a non-breaking space.

### Lists

- `enumerate` - Numbered lists
- `itemize` - Bullet points
- Each item starts with `\item`

## How to Compile

```bash
pdflatex math_lists.tex
```

Run twice if references show as "??" - LaTeX needs two passes.

## Try It

1. Add the Black-Scholes formula: $C = S_0 N(d_1) - K e^{-rT} N(d_2)$
2. Create a nested list (a list inside a list item)
3. Add a multi-line equation using the `align` environment
