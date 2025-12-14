"""BookIt: Main class for creating codebooks from DataFrames."""

from pathlib import Path
from typing import Any

from .config import CodebookConfig
from .stats import compute_stats, get_dtype_string
from .variable import Variable


class BookIt:
    """Create a codebook documenting a DataFrame's variables.
    
    BookIt can be used as a context manager (auto-saves on exit if output path
    is provided) or with explicit .save() calls.
    
    Attributes:
        title: Title of the codebook.
        config: Configuration options for the codebook.
        variables: List of Variable objects in the codebook.
    
    Example (context manager with auto-save):
        >>> with BookIt("Survey Codebook", output="codebook.pdf") as book:
        ...     book.from_dataframe(df)
        # Saves automatically on exit
        
    Example (explicit save):
        >>> book = BookIt("Survey Codebook")
        >>> book.from_dataframe(df)
        >>> book.save("codebook.pdf")
    """
    
    def __init__(
        self,
        title: str = "Codebook",
        output: str | Path | None = None,
        *,
        author: str = "",
        date: str | None = None,
        include_toc: bool = True,
        include_title_page: bool = True,
        include_stats: bool = True,
        config: CodebookConfig | None = None,
    ) -> None:
        """Initialize a new BookIt instance.
        
        Args:
            title: Title of the codebook.
            output: Output file path. If provided and used as context manager,
                    the codebook will auto-save on exit.
            author: Author name(s).
            date: Date string. Defaults to today's date.
            include_toc: Whether to include table of contents.
            include_title_page: Whether to include title page.
            include_stats: Whether to include summary statistics.
            config: Full CodebookConfig object. If provided, overrides
                    individual settings above.
        """
        # Use provided config or build from individual args
        if config is not None:
            self.config = config
        else:
            kwargs = {
                "title": title,
                "author": author,
                "include_toc": include_toc,
                "include_title_page": include_title_page,
                "include_stats": include_stats,
            }
            if date is not None:
                kwargs["date"] = date
            self.config = CodebookConfig(**kwargs)
        
        self.title = title
        self.output = Path(output) if output else None
        self.variables: list[Variable] = []
        self._saved = False
    
    def from_dataframe(
        self,
        df: Any,
        columns: list[str] | None = None,
        descriptions: dict[str, str] | None = None,
        value_labels: dict[str, dict[Any, str]] | None = None,
        suppress_numeric_stats: list[str] | None = None,
    ) -> "BookIt":
        """Import variables from a DataFrame.
        
        Args:
            df: A polars or pandas DataFrame.
            columns: List of column names to include. Defaults to all columns.
            descriptions: Dict mapping column names to descriptions.
            value_labels: Dict mapping column names to value label dicts.
            suppress_numeric_stats: List of column names for which to hide
                numeric statistics (mean, std, min, max) in output.
            
        Returns:
            self, for method chaining.
            
        Example:
            >>> book.from_dataframe(
            ...     df,
            ...     columns=["age", "income"],
            ...     descriptions={"age": "Respondent age in years"},
            ...     suppress_numeric_stats=["age"]  # Hide mean/std for age
            ... )
        """
        descriptions = descriptions or {}
        value_labels = value_labels or {}
        suppress_numeric_stats = suppress_numeric_stats or []
        
        # Get column list
        module = type(df).__module__
        if module.startswith("polars"):
            all_columns = df.columns
        elif module.startswith("pandas"):
            all_columns = list(df.columns)
        else:
            raise TypeError(
                f"Unsupported DataFrame type: {type(df)}. "
                "Expected polars.DataFrame or pandas.DataFrame."
            )
        
        columns_to_process = columns if columns else all_columns
        
        for col_name in columns_to_process:
            if col_name not in all_columns:
                raise ValueError(f"Column '{col_name}' not found in DataFrame.")
            
            # Get the series/column
            series = df[col_name]
            
            # Create Variable
            var = Variable(
                name=col_name,
                description=descriptions.get(col_name, ""),
                dtype=get_dtype_string(series),
                values=value_labels.get(col_name, {}),
                suppress_numeric_stats=(col_name in suppress_numeric_stats),
            )
            
            # Compute statistics if enabled
            if self.config.include_stats:
                var.stats = compute_stats(series)
            
            self.variables.append(var)
        
        return self
    
    def add_variable(
        self,
        name: str,
        description: str = "",
        dtype: str = "",
        values: dict[Any, str] | None = None,
        context: str = "",
        suppress_numeric_stats: bool = False,
    ) -> "BookIt":
        """Manually add a variable to the codebook.
        
        Args:
            name: Variable name.
            description: Human-readable description.
            dtype: Data type string.
            values: Value labels for categorical variables.
            context: Additional contextual notes.
            suppress_numeric_stats: If True, hide mean/std/min/max in output.
            
        Returns:
            self, for method chaining.
        """
        var = Variable(
            name=name,
            description=description,
            dtype=dtype,
            values=values or {},
            context=context,
            suppress_numeric_stats=suppress_numeric_stats,
        )
        self.variables.append(var)
        return self
    
    def add_context(self, variable_name: str, text: str) -> "BookIt":
        """Add contextual notes to a variable.
        
        Args:
            variable_name: Name of the variable to add context to.
            text: Contextual text to add.
            
        Returns:
            self, for method chaining.
            
        Raises:
            ValueError: If variable is not found.
        """
        for var in self.variables:
            if var.name == variable_name:
                var.context = text
                return self
        
        raise ValueError(f"Variable '{variable_name}' not found in codebook.")
    
    def save(self, path: str | Path | None = None) -> None:
        """Save the codebook to a file.
        
        Args:
            path: Output file path. Uses the path from __init__ if not provided.
            
        Raises:
            ValueError: If no output path is available.
        """
        output_path = Path(path) if path else self.output
        
        if output_path is None:
            raise ValueError(
                "No output path specified. Provide a path to save() or set "
                "output in BookIt()."
            )
        
        # Import renderer here to avoid circular imports
        from .renderers.pdf import PDFRenderer
        
        renderer = PDFRenderer(self)
        renderer.render(output_path)
        self._saved = True
    
    def __enter__(self) -> "BookIt":
        """Enter context manager."""
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager, auto-saving if output path was set."""
        if exc_type is None and self.output is not None and not self._saved:
            self.save()
    
    def __repr__(self) -> str:
        """Concise representation for debugging."""
        return (
            f"BookIt(title={self.title!r}, "
            f"variables={len(self.variables)})"
        )
