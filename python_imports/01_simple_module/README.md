# 01 - Simple Module Import

## What You Learn

- A single `.py` file is a **module**
- You can import it by filename (without the `.py` extension)
- Python looks in the current directory first when resolving imports

## Files

| File | Purpose |
|------|---------|
| `mypackage.py` | A module that defines `say_hello()` |
| `main.py` | Imports and uses the module |

## How to Run

```bash
cd 01_simple_module
python main.py
```

## Try It

- Rename `mypackage.py` to something else and update the import. Does it still work?
- What happens if you try to import a file that doesn't exist?
