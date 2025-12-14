"""Statistics computation for DataFrames (polars and pandas)."""

from typing import Any

from .variable import VariableStats


def compute_stats(series: Any) -> VariableStats:
    """Compute summary statistics from a DataFrame column.
    
    Supports both polars Series and pandas Series. Automatically detects
    the type and dispatches to the appropriate implementation.
    
    Args:
        series: A polars Series or pandas Series.
        
    Returns:
        VariableStats with computed statistics.
        
    Example:
        >>> import polars as pl
        >>> s = pl.Series("age", [25, 30, 35, None, 40])
        >>> stats = compute_stats(s)
        >>> stats.count
        5
        >>> stats.missing
        1
    """
    # Detect series type by module name (duck typing)
    module = type(series).__module__
    
    if module.startswith("polars"):
        return _compute_stats_polars(series)
    elif module.startswith("pandas"):
        return _compute_stats_pandas(series)
    else:
        raise TypeError(
            f"Unsupported series type: {type(series)}. "
            "Expected polars.Series or pandas.Series."
        )


def _compute_stats_polars(series: Any) -> VariableStats:
    """Compute statistics for a polars Series."""
    import polars as pl
    
    count = len(series)
    missing = series.null_count()
    unique = series.n_unique()
    
    # Initialize stats
    stats = VariableStats(
        count=count,
        missing=missing,
        unique=unique,
    )
    
    # Numeric statistics
    if series.dtype.is_numeric():
        stats.mean = series.mean()
        stats.std = series.std()
        stats.min = series.min()
        stats.max = series.max()
    else:
        # For non-numeric, still get min/max if orderable
        try:
            stats.min = series.min()
            stats.max = series.max()
        except Exception:
            pass
    
    # Top values for categorical-like columns
    if unique <= 20 or not series.dtype.is_numeric():
        value_counts = series.drop_nulls().value_counts().sort("count", descending=True)
        top_n = min(10, len(value_counts))
        if top_n > 0:
            # Get column names - polars value_counts returns the series name as first column
            col_name = series.name if series.name else "value"
            stats.top_values = [
                (row[col_name], row["count"])
                for row in value_counts.head(top_n).iter_rows(named=True)
            ]
    
    return stats


def _compute_stats_pandas(series: Any) -> VariableStats:
    """Compute statistics for a pandas Series."""
    import pandas as pd
    import numpy as np
    
    count = len(series)
    missing = int(series.isna().sum())
    unique = series.nunique(dropna=True)
    
    stats = VariableStats(
        count=count,
        missing=missing,
        unique=unique,
    )
    
    # Numeric statistics
    if pd.api.types.is_numeric_dtype(series):
        stats.mean = float(series.mean()) if not pd.isna(series.mean()) else None
        stats.std = float(series.std()) if not pd.isna(series.std()) else None
        stats.min = series.min() if not pd.isna(series.min()) else None
        stats.max = series.max() if not pd.isna(series.max()) else None
    else:
        # For non-numeric, try to get min/max
        try:
            stats.min = series.min()
            stats.max = series.max()
        except Exception:
            pass
    
    # Top values for categorical-like columns
    if unique <= 20 or not pd.api.types.is_numeric_dtype(series):
        value_counts = series.dropna().value_counts().head(10)
        stats.top_values = list(value_counts.items())
    
    return stats


def get_dtype_string(series: Any) -> str:
    """Get a human-readable dtype string from a series.
    
    Args:
        series: A polars Series or pandas Series.
        
    Returns:
        Human-readable data type string.
    """
    module = type(series).__module__
    
    if module.startswith("polars"):
        return str(series.dtype)
    elif module.startswith("pandas"):
        return str(series.dtype)
    else:
        return "unknown"
