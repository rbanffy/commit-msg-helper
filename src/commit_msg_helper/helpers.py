import re
import subprocess

JIRA_TICKET_RE = re.compile(r"^[A-Z]{2,}-\d+")
SAFE_BRANCHES = {"main", "master", "develop"}


def get_current_branch() -> str | None:
    """Return the current Git branch name, or None if it cannot be determined."""
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
    """Return True if the branch name starts with a Jira ticket (e.g. ABC-123)."""
    return bool(JIRA_TICKET_RE.match(branch))


def is_safe_branch(branch: str) -> bool:
    """Return True if the branch is a well-known branch that doesn't need a Jira ticket."""
    return branch in SAFE_BRANCHES
