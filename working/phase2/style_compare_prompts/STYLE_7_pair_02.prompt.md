You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_7.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_7 section pair 2

This file contains one or two `##` sections from docs/to_integrate/STYLE_7.md.

## Error Handling

### Use Custom Error Classes

In Python, it's best practice to create custom exceptions by inheriting from the built-in `Exception` class or a more specific exception, like `ValueError` or `IOError`.

```python
# ✅ Good
class ValidationError(ValueError):
    """Indicates an error during data validation."""
    # Inheriting from a specific built-in exception like ValueError
    # is often better than using the generic Exception class.
    pass

# You can add more logic inside if needed
class NetworkError(IOError):
    """Indicates a failure during a network request."""
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

# Use 'raise' to throw an exception
raise ValidationError('Invalid email format')


# ❌ Bad
# Using a generic exception provides no specific context for handling.
raise Exception('Invalid email format')
```

-----

### Handle Errors Appropriately

Python's `try[ELIDED]except` block is designed to catch specific exceptions, which is cleaner than using `if/else` checks inside a generic `catch` block.

```python
# ✅ Good
# Use multiple, specific `except` blocks to handle different errors.
try:
    # Assume fetch_data and process_data are defined, possibly as async
    data = await fetch_data()
    return process_data(data)
except ValidationError as e:
    # Handle validation error (e.g., log it, return a 400 response)
    print(f"Validation failed: {e}")
    return None
except NetworkError as e:
    # Handle network error (e.g., retry or return a 503 response)
    print(f"Network error, status {e.status_code}: {e}")
    return None
except Exception as e:
    # Let any other unexpected errors propagate up.
    # Logging the exception here is good practice.
    print(f"An unexpected error occurred: {e}")
    raise  # Re-raises the caught exception

# ❌ Bad
# A broad 'except' that silences the error is dangerous.
try:
    data = await fetch_data()
    return process_data(data)
except Exception as e:
    # This is a "Pokémon exception" (gotta catch 'em all!).
    # It catches *all* exceptions, hides the error, and
    # returns a vague 'None', making debugging very difficult.
    print(e)
    return None
```
--- SOURCE SECTION END ---
