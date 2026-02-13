# 02 - Package Directory

## What You Learn

- A **package** is a directory containing an `__init__.py` file
- You import a package the same way you import a module
- The code in `__init__.py` runs when the package is imported

## Files

```
02_package_directory/
├── main.py
└── mypackage/
    └── __init__.py
```

| File | Purpose |
|------|---------|
| `mypackage/__init__.py` | Package init that defines `say_hello()` |
| `main.py` | Imports and uses the package |

## How to Run

```bash
cd 02_package_directory
python main.py
```

## Key Concept

In `01_simple_module`, `mypackage` was a single file (`mypackage.py`). Here, `mypackage` is a **directory** with `__init__.py`. From the caller's perspective, the import looks identical:

```python
import mypackage
mypackage.say_hello()
```

## Try It

- What happens if you delete `__init__.py`? Can you still import `mypackage`?
- Add a second function to `__init__.py` and call it from `main.py`
