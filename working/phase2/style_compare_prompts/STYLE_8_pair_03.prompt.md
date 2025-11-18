You are updating `docs/code-style-guide.md`.

The following content comes from `docs/to_integrate/STYLE_8.md`.
Ensure that all substantive concepts in this slice are represented in `docs/code-style-guide.md`.
You do not need to copy text verbatim, but you should add or adjust sections in `docs/code-style-guide.md`
so that no important guidance from this slice is lost, resolving any conflicts in favor of the current ADRs,
`pyproject.toml`, and the existing codebase behavior.

--- SOURCE SECTION START ---
# STYLE_8 section pair 3

This file contains one or two `##` sections from docs/to_integrate/STYLE_8.md.

## 🤖 Automated Tooling & Enforcement

Our development workflow is enforced by a combination of tools managed by `uv` and `pre-commit`.

### 1\. Linting & Formatting with Ruff

`ruff` handles both linting (`ruff check`) and formatting (`ruff format`). It's configured in our `pyproject.toml` file.

### 2\. Type Checking with mypy

To catch type-related bugs before runtime, we use **`mypy`**, the standard for static type checking in Python. This was the missing piece in our previous setup.

* Run it via: `uv run typecheck`

### 3\. Security Scanning with Checkov

We continue to use `checkov` to scan our codebase and Infrastructure-as-Code (IaC) files for security vulnerabilities.

* Run it via: `uv run security`

### 4\. Running Tasks with uv

We define all our scripts in `pyproject.toml` under the `[tool.uv.scripts]` section. This provides a single interface for running all our quality checks.

**Example `pyproject.toml` configuration:**

```toml
[tool.uv.scripts]
# Run all formatters
format = "ruff format ."

# Run all non-fixing checks
lint = [
    "ruff check .",
    "uv run typecheck",
    "uv run security",
]

# Individual tasks
typecheck = "mypy ."
security = "checkov --directory ."
```

> **Workflow:**
>
>   * Run `uv run format` to fix formatting.
>   * Run `uv run lint` to check for all linting, type, and security errors.

### 5\. Git Hooks with pre-commit

To ensure no bad code is ever committed, our `pre-commit` hook runs our checks on staged files. The hook is configured to run the individual tasks for maximum speed and efficiency.

Here is the recommended `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.5 # Use the latest ruff version
    hooks:
    -   id: ruff-format
        args: [ "--check" ] # Use --check to fail on unformatted files
    -   id: ruff
        args: [ "--fix", "--exit-non-zero-on-fix" ]

-   repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0 # Use the latest mypy version
    hooks:
    -   id: mypy
        args: [ "--strict" ] # Enforce strict type checking
        additional_dependencies: [
            # Add your project's type-stub dependencies here
            # e.g., "pandas-stubs"
        ]

-   repo: https://github.com/bridgecrewio/checkov
    rev: 3.2.144 # Use the latest checkov version
    hooks:
    -   id: checkov
        args: [ "--quiet" ] # Add any other flags you use
```

> **Note:** The user's original request mentioned the pre-commit hook runs `uv run lint`. While possible (using a `local` hook), the setup above is the community-standard way to use `pre-commit`. It's generally faster as it only runs tools on the files that have changed.
--- SOURCE SECTION END ---
