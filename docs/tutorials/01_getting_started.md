# Getting Started

Learn how to create your first codebook with BookIt.

---

## Sample Data

For this tutorial, we'll create a sample survey dataset:

```python
import polars as pl

df = pl.DataFrame({
    "respondent_id": range(1, 101),
    "age": [25, 30, 35, 40, 45, None, 28, 33, 38, 43] * 10,
    "gender": [1, 2, 1, 2, 1, 2, 1, 2, None, 1] * 10,
    "education": ["HS", "BA", "MA", "PhD", "HS", "BA", "MA", "PhD", "HS", "BA"] * 10,
    "income": [45000.0, 55000.0, 75000.0, 95000.0, 35000.0, None, 65000.0, 85000.0, 40000.0, 60000.0] * 10,
    "satisfaction": [3, 4, 5, 2, 4, 3, 5, 4, 3, None] * 10,
})
```

---

## Creating a Codebook

### Basic Usage (Context Manager)

The easiest way to create a codebook is with a context manager:

```python
from bookit_df import BookIt

with BookIt(
    "Sample Survey Codebook",
    output="codebook.pdf",
    author="Research Team"
) as book:
    book.from_dataframe(
        df,
        descriptions={
            "respondent_id": "Unique identifier for each survey respondent",
            "age": "Respondent's age in years at time of survey",
            "gender": "Self-reported gender identity",
            "education": "Highest level of education completed",
            "income": "Annual household income in USD",
            "satisfaction": "Overall life satisfaction rating (1-5 scale)",
        },
        value_labels={
            "gender": {1: "Male", 2: "Female"},
            "satisfaction": {
                1: "Very Dissatisfied",
                2: "Dissatisfied", 
                3: "Neutral",
                4: "Satisfied",
                5: "Very Satisfied"
            },
        },
        suppress_numeric_stats=["gender", "respondent_id"],
    )
    book.add_context("income", "Values are top-coded at $200,000.")
# PDF saved automatically on exit!
```

---

## Output

Here's what the generated codebook looks like:

<iframe src="../../assets/sample_codebook.pdf" width="100%" height="600px" style="border: 1px solid #ccc; border-radius: 4px;"></iframe>

!!! tip "Can't see the PDF?"
    If the embedded viewer doesn't work, you can [download the PDF directly](../../assets/sample_codebook.pdf).

---

## Key Concepts

### Descriptions

Descriptions explain what each variable represents:

```python
descriptions={
    "age": "Respondent's age in years",
}
```

### Value Labels

For coded categorical variables, provide human-readable labels:

```python
value_labels={
    "gender": {1: "Male", 2: "Female"},
}
```

### Suppressing Numeric Stats

For categorical variables stored as numbers (like `gender`), suppress mean/std/min/max:

```python
suppress_numeric_stats=["gender", "satisfaction"]
```

### Context Notes

Add additional notes to specific variables:

```python
book.add_context("income", "Top-coded at $200,000")
```

---

## Next Steps

- See the [API Reference](../reference/core.md) for all available options
