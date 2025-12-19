"""Generate the mtcars codebook PDF for tutorial 02."""

from bookit_df import BookIt
from plotnine.data import mtcars

with BookIt(
    "mtcars Codebook",
    output="docs/assets/mtcars_codebook.pdf",
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
            "carb": "Number of carburetor barrels",
        },
        value_labels={
            "vs": {0: "V-shaped", 1: "Straight"},
            "am": {0: "Automatic", 1: "Manual"},
            "gear": {
                3: "3 gears",
                4: "4 gears",
                5: "5 gears",
            },
            "cyl": {
                4: "4 cylinders",
                6: "6 cylinders",
                8: "8 cylinders",
            },
            "carb": {
                1: "1 barrel",
                2: "2 barrels",
                3: "3 barrels",
                4: "4 barrels",
                6: "6 barrels",
                8: "8 barrels",
            },
        },
        suppress_numeric_stats=["am", "vs"],
    )
    book.add_context("mpg", "Fuel economy measure for the 1970s era vehicles.")

print("Generated: docs/assets/mtcars_codebook.pdf")
