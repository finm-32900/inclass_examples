# 06 - Minimal Beamer Presentation

## What You'll Learn

- The `beamer` document class for presentations
- Creating slides with `frame` environment
- Title slides and table of contents
- Sections for navigation
- Block environments

## Key Concepts

### Beamer vs Articles

| Concept | Article | Beamer |
|---------|---------|--------|
| Document class | `article` | `beamer` |
| Content unit | Pages | Frames (slides) |
| Organization | Sections | Sections (with navigation) |

### Frame Syntax

```latex
\begin{frame}{Slide Title}
    Content goes here.
\end{frame}
```

### Special Frames

**Title slide:**
```latex
\begin{frame}
    \titlepage
\end{frame}
```

**Table of contents:**
```latex
\begin{frame}{Outline}
    \tableofcontents
\end{frame}
```

### Block Environments

Beamer provides three block types:
- `block` - Standard (blue by default)
- `alertblock` - Warning/important (red)
- `exampleblock` - Examples (green)

```latex
\begin{block}{Title}
    Content
\end{block}
```

## How to Compile

```bash
pdflatex minimal_slides.tex
```

## Try It

1. Add a new section with two frames
2. Try `\begin{alertblock}{Warning}` for emphasis
3. Add `\pause` between items to reveal them one at a time
4. Change the theme: add `\usetheme{Madrid}` in the preamble
