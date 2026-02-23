# 01 Syntax Comparison: Pandas vs Polars

Side-by-side comparison showing why Polars syntax is more consistent and less error-prone than pandas.

## What You Learn

- How common operations translate from pandas to polars
- Why polars eliminates pandas pain points (`SettingWithCopyWarning`, `.loc` vs `.iloc`)
- The expression API: `pl.col()`, `pl.when()`, `.over()`
- Method chaining for readable analytical pipelines

## Run

```bash
python pandas_vs_polars.py
```

## Key Concepts

| Concept | pandas | polars |
|---------|--------|--------|
| Select columns | `df[["a","b"]]` | `df.select("a", "b")` |
| Filter rows | `df[df["x"] > 0]` or `df.loc[...]` | `df.filter(pl.col("x") > 0)` |
| Add columns | `df["new"] = ...` | `df.with_columns(...)` |
| Conditional | `np.where(cond, a, b)` | `pl.when(cond).then(a).otherwise(b)` |
| GroupBy + agg | `df.groupby("a").agg(...)` | `df.group_by("a").agg(...)` |
| Window function | `df.groupby("a")["x"].transform(...)` | `pl.col("x").mean().over("a")` |

## Try It

- Convert a pandas script from your own work to polars
- Try triggering `SettingWithCopyWarning` in pandas, then do the same in polars
- Add a new section comparing `.pivot()` in both libraries
