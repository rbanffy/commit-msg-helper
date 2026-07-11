# commit-msg-helper

A pre-commit helper that enforces Jira ticket references in Git branch names and commit messages.

## Hooks

### `branch-needs-jira`

Verifies that the current branch name starts with a Jira ticket identifier
(two or more uppercase letters, a hyphen, and one or more digits — e.g. `ABC-123`).

The following branches are exempt: `main`, `master`, `develop`.

Exits `0` (allow commit) when the branch is valid or exempt, `1` (block commit) otherwise.

### `message-needs-jira`

Runs at the `prepare-commit-msg` stage. If the current branch starts with
a Jira ticket identifier, that ticket is automatically prepended to the
commit message (e.g. `ABC-123 your message`). Does nothing on safe
branches or branches without a ticket prefix.

## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/rbanffy/commit-msg-helper
    rev: main
    hooks:
    -   id: branch-needs-jira
    -   id: message-needs-jira
```

Then install the hooks — all three hook types are required:

```shell
pre-commit install
pre-commit install --hook-type prepare-commit-msg
pre-commit install --hook-type commit-msg
```

## Development

```shell
uv add --dev pytest ruff
uv run pytest
```
