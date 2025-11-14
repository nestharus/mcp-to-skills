# Agent Notes

- This repository may include multiple virtual environment directories. `.venv` corresponds to the Linux (WSL) toolchain, while `.venv2` points to the Windows interpreter that the host IDE uses. Windows paths typically reference `.venv2`, and WSL tooling (including `uv run ...`) points at `.venv`.
- Treat both directories as intentional. Do not delete or rename them, and assume either may contain valid interpreter state depending on which side (Windows vs. WSL) last executed `uv`.
- When updating documentation or scripts, prefer CLI workflows (`uv run ...`) that do not assume a specific interpreter path so both environments continue to work without extra steps.
