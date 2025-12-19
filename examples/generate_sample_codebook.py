"""Generate the sample survey codebook PDF for tutorial 01."""

import polars as pl

from bookit_df import BookIt

# Create a sample DataFrame with various data types
df = pl.DataFrame({
    "respondent_id": range(1, 101),
    "age": [25, 30, 35, 40, 45, None, 28, 33, 38, 43] * 10,
    "gender": [1, 2, 1, 2, 1, 2, 1, 2, None, 1] * 10,
    "education": ["HS", "BA", "MA", "PhD", "HS", "BA", "MA", "PhD", "HS", "BA"] * 10,
    "income": [45000.0, 55000.0, 75000.0, 95000.0, 35000.0, None, 65000.0, 85000.0, 40000.0, 60000.0] * 10,
    "satisfaction": [3, 4, 5, 2, 4, 3, 5, 4, 3, None] * 10,
})

with BookIt(
    "Sample Survey Codebook",
    output="docs/assets/sample_codebook.pdf",
    author="Research Team",
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
                5: "Very Satisfied",
            },
        },
        suppress_numeric_stats=["gender", "respondent_id"],
    )
    book.add_context("income", "Values are top-coded at $200,000.")

print("Generated: docs/assets/sample_codebook.pdf")
