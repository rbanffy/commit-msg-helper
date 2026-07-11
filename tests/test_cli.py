from pathlib import Path

from commit_msg_helper import cli


class TestMessageNeedsJira:
    def test_returns_error_when_message_path_arg_is_missing(
        self, monkeypatch, capsys
    ):
        monkeypatch.setattr(cli, "get_current_branch", lambda: "ABC-123-feature")
        monkeypatch.setattr(
            cli, "get_jira_ticket_from_branch", lambda branch: "ABC-123"
        )
        monkeypatch.setattr(cli.sys, "argv", ["message-needs-jira"])

        result = cli.message_needs_jira()

        captured = capsys.readouterr()
        assert result == 1
        assert "missing commit message file path" in captured.err

    def test_prepends_ticket_to_commit_message(self, monkeypatch, tmp_path):
        msg_path = tmp_path / "COMMIT_EDITMSG"
        msg_path.write_text("my commit message")

        monkeypatch.setattr(cli, "get_current_branch", lambda: "ABC-123-feature")
        monkeypatch.setattr(
            cli, "get_jira_ticket_from_branch", lambda branch: "ABC-123"
        )
        monkeypatch.setattr(
            cli.sys, "argv", ["message-needs-jira", str(msg_path)]
        )

        result = cli.message_needs_jira()

        assert result == 0
        assert msg_path.read_text() == "ABC-123 my commit message"

    def test_does_not_duplicate_existing_prefix(self, monkeypatch, tmp_path):
        msg_path = tmp_path / "COMMIT_EDITMSG"
        msg_path.write_text("ABC-123 existing message")

        monkeypatch.setattr(cli, "get_current_branch", lambda: "ABC-123-feature")
        monkeypatch.setattr(
            cli, "get_jira_ticket_from_branch", lambda branch: "ABC-123"
        )
        monkeypatch.setattr(
            cli.sys, "argv", ["message-needs-jira", str(msg_path)]
        )

        result = cli.message_needs_jira()

        assert result == 0
        assert msg_path.read_text() == "ABC-123 existing message"

    def test_returns_success_when_branch_has_no_ticket(self, monkeypatch, tmp_path):
        msg_path = tmp_path / "COMMIT_EDITMSG"
        msg_path.write_text("my commit message")

        monkeypatch.setattr(cli, "get_current_branch", lambda: "feature/no-jira")
        monkeypatch.setattr(cli, "get_jira_ticket_from_branch", lambda branch: None)
        monkeypatch.setattr(
            cli.sys, "argv", ["message-needs-jira", str(msg_path)]
        )

        result = cli.message_needs_jira()

        assert result == 0
        assert msg_path.read_text() == "my commit message"

    def test_returns_success_when_branch_cannot_be_determined(
        self, monkeypatch, tmp_path
    ):
        msg_path = tmp_path / "COMMIT_EDITMSG"
        msg_path.write_text("my commit message")

        monkeypatch.setattr(cli, "get_current_branch", lambda: None)
        monkeypatch.setattr(
            cli.sys, "argv", ["message-needs-jira", str(msg_path)]
        )

        result = cli.message_needs_jira()

        assert result == 0
        assert msg_path.read_text() == "my commit message"
