import sys

from commit_msg_helper.helpers import (
    get_current_branch,
    is_jira_in_branch_name,
    is_safe_branch,
)


def branch_needs_jira() -> int:
    """Pre-commit hook entry point.

    Exits 0 if the current branch starts with a Jira ticket (e.g. ABC-123),
    or is one of the well-known safe branches (main, master, develop).
    Exits 1 otherwise, printing a diagnostic message to stderr.
    """
    branch = get_current_branch()
    if branch is None:
        print(
            "branch-needs-jira: could not determine current branch (detached HEAD?)",
            file=sys.stderr,
        )
        return 1

    if is_safe_branch(branch) or is_jira_in_branch_name(branch):
        return 0

    print(
        f"branch-needs-jira: branch '{branch}' does not start with a Jira ticket (e.g. ABC-123)",
        file=sys.stderr,
    )
    return 1


def message_needs_jira() -> int:
    """Pre-commit hook entry point (not yet implemented).

    Will verify that the commit message references a Jira ticket.
    Currently a no-op that always exits 0.
    """
    return 0
