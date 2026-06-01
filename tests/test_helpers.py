import pytest

from commit_msg_helper.helpers import is_jira_in_branch_name, is_safe_branch


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
