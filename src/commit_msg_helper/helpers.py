import re
import subprocess

JIRA_TICKET_RE = re.compile(r"^[A-Z]{2,}-\d+")
SAFE_BRANCHES = {"main", "master", "develop"}


def get_current_branch() -> str | None:
    """Return the current Git branch name.

    Returns None when the branch cannot be determined, e.g. in a detached HEAD state.
    """
    try:
        return (
            subprocess.check_output(
                ["git", "symbolic-ref", "--short", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        return None


def is_jira_in_branch_name(branch: str) -> bool:
    """Return True if the branch name starts with a Jira ticket.

    A valid Jira ticket prefix consists of two or more uppercase letters,
    a hyphen, and one or more digits (e.g. ABC-123, MYPROJECT-42).
    """
    return bool(JIRA_TICKET_RE.match(branch))


def is_safe_branch(branch: str) -> bool:
    """Return True if the branch is exempt from the Jira ticket requirement.

    The exempt branches are: main, master, develop.
    """
    return branch in SAFE_BRANCHES


def get_jira_ticket_from_branch(branch: str) -> str | None:
    """Extract the Jira ticket identifier from a branch name.

    Returns the ticket string (e.g. "ABC-123") if the branch starts with one,
    or None if no ticket prefix is found.
    """
    match = JIRA_TICKET_RE.match(branch)
    return match.group(0) if match else None
