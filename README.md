# commit-msg-helper

A pre-commit helper that enforces Jira ticket references in Git branch names and commit messages.

## Hooks

### `branch-needs-jira`

Verifies that the current branch name starts with a Jira ticket identifier
(two or more uppercase letters, a hyphen, and one or more digits — e.g. `ABC-123`).

The following branches are exempt: `main`, `master`, `develop`.

Exits `0` (allow commit) when the branch is valid or exempt, `1` (block commit) otherwise.

### `message-needs-jira`

Not yet implemented. Will verify that the commit message references a Jira ticket.

## Usage

Add the following to your `.pre-commit-config.yaml`:

```yaml
repos:
-   repo: https://github.com/rbanffy/commit-msg-helper
    rev: main
    hooks:
    -   id: branch-needs-jira
```

Then install the hooks:

```shell
pre-commit install
```

## Development

```shell
uv add --dev pytest ruff
uv run pytest
```
