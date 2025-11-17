**Purpose**
- Document the project's layered code quality philosophy and tooling stack, centered on Ruff (local linting/formatting), Checkov (security/IaC scanning), and Sonar (CI-based deep analysis), with guidance on local workflows, pre-commit hooks, and CI integration.

**Main Topics**
- Quality philosophy: fast local feedback for developers, security-focused scanning for infrastructure and Docker, and deeper CI analysis for long-term maintainability.
- Three-tool stack: Ruff for linting/formatting, Checkov for IaC and Dockerfile security, and Sonar for bugs, code smells, and vulnerabilities beyond Ruff's rule set.
- Local execution patterns: using `uv run lint` (Ruff wrapper) for day-to-day linting/formatting, and `uv run checkov` (or equivalent) for ad hoc security scans.
- Automated checks: pre-commit hook running `uv run lint` for fast local checks, plus CI pipelines that run Ruff, Checkov, Sonar, and pytest on each PR.
- Roles and responsibilities: clarify what each tool is responsible for (style, static analysis, security, complexity) and how they complement each other.

**Opinions / Guidelines**
- Use Ruff as the unified local tool replacing separate Black/Isort/Flake8 stacks; rely on `uv run lint` instead of individual formatter commands.
- Treat Checkov as the primary tool for scanning Dockerfile and IaC for misconfigurations (root users, open ports, missing best practices).
- Rely on Sonar (SonarCloud or SonarQube) in CI for deeper language-aware analysis, including injection risks, complex control flow, and maintainability.
- Keep pre-commit hooks fast: run only Ruff (via `uv run lint`) locally, while CI runs the more expensive Checkov and Sonar checks.
- Enforce that PRs only merge when all quality gates pass (Ruff, Checkov, Sonar, pytest), making failures blocking rather than advisory.

**Assumptions**
- Ruff configuration is defined in `pyproject.toml` and is wired to the `lint` script used by `uv run lint`.
- Checkov is installed as a development dependency and wired to a script or documented `uv` invocation.
- Sonar is configured in CI (via SonarCloud or SonarQube) even though the doc does not show the actual configuration file.
- Pre-commit hooks are installed via `uv run mcp-setup`, which sets up a hook that runs `uv run lint` on staged Python files.
- CI pipelines (likely under `.github/workflows/`) run pytest alongside static analysis tools as part of the default PR checks.

**Staleness Indicators**
- The doc references Sonar usage but not a concrete `sonar-project.properties` or CI workflow, which may drift as configuration evolves.
- Checkov examples emphasize manual invocation; actual CI wiring may change (e.g., different paths, additional policies).
- Tool versions for Ruff and Checkov are not pinned in the text, so the doc can become misleading if versions in `pyproject.toml` change.
- Pre-commit configuration may evolve (additional hooks, different commands), requiring updates to stay aligned with `.pre-commit-config.yaml`.
- No mention of additional tools (e.g., mypy) that might be introduced later, potentially shifting the "three-tool" narrative.

**Tags**
- tooling, linting, ruff, checkov, sonar, code-quality, security, ci, pre-commit, static-analysis, iac

**Preliminary Target Docs**
- Recommend keeping this as a standalone `docs/linting-guide.md` because it articulates the philosophy and rationale behind the chosen tooling stack.
- A condensed summary of the stack and expectations can live in `README.md`'s Code Quality section, linking back here for full detail.
- Command-level usage examples should coordinate with `docs/command-reference.md` and any `docs/git-workflow.md` CI documentation.

**Red Flags**
- Overlap with `README.md` Code Quality section, which already explains Ruff workflows and pre-commit; duplication increases maintenance cost.
- Overlap with `STYLE_8` tooling guidance, which also discusses Ruff and Checkov and introduces mypy, creating potential confusion about required tools.
- Overlap with `docs/to_integrate/command-reference.md` for specific `uv run lint` and `uv run ruff format .` commands; sources must not diverge.
- Sonar usage is described at a high level but the repository may not yet contain explicit Sonar configuration files, leading to gaps between docs and reality.
- Checkov is described as running in CI, but no specific workflow or command is called out; must be aligned with actual CI config (e.g., GitHub Actions).
- Pre-commit hook design is described as Ruff-only; if additional hooks (e.g., Checkov, mypy) are later added, this guide must be updated.
- Mypy is emphasized in `STYLE_8` but absent here, making it unclear whether type checking is part of the official quality gate.
- No explicit mention of version constraints for Ruff/Checkov/Sonar may cause discrepancies with `pyproject.toml` and CI configs.
- Ruff configuration details (line length, rule sets) are not surfaced; developers must discover them in `pyproject.toml`.
- Pytest's role in the quality gate is acknowledged but not tied to specific docs (`docs/TEST.md`, `docs/TESTING_ARCHITECTURE.md`), which may fragment the testing narrative.

**References**
- `docs/to_integrate/linting-guide.md` (source of philosophy and workflow details).
- `README.md` (overlapping Code Quality overview).
- `working/phase1/summaries/docs/to_integrate/STYLE_8.summary.md` (related tooling guidance and mypy emphasis).
- `docs/to_integrate/command-reference.md` (overlapping command examples for Ruff and Checkov).
- `pyproject.toml` (Ruff and Checkov configuration and script definitions).
- `.pre-commit-config.yaml` (hook configuration wired to `uv run lint`).
- `docs/to_integrate/git-workflow.md` (context for CI and PR workflows).
- `docs/TEST.md` and `docs/TESTING_ARCHITECTURE.md` (pytest integration and testing tiers).
- `Dockerfile` (Checkov scan target for Docker security guidance).
