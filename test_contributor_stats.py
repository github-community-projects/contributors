"""This module contains the tests for the ContributorStats class."""

import unittest
from unittest.mock import MagicMock, patch

from contributor_stats import (
    ContributorStats,
    get_sponsor_information,
    is_new_contributor,
    merge_contributors,
)


class TestContributorStats(unittest.TestCase):
    """
    Test case for the ContributorStats class.
    """

    def setUp(self):
        """
        Set up a ContributorStats instance for use in tests.
        """
        self.contributor = ContributorStats(
            "zkoppert",
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            1261,
            "commit_url5",
            "",
        )

    def test_init_new_contributor_true(self):
        """
        Test that new_contributor=True is preserved by __init__.
        """
        contributor = ContributorStats(
            "new_user",
            avatar_url="https://example.com/avatar.png",
            contribution_count=1,
            commit_url="commit_url_new",
            sponsor_info="",
            new_contributor=True,
        )
        self.assertTrue(contributor.new_contributor)

    def test_init(self):
        """
        Test the __init__ method of the ContributorStats class.
        """
        self.assertEqual(self.contributor.username, "zkoppert")
        self.assertFalse(self.contributor.new_contributor)
        self.assertEqual(
            self.contributor.avatar_url,
            "https://avatars.githubusercontent.com/u/29484535?v=4",
        )
        self.assertEqual(self.contributor.contribution_count, 1261)
        self.assertEqual(
            self.contributor.commit_url,
            "commit_url5",
        )

    def test_repr(self):
        """Test the __repr__ method includes key fields."""
        expected = (
            "contributor_stats(username=zkoppert, "
            "avatar_url=https://avatars.githubusercontent.com/u/29484535?v=4, "
            "contribution_count=1261, "
            "commit_url=commit_url5, "
            "sponsor_info=, "
            "new_contributor=False)"
        )
        self.assertEqual(repr(self.contributor), expected)

    def test_merge_contributors(self):
        """
        Test the merge_contributors function.
        """
        contributor1 = ContributorStats(
            "user1",
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            100,
            "commit_url1",
            "",
        )
        contributor2 = ContributorStats(
            "user2",
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            200,
            "commit_url2",
            "",
        )
        contributor3 = ContributorStats(
            "user1",
            "https://avatars.githubusercontent.com/u/29484535?v=4",
            150,
            "commit_url3",
            "",
        )
        all_contributors = [
            [
                contributor1,
                contributor2,
                contributor3,
            ]
        ]
        expected_result = [
            ContributorStats(
                "user1",
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                250,
                "commit_url1, commit_url3",
                "",
            ),
            ContributorStats(
                "user2",
                "https://avatars.githubusercontent.com/u/29484535?v=4",
                200,
                "commit_url2",
                "",
            ),
        ]

        result = merge_contributors(all_contributors)

        self.assertEqual(expected_result, result)

    def test_is_new_contributor_true(self):
        """
        Test the is_new_contributor function when the contributor is new.
        """
        username = "new_user"
        returning_contributors = [
            ContributorStats(
                username="user1",
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=100,
                commit_url="url1",
                sponsor_info="",
            ),
            ContributorStats(
                username="user2",
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=200,
                commit_url="url2",
                sponsor_info="",
            ),
        ]

        result = is_new_contributor(username, returning_contributors)

        self.assertTrue(result)

    def test_is_new_contributor_false(self):
        """
        Test the is_new_contributor function when the contributor is not new.
        """
        username = "user1"
        returning_contributors = [
            ContributorStats(
                username="user1",
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=100,
                commit_url="url1",
                sponsor_info="",
            ),
            ContributorStats(
                username="user2",
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=200,
                commit_url="url2",
                sponsor_info="",
            ),
        ]

        result = is_new_contributor(username, returning_contributors)

        self.assertFalse(result)

    @patch("requests.post")
    def test_fetch_sponsor_info(self, mock_post):
        """
        Test the get_sponsor_information function.
        """
        # Mock response data
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": {"repositoryOwner": {"hasSponsorsListing": True}}
        }
        mock_post.return_value = mock_response

        # Mock contributors
        user = "user1"
        returning_contributors = [
            ContributorStats(
                username=user,
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=100,
                commit_url="url1",
                sponsor_info="",
            ),
        ]

        # Test parameters
        ghe = ""
        token = "token"

        # Call the function
        result = get_sponsor_information(returning_contributors, token, ghe)

        # Assertions
        self.assertEqual(result[0].sponsor_info, "https://github.com/sponsors/user1")

        # Ensure the post request was called with the correct parameters
        mock_post.assert_called_once_with(
            "https://api.github.com/graphql",
            json={
                "query": """
        query($username: String!){
            repositoryOwner(login: $username) {
                ... on User {
                hasSponsorsListing
                }
            }
        }
        """,
                "variables": {"username": "user1"},
            },
            headers={"Authorization": "Bearer token"},
            timeout=60,
        )

    @patch("requests.post")
    def test_fetch_sponsor_info_skips_when_repository_owner_is_none(self, mock_post):
        """Skip users whose repositoryOwner is null (orgs, deleted users, bots)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": {"repositoryOwner": None}}
        mock_post.return_value = mock_response

        contributors = [
            ContributorStats(
                username="some-org",
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=10,
                commit_url="url",
                sponsor_info="",
            ),
        ]

        result = get_sponsor_information(contributors, token="token", ghe="")

        self.assertEqual(result[0].sponsor_info, "")

    @patch("requests.post")
    def test_fetch_sponsor_info_raises_on_error(self, mock_post):
        """Test get_sponsor_information raises when the API response is invalid."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"errors": [{"message": "fail"}]}
        mock_post.return_value = mock_response

        contributors = [
            ContributorStats(
                username="user1",
                avatar_url="https://avatars.githubusercontent.com/u/",
                contribution_count=100,
                commit_url="url1",
                sponsor_info="",
            ),
        ]

        with self.assertRaises(ValueError):
            get_sponsor_information(contributors, token="token", ghe="")


if __name__ == "__main__":
    unittest.main()
