# 01 - Sphinx Quickstart

## What You'll Learn

- How to bootstrap a Sphinx documentation project using `sphinx-quickstart`
- The files and directories Sphinx creates
- How to build HTML documentation with `make html`
- The default project structure: `conf.py`, `index.rst`, `Makefile`

## Key Concepts

### What is Sphinx?

Sphinx is a documentation generator that converts reStructuredText (or Markdown)
into HTML, PDF, and other formats. It is the standard tool for Python project
documentation and is used in all course projects.

### The `sphinx-quickstart` Command

`sphinx-quickstart` is an interactive CLI that creates the scaffolding for a new
Sphinx project. It generates:

- `conf.py` — Configuration file (project name, extensions, theme)
- `index.rst` — Root document (table of contents)
- `Makefile` / `make.bat` — Build shortcuts
- `_build/` — Output directory (created on first build)
- `_static/` and `_templates/` — Directories for custom assets

## How to Run

1. Create and enter a working directory:

   ```bash
   mkdir my_sphinx_project
   cd my_sphinx_project
   ```

2. Run the quickstart wizard:

   ```bash
   sphinx-quickstart
   ```

3. When prompted, use these responses:

   | Prompt | Suggested Response |
   |--------|--------------------|
   | Separate source and build directories | `n` (keep it simple) |
   | Project name | `My First Docs` |
   | Author name(s) | Your name |
   | Project release | `0.1` |
   | Project language | `en` (press Enter for default) |

4. Build the HTML documentation:

   ```bash
   make html
   ```

   On Windows without Make:

   ```bash
   sphinx-build -b html . _build/html
   ```

5. Open the result in your browser:

   ```bash
   open _build/html/index.html
   ```

## What You Should See

After the quickstart, your directory looks like this:

```
my_sphinx_project/
├── _build/          # Generated HTML output (after building)
├── _static/         # Custom CSS, images, etc.
├── _templates/      # Custom Jinja2 templates
├── conf.py          # Sphinx configuration
├── index.rst        # Root document with toctree
├── Makefile         # Build shortcut (Unix)
└── make.bat         # Build shortcut (Windows)
```

The generated site uses the **alabaster** theme (Sphinx's default).

## Try It

1. Open `conf.py` and find the `html_theme` setting. What is the default?
2. Edit `index.rst` to add a line of text below the heading. Rebuild and refresh.
3. Run `make clean` to remove the build output, then `make html` to rebuild.
4. Look at the `sample_module.py` file in this directory. In the next example,
   you will learn how to automatically generate documentation from its docstrings.
