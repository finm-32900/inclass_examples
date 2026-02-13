# 03 - Name Shadowing

## What You Learn

- Python searches `sys.path` **in order** to resolve imports
- The current directory is typically first in `sys.path`
- A local file named `numpy.py` will **shadow** the real `numpy` package
- This is a common source of confusing errors for beginners

## Files

| File | Purpose |
|------|---------|
| `numpy.py` | A local file that shadows the real `numpy` |
| `main.py` | Demonstrates the shadowing problem |

## How to Run

```bash
cd 03_name_shadowing
python main.py
```

You'll see that `import numpy` loads the local `numpy.py` instead of the real numpy library.

## Key Concept

Python resolves imports by searching directories in `sys.path` order. The current directory (or script directory) is usually first, so a local file with the same name as an installed package will "win."

## Try It

- Rename `numpy.py` to something else and run `main.py` again. What happens now?
- Create a file called `os.py` with a print statement. What happens when you `import os`?
