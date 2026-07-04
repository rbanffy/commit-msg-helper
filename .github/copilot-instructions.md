# Copilot Instructions — commit-msg-helper

This repository is a pre-commit plugin written in Python. It exposes Git hooks
as console script entry points defined in `pyproject.toml`. Follow the
conventions below when adding or modifying code.

---

## Project structure

```
src/commit_msg_helper/
    __init__.py       — package init, keep empty
    cli.py            — hook entry points only; no business logic
    helpers.py        — pure helper functions and compiled regexes
tests/
    test_helpers.py   — unit tests for helpers.py
pyproject.toml        — build config, entry points, dev dependencies
.pre-commit-hooks.yaml — hook definitions consumed by pre-commit
```

Keep `cli.py` thin: it calls helpers, prints diagnostics to stderr, and returns
an integer exit code. All logic belongs in `helpers.py`.

---

## Entry points (hooks)

Each hook is a function in `cli.py` that:

- Takes no arguments (pre-commit passes context via the environment or stdin,
  not as CLI args to these functions).
- Returns `int` — `0` for success (allow commit), `1` for failure (block commit).
- Prints human-readable diagnostics to `sys.stderr`, never to `sys.stdout`.
- Is registered in `pyproject.toml` under `[project.scripts]`.

```python
# pyproject.toml
[project.scripts]
my-hook = "commit_msg_helper.cli:my_hook"
```

```python
# cli.py
def my_hook() -> int:
    """Pre-commit hook entry point. Returns 0 to allow, 1 to block."""
    ...
```

---

## Hook types and how pre-commit passes data

| Hook stage       | How data arrives                        | `pass_filenames` |
|------------------|-----------------------------------------|------------------|
| `pre-commit`     | Staged file paths as CLI arguments      | `true` (default) |
| `commit-msg`     | Path to the commit message file via `$1`/`sys.argv[1]` | `false` |
| `prepare-commit-msg` | Same as commit-msg                  | `false`          |
| Branch/env hooks | Environment variables or `git` commands | `false`          |

For hooks that do not operate on files (e.g. branch name checks), always set
`pass_filenames: false` and `always_run: true` in the hook definition.

---

## `.pre-commit-hooks.yaml`

This file is what pre-commit reads when users reference this repo. It must exist
at the repository root. Example:

```yaml
- id: branch-needs-jira
  name: Branch name includes Jira ticket
  language: python
  entry: branch-needs-jira
  pass_filenames: false
  always_run: true
```

**`language`** should be `python` (not `system`) in `.pre-commit-hooks.yaml` so
pre-commit manages an isolated, reproducible environment for consumers of this
hook. Use `language: system` only in the local `.pre-commit-config.yaml` for
development purposes.

---

## Helper functions

- Place all logic in `helpers.py`.
- Compile regexes at module level as constants (e.g. `JIRA_TICKET_RE`).
- Functions that check a condition should be named `is_*` and return `bool`.
- Functions that extract a value should be named `get_*` and return the value
  or `None`.
- Functions that call `subprocess` should isolate the call and return `None`
  (not raise) on expected failures such as `CalledProcessError`.

```python
# Good
JIRA_TICKET_RE = re.compile(r"^[A-Z]{2,}-\d+")

def is_jira_in_branch_name(branch: str) -> bool: ...
def get_jira_ticket_from_branch(branch: str) -> str | None: ...
def get_current_branch() -> str | None: ...  # returns None on detached HEAD
```

---

## Safe / exempt branches

The set of branches exempt from Jira ticket requirements is `SAFE_BRANCHES` in
`helpers.py`:

```python
SAFE_BRANCHES = {"main", "master", "develop"}
```

When adding new hooks that also need to exempt these branches, import and reuse
`SAFE_BRANCHES` and `is_safe_branch()` — do not duplicate the set.

---

## Git interaction

Use `subprocess.check_output` with `stderr=subprocess.DEVNULL` to suppress Git
noise. Always pass commands as a list (never a string) to avoid shell injection.

```python
# Good
subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"], stderr=subprocess.DEVNULL)

# Bad — shell=True is a security risk
subprocess.check_output("git symbolic-ref --short HEAD", shell=True)
```

For reading the commit message file (commit-msg hooks), read the path from
`sys.argv[1]` and open it with `pathlib.Path`:

```python
import sys
from pathlib import Path

def message_needs_jira() -> int:
    msg = Path(sys.argv[1]).read_text().strip()
    ...
```

---

## Testing

- Tests live in `tests/` and use `pytest`.
- Test helper functions directly; do not test `cli.py` entry points via
  subprocess unless testing the actual exit code is necessary.
- Group tests in classes named `Test<FunctionName>`.
- Cover: valid inputs, invalid inputs, edge cases (empty string, detached HEAD,
  safe branches).
- Run tests with `uv run pytest`.

---

## Code style

- Linter/formatter: `ruff` (configured via `pyproject.toml` or `ruff.toml`).
- Minimum Python version: 3.12 (see `requires-python` in `pyproject.toml`).
  - Use `str | None` union syntax instead of `Optional[str]`.
- No `print` to stdout in production code — only `sys.stderr`.
- No bare `except`; catch specific exceptions (`subprocess.CalledProcessError`,
  `OSError`, etc.).
- Try to make functions pure (no side effects) and testable in isolation. Avoid global state.

---

## Adding a new hook — checklist

1. Add the helper logic to `helpers.py` with an `is_*` or `get_*` function.
2. Add the entry point function to `cli.py`; keep it to ~10 lines.
3. Register the console script in `pyproject.toml` under `[project.scripts]`.
4. Add the hook definition to `.pre-commit-hooks.yaml`.
5. Add the hook to `.pre-commit-config.yaml` (local, `language: system`) for
   development.
6. Write tests in `tests/test_helpers.py` for the new helper functions.
7. Update `README.md` with a description of the new hook.
