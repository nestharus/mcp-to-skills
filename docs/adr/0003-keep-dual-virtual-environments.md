# ADR 0003: Keep Dual Virtual Environments (.venv and .venv2)

## Context

The repository is used from both WSL (Linux) and Windows host environments. `.venv` is used by WSL tooling (including `uv`), while `.venv2` is used by Windows-based IDEs. Both environments are active and removing either risks breaking established workflows.

## Decision

Retain both virtual environments:

- `.venv` remains the canonical environment for WSL and CLI usage (e.g., `uv run [ELIDED]`).
- `.venv2` remains available for Windows IDE integration.
- Documentation and agent guidance should prefer CLI workflows that do not hardcode interpreter paths, so both environments can coexist.

## Consequences

- Supports hybrid development setups (Windows host + WSL).
- Adds some complexity to environment documentation; mitigated via clear setup instructions.
- Avoids accidentally breaking either environment when updating tooling.

## References

- `docs/development-setup.md` (environment setup)
- `AGENTS.md` (agent-specific guidance)
