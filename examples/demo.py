"""Test script to generate a sample codebook and verify the package works."""

import polars as pl
import sys
sys.path.insert(0, "/workspaces/book-it/src")

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

print(f"DataFrame shape: {df.shape}")
print(f"Columns: {df.columns}")

# Test context manager with auto-save
output_path = "sample_codebook.pdf"

with BookIt(
    "Sample Survey Codebook",
    output=output_path,
    author="A Statistician",
    include_toc=True,
    include_title_page=True,
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
            "satisfaction": {1: "Very Dissatisfied", 2: "Dissatisfied", 3: "Neutral", 4: "Satisfied", 5: "Very Satisfied"},
        },
        suppress_numeric_stats=["gender", "respondent_id"],  # Hide mean/std for categorical vars
    )
    book.add_context("income", "Values are top-coded at $200,000. All values above this threshold are set to $200,000.")
    book.add_context("satisfaction", "This is a validated 5-point Likert scale measure.")

print(f"\n✓ Codebook saved to: {output_path}")
print(f"✓ Variables documented: {len(book.variables)}")

# Also test explicit save pattern
book2 = BookIt("Test Explicit Save", author="Test Author")
book2.from_dataframe(df, columns=["age", "income"])
book2.save("sample_codebook_explicit.pdf")
print(f"✓ Explicit save also worked!")
