import re
import subprocess
import sys

JIRA_TICKET_RE = re.compile(r"^[A-Z]{2,}-\d+")
SAFE_BRANCHES = {"main", "master", "develop"}


def branch_needs_jira() -> int:
    try:
        branch = (
            subprocess.check_output(
                ["git", "symbolic-ref", "--short", "HEAD"],
                stderr=subprocess.DEVNULL,
            )
            .decode()
            .strip()
        )
    except subprocess.CalledProcessError:
        print(
            "branch-needs-jira: could not determine current branch (detached HEAD?)",
            file=sys.stderr,
        )
        return 1

    if branch in SAFE_BRANCHES or JIRA_TICKET_RE.match(branch):
        return 0

    print(
        f"branch-needs-jira: branch '{branch}' does not start with a Jira ticket (e.g. ABC-123)",
        file=sys.stderr,
    )
    return 1


def message_needs_jira() -> int:
    return 0
