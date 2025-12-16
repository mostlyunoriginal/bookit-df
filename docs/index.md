# BookIt

A Python package for creating PDF codebooks from DataFrames.

---

## What is BookIt?

`bookit` helps you document your data by generating professional PDF codebooks from polars or pandas DataFrames. It's designed as an educational project showcasing Object-Oriented Programming (OOP) principles in Python.

### Key Features

- **DataFrame support** — Works with polars and pandas
- **Automatic statistics** — Computes count, missing, unique, mean, std, min, max
- **Charts** — Bar charts for categorical variables, histograms for numeric
- **Value labels** — Document coded values (e.g., `1 = "Male"`)
- **Context manager** — Auto-save on exit with `with BookIt(...) as book:`

---

## Quick Example

```python
import polars as pl
from bookit_df import BookIt

df = pl.read_csv("survey_data.csv")

# Context manager with auto-save
with BookIt("Survey Codebook", output="codebook.pdf", author="Research Team") as book:
    book.from_dataframe(
        df,
        descriptions={
            "age": "Respondent's age in years",
            "income": "Annual household income (USD)",
        },
        value_labels={
            "gender": {1: "Male", 2: "Female"}
        }
    )
# PDF saved automatically!
```

---

## Installation

```bash
pip install book-it
```

### Optional Dependencies

```bash
# polars support (recommended)
pip install bookit-df[polars]

# pandas support
pip install bookit-df[pandas]
```

---

## Next Steps

- **[Tutorials](tutorials/index.md)** — Step-by-step guides
- **[API Reference](reference/core.md)** — Complete documentation

---

## Links

- [GitHub Repository](https://github.com/mostlyunoriginal/book-it)
