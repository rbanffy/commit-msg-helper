import subprocess
from unittest.mock import patch

from commit_msg_helper.helpers import (
    get_current_branch,
    get_jira_ticket_from_branch,
    is_jira_in_branch_name,
    is_safe_branch,
)


class TestGetCurrentBranch:
    def test_returns_branch_name(self):
        with patch(
            "commit_msg_helper.helpers.subprocess.check_output",
            return_value=b"ABC-123-my-feature\n",
        ):
            assert get_current_branch() == "ABC-123-my-feature"

    def test_strips_whitespace(self):
        with patch(
            "commit_msg_helper.helpers.subprocess.check_output",
            return_value=b"  main  \n",
        ):
            assert get_current_branch() == "main"

    def test_returns_none_on_detached_head(self):
        with patch(
            "commit_msg_helper.helpers.subprocess.check_output",
            side_effect=subprocess.CalledProcessError(128, "git"),
        ):
            assert get_current_branch() is None



class TestIsJiraInBranchName:
    def test_valid_ticket(self):
        assert is_jira_in_branch_name("ABC-123") is True

    def test_valid_ticket_with_description(self):
        assert is_jira_in_branch_name("ABC-123-my-feature") is True

    def test_valid_ticket_long_prefix(self):
        assert is_jira_in_branch_name("MYPROJECT-42-fix-bug") is True

    def test_single_letter_prefix_is_invalid(self):
        assert is_jira_in_branch_name("A-123") is False

    def test_lowercase_prefix_is_invalid(self):
        assert is_jira_in_branch_name("abc-123") is False

    def test_no_digits_is_invalid(self):
        assert is_jira_in_branch_name("ABC-") is False

    def test_no_hyphen_is_invalid(self):
        assert is_jira_in_branch_name("ABC123") is False

    def test_plain_branch_name_is_invalid(self):
        assert is_jira_in_branch_name("my-feature") is False

    def test_empty_string_is_invalid(self):
        assert is_jira_in_branch_name("") is False


class TestIsSafeBranch:
    def test_main_is_safe(self):
        assert is_safe_branch("main") is True

    def test_master_is_safe(self):
        assert is_safe_branch("master") is True

    def test_develop_is_safe(self):
        assert is_safe_branch("develop") is True

    def test_feature_branch_is_not_safe(self):
        assert is_safe_branch("my-feature") is False

    def test_jira_branch_is_not_safe(self):
        assert is_safe_branch("ABC-123-my-feature") is False

    def test_empty_string_is_not_safe(self):
        assert is_safe_branch("") is False


class TestGetJiraTicketFromBranch:
    def test_returns_ticket_from_plain_ticket_branch(self):
        assert get_jira_ticket_from_branch("ABC-123") == "ABC-123"

    def test_returns_ticket_prefix_from_descriptive_branch(self):
        assert get_jira_ticket_from_branch("ABC-123-my-feature") == "ABC-123"

    def test_returns_ticket_with_long_project_key(self):
        assert get_jira_ticket_from_branch("MYPROJECT-42-fix-bug") == "MYPROJECT-42"

    def test_returns_none_for_plain_branch(self):
        assert get_jira_ticket_from_branch("my-feature") is None

    def test_returns_none_for_safe_branch(self):
        assert get_jira_ticket_from_branch("main") is None

    def test_returns_none_for_lowercase_prefix(self):
        assert get_jira_ticket_from_branch("abc-123") is None

    def test_returns_none_for_empty_string(self):
        assert get_jira_ticket_from_branch("") is None
