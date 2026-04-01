"""This module contains the tests for the contributors.py module"""

import runpy
import unittest
from unittest.mock import MagicMock, patch

import contributors as contributors_module
from contributor_stats import ContributorStats


class TestContributors(unittest.TestCase):
    """
    Test case for the contributors module.
    """

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors(self, mock_contributor_stats):
        """
        Test the get_contributors function.
        """
        mock_repo = MagicMock()
        mock_commit = MagicMock()
        mock_commit.author.login = "user"
        mock_commit.author.avatar_url = (
            "https://avatars.githubusercontent.com/u/12345678?v=4"
        )
        mock_repo.full_name = "owner/repo"
        mock_repo.commits.return_value = iter([mock_commit])

        result = contributors_module.get_contributors(
            mock_repo, "2022-01-01", "2022-12-31", ""
        )

        self.assertEqual(len(result), 1)
        mock_repo.commits.assert_called_once_with(
            since="2022-01-01", until="2022-12-31"
        )
        mock_contributor_stats.assert_called_once_with(
            "user",
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            1,
            "https://github.com/owner/repo/commits?author=user&since=2022-01-01&until=2022-12-31",
            "",
        )

    @patch("contributors.get_contributors")
    def test_get_all_contributors_with_organization(self, mock_get_contributors):
        """
        Test the get_all_contributors function when an organization is provided.
        """
        mock_github_connection = MagicMock()
        mock_github_connection.organization().repositories.return_value = [
            "repo1",
            "repo2",
        ]
        mock_get_contributors.return_value = [
            ContributorStats(
                "user",
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                100,
                "commit_url",
                "sponsor_url_1",
            ),
        ]
        ghe = ""

        result = contributors_module.get_all_contributors(
            "org", [], "2022-01-01", "2022-12-31", mock_github_connection, ghe
        )

        self.assertEqual(
            result,
            [
                ContributorStats(
                    "user",
                    "https://avatars.githubusercontent.com/u/29484535?v=4",
                    200,
                    "commit_url, commit_url",
                    "sponsor_url_1",
                ),
            ],
        )
        mock_get_contributors.assert_any_call("repo1", "2022-01-01", "2022-12-31", ghe)
        mock_get_contributors.assert_any_call("repo2", "2022-01-01", "2022-12-31", ghe)

    @patch("contributors.get_contributors")
    def test_get_all_contributors_with_repository(self, mock_get_contributors):
        """
        Test the get_all_contributors function when a repository is provided.
        """
        mock_github_connection = MagicMock()
        mock_github_connection.repository.return_value = "repo"
        mock_get_contributors.return_value = [
            ContributorStats(
                "user",
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                100,
                "commit_url2",
                "sponsor_url_2",
            )
        ]
        ghe = ""

        result = contributors_module.get_all_contributors(
            "", ["owner/repo"], "2022-01-01", "2022-12-31", mock_github_connection, ghe
        )

        self.assertEqual(
            result,
            [
                ContributorStats(
                    "user",
                    "https://avatars.githubusercontent.com/u/29484535?v=4",
                    100,
                    "commit_url2",
                    "sponsor_url_2",
                ),
            ],
        )
        mock_get_contributors.assert_called_once_with(
            "repo", "2022-01-01", "2022-12-31", ghe
        )

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors_with_single_commit(self, mock_contributor_stats):
        """
        Test get_contributors returns a single contributor for one commit in the date range.
        """
        mock_repo = MagicMock()
        mock_commit = MagicMock()
        mock_commit.author.login = "user"
        mock_commit.author.avatar_url = (
            "https://avatars.githubusercontent.com/u/12345678?v=4"
        )

        mock_repo.full_name = "owner/repo"
        mock_repo.commits.return_value = iter([mock_commit])
        ghe = ""

        result = contributors_module.get_contributors(
            mock_repo, "2022-01-01", "2022-12-31", ghe
        )

        self.assertEqual(len(result), 1)
        mock_repo.commits.assert_called_once_with(
            since="2022-01-01", until="2022-12-31"
        )
        mock_contributor_stats.assert_called_once_with(
            "user",
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            1,
            "https://github.com/owner/repo/commits?author=user&since=2022-01-01&until=2022-12-31",
            "",
        )

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors_skip_bot(self, mock_contributor_stats):
        """
        Test if the get_contributors function skips the bot user.
        """
        mock_repo = MagicMock()
        mock_commit = MagicMock()
        mock_commit.author.login = "[bot]"
        mock_commit.author.avatar_url = (
            "https://avatars.githubusercontent.com/u/12345678?v=4"
        )

        mock_repo.full_name = "owner/repo"
        mock_repo.commits.return_value = iter([mock_commit])
        ghe = ""

        result = contributors_module.get_contributors(
            mock_repo, "2022-01-01", "2022-12-31", ghe
        )

        self.assertEqual(result, [])
        # Ensure that the bot user is skipped and ContributorStats is never instantiated
        mock_contributor_stats.assert_not_called()

    @patch("contributors.contributor_stats.ContributorStats")
    def test_get_contributors_no_commit_end_date(self, mock_contributor_stats):
        """
        Test get_contributors skips commit-range filtering when end_date is not set.
        """
        mock_repo = MagicMock()
        mock_user = MagicMock()
        mock_user.login = "user"
        mock_user.avatar_url = "https://avatars.githubusercontent.com/u/12345678?v=4"
        mock_user.contributions_count = 100

        mock_repo.contributors.return_value = [mock_user]
        mock_repo.full_name = "owner/repo"
        ghe = ""

        contributors_module.get_contributors(mock_repo, "2022-01-01", "", ghe)

        mock_repo.commits.assert_not_called()
        mock_contributor_stats.assert_called_once_with(
            "user",
            "https://avatars.githubusercontent.com/u/12345678?v=4",
            100,
            "https://github.com/owner/repo/commits?author=user",
            "",
        )

    def test_get_contributors_skips_when_no_commits_in_range(self):
        """Test get_contributors returns empty list when no commits in the date range."""
        mock_repo = MagicMock()
        mock_repo.full_name = "owner/repo"
        mock_repo.commits.return_value = iter([])

        result = contributors_module.get_contributors(
            mock_repo, "2022-01-01", "2022-12-31", ""
        )

        self.assertEqual(result, [])

    def test_get_contributors_skips_none_author(self):
        """Test get_contributors skips commits with no linked GitHub author."""
        mock_repo = MagicMock()
        mock_repo.full_name = "owner/repo"
        mock_commit = MagicMock()
        mock_commit.author = None
        mock_repo.commits.return_value = iter([mock_commit])

        result = contributors_module.get_contributors(
            mock_repo, "2022-01-01", "2022-12-31", ""
        )

        self.assertEqual(result, [])

    def test_get_contributors_aggregates_multiple_commits(self):
        """Test get_contributors counts multiple commits per author correctly."""
        mock_repo = MagicMock()
        mock_repo.full_name = "owner/repo"
        mock_commit1 = MagicMock()
        mock_commit1.author.login = "user"
        mock_commit1.author.avatar_url = "https://avatars.githubusercontent.com/u/1"
        mock_commit2 = MagicMock()
        mock_commit2.author.login = "user"
        mock_commit2.author.avatar_url = "https://avatars.githubusercontent.com/u/1"
        mock_repo.commits.return_value = iter([mock_commit1, mock_commit2])

        result = contributors_module.get_contributors(
            mock_repo, "2022-01-01", "2022-12-31", ""
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].contribution_count, 2)

    def test_get_contributors_handles_exception(self):
        """Test get_contributors returns None when an exception is raised."""

        class BoomIterable:  # pylint: disable=too-few-public-methods
            """Iterable that raises an exception when iterated over."""

            def __iter__(self):
                raise RuntimeError("boom")

        mock_repo = MagicMock()
        mock_repo.full_name = "owner/repo"
        mock_repo.commits.return_value = BoomIterable()

        with patch("builtins.print") as mock_print:
            result = contributors_module.get_contributors(
                mock_repo, "2022-01-01", "2022-12-31", ""
            )

        self.assertIsNone(result)
        mock_print.assert_any_call(
            "Error getting contributors for repository: owner/repo"
        )
        self.assertTrue(
            any(
                args and str(args[0]) == "boom" for args, _ in mock_print.call_args_list
            )
        )

    def test_main_runs_under_main_guard(self):
        """Test running contributors as a script executes main."""
        mock_env = MagicMock()
        mock_env.get_env_vars.return_value = (
            "org",
            [],
            123,
            456,
            b"key",
            False,
            "",
            "",
            "2022-01-01",
            "2022-12-31",
            False,
            False,
            "contributors.md",
            False,
        )

        mock_auth = MagicMock()
        mock_github = MagicMock()
        mock_org = MagicMock()
        mock_org.repositories.return_value = []
        mock_github.organization.return_value = mock_org
        mock_auth.auth_to_github.return_value = mock_github
        mock_auth.get_github_app_installation_token.return_value = "token"

        mock_markdown = MagicMock()
        mock_json_writer = MagicMock()

        with patch.dict(
            "sys.modules",
            {
                "env": mock_env,
                "auth": mock_auth,
                "markdown": mock_markdown,
                "json_writer": mock_json_writer,
            },
            clear=False,
        ):
            runpy.run_module("contributors", run_name="__main__")

        mock_env.get_env_vars.assert_called_once()
        mock_auth.auth_to_github.assert_called_once()
        mock_auth.get_github_app_installation_token.assert_called_once_with(
            "", 123, b"key", 456
        )
        mock_markdown.write_to_markdown.assert_called_once()
        mock_json_writer.write_to_json.assert_called_once()

    def test_main_sets_new_contributor_flag(self):
        """Test main sets new_contributor when start/end dates are provided."""
        contributor = ContributorStats(
            "user1",
            "https://avatars.githubusercontent.com/u/1",
            10,
            "commit_url",
            "",
        )

        with (
            patch.object(contributors_module.env, "get_env_vars") as mock_get_env_vars,
            patch.object(
                contributors_module.auth, "auth_to_github"
            ) as mock_auth_to_github,
            patch.object(
                contributors_module, "get_all_contributors"
            ) as mock_get_all_contributors,
            patch.object(
                contributors_module.contributor_stats,
                "is_new_contributor",
                return_value=True,
            ) as mock_is_new,
            patch.object(contributors_module.markdown, "write_to_markdown"),
            patch.object(contributors_module.json_writer, "write_to_json"),
        ):
            mock_get_env_vars.return_value = (
                "org",
                [],
                None,
                None,
                b"",
                False,
                "token",
                "",
                "2022-01-01",
                "2022-12-31",
                False,
                False,
                "contributors.md",
                False,
            )
            mock_auth_to_github.return_value = MagicMock()
            mock_get_all_contributors.side_effect = [[contributor], []]

            contributors_module.main()

        mock_is_new.assert_called_once_with("user1", [])
        self.assertTrue(contributor.new_contributor)

    def test_main_fetches_sponsor_info_when_enabled(self):
        """Test main fetches sponsor information when sponsor_info is enabled."""
        contributor = ContributorStats(
            "user1",
            "https://avatars.githubusercontent.com/u/1",
            10,
            "commit_url",
            "",
        )
        sponsored_contributor = ContributorStats(
            "user1",
            "https://avatars.githubusercontent.com/u/1",
            10,
            "commit_url",
            "https://github.com/sponsors/user1",
        )

        with (
            patch.object(contributors_module.env, "get_env_vars") as mock_get_env_vars,
            patch.object(
                contributors_module.auth, "auth_to_github"
            ) as mock_auth_to_github,
            patch.object(
                contributors_module, "get_all_contributors"
            ) as mock_get_all_contributors,
            patch.object(
                contributors_module.contributor_stats, "get_sponsor_information"
            ) as mock_get_sponsor_information,
            patch.object(contributors_module.markdown, "write_to_markdown"),
            patch.object(contributors_module.json_writer, "write_to_json"),
        ):
            mock_get_env_vars.return_value = (
                "org",
                [],
                None,
                None,
                b"",
                False,
                "token",
                "",
                "",
                "",
                True,
                False,
                "contributors.md",
                False,
            )
            mock_auth_to_github.return_value = MagicMock()
            mock_get_all_contributors.return_value = [contributor]
            mock_get_sponsor_information.return_value = [sponsored_contributor]

            contributors_module.main()

        mock_get_sponsor_information.assert_called_once_with([contributor], "token", "")


if __name__ == "__main__":
    unittest.main()
