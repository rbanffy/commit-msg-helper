import sys
from pathlib import Path

from commit_msg_helper.helpers import (
    get_current_branch,
    get_jira_ticket_from_branch,
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
    """Pre-commit hook entry point (prepare-commit-msg stage).

    Prepends the Jira ticket found in the current branch name to the
    commit message, unless the branch does not start with a Jira ticket
    or the message already begins with one.
    """
    branch = get_current_branch()
    if branch is None or is_safe_branch(branch):
        return 0

    ticket = get_jira_ticket_from_branch(branch)
    if ticket is None:
        return 0

    if len(sys.argv) < 2:
        print(
            "message-needs-jira: missing commit message file path",
            file=sys.stderr,
        )
        return 1

    msg_path = Path(sys.argv[1])
    try:
        msg = msg_path.read_text()
    except OSError as exc:
        print(
            f"message-needs-jira: could not read commit message file '{msg_path}': {exc}",
            file=sys.stderr,
        )
        return 1

    if not msg.startswith(ticket):
        try:
            msg_path.write_text(f"{ticket} {msg}")
        except OSError as exc:
            print(
                f"message-needs-jira: could not write commit message file '{msg_path}': {exc}",
                file=sys.stderr,
            )
            return 1

    return 0
