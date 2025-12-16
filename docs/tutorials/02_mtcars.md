# Working with mtcars

Learn how to create a codebook for the classic mtcars dataset.

---

## Sample Data

For this tutorial, we'll use the `mtcars` dataset from plotnine:

```python
from plotnine.data import mtcars

print(mtcars.head())
```

This dataset contains fuel consumption and 10 aspects of automobile design and performance for 32 automobiles (1973–74 models).

---

## Creating a Codebook

### Basic Usage (Context Manager)

Create a professional codebook with variable descriptions and value labels:

```python
from bookit_df import BookIt
from plotnine.data import mtcars

with BookIt(
    "mtcars Codebook",
    output="mtcars_codebook.pdf",
    author="Your Name"
) as book:
    book.from_dataframe(
        mtcars,
        descriptions={
            "mpg": "Miles per gallon",
            "cyl": "Number of cylinders",
            "disp": "Displacement in cubic inches",
            "hp": "Horsepower",
            "drat": "Rear axle ratio",
            "wt": "Weight in 1000 lbs",
            "qsec": "1/4 mile time",
            "vs": "Engine shape (0 = V-shaped, 1 = straight)",
            "am": "Transmission (0 = automatic, 1 = manual)",
            "gear": "Number of forward gears",
            "carb": "Number of carburetors",
        },
        value_labels={
            "vs": {0: "V-shaped", 1: "Straight"},
            "am": {0: "Automatic", 1: "Manual"},
            "gear": {
                3: "3 gears",
                4: "4 gears",
                5: "5 gears",
            },
            "carb": {
                1: "1 carburetor",
                2: "2 carburetors",
                3: "3 carburetors",
                4: "4 carburetors",
                6: "6 carburetors",
                8: "8 carburetors",
            },
        },
        suppress_numeric_stats=["am", "vs", "cyl", "gear", "carb"],
    )
    book.add_context("mpg", "Fuel economy measure for the 1970s era vehicles.")
# PDF saved automatically on exit!
```

---

## Output

Here's what the generated codebook looks like:

<iframe src="../../assets/mtcars_codebook.pdf" width="100%" height="600px" style="border: 1px solid #ccc; border-radius: 4px;"></iframe>

!!! tip "Can't see the PDF?"
    If the embedded viewer doesn't work, you can [download the PDF directly](../../assets/mtcars_codebook.pdf).

---

## Key Concepts

### Categorical Variables

Two variables in mtcars are categorical but stored as numbers:

| Variable | Values | Meaning |
|----------|--------|---------|
| `vs` | 0, 1 | Engine shape (V-shaped or Straight) |
| `am` | 0, 1 | Transmission type (Automatic or Manual) |
| `cyl` | 4, 6, 8 | Number of cylinders |
| `gear` | 3, 4, 5 | Number of forward gears |
| `carb` | 1, 2, 3, 4, 6, 8 | Number of carburetors |

### Suppressing Numeric Stats

For these categorical variables, we suppress misleading summary statistics:

```python
suppress_numeric_stats=["am", "vs", "cyl", "gear", "carb"]
```

!!! note "Why suppress?"
    Computing mean and standard deviation for categorical variables like `am` 
    (transmission type) would be misleading—the "average" transmission type isn't meaningful.

---

## Next Steps

- See the [Getting Started](01_getting_started.md) tutorial for more details
- Check the [API Reference](../reference/core.md) for all available options