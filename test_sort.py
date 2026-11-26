"""Test cases for the sort module."""

import unittest

from sort import sort_contributions

import contributor_stats


# Case insensitive sort with natural sorting support
class TestSortedCollaborators(unittest.TestCase):
    # Sample list of ContributorStats objects
    """ContributorStats object:
    username: str,
    avatar_url: str,
    contribution_count: int,
    commit_url: str,
    sponsor_info: str,
    new_contributor: bool,
    """

    person1 = contributor_stats.ContributorStats(
        "Bob", "url", 3, "commit url", "sponsor_url_1", True
    )
    person2 = contributor_stats.ContributorStats(
        "alice", "url2", 5, "commit url2", "sponsor_url_2", False
    )
    person3 = contributor_stats.ContributorStats(
        "user10", "url2", 2, "commit url2", "sponsor_url_2", False
    )
    person4 = contributor_stats.ContributorStats(
        "user2", "url2", 1, "commit url2", "sponsor_url_2", False
    )

    collaborators = [
        person1,
        person2,
        person3,
        person4,
    ]

    def test_sort_does_not_modify_original_list(self):
        """Verify sorting leaves the original collaborators list unchanged."""
        original_order = [getattr(c, "username") for c in self.collaborators]
        sort_contributions(self.collaborators, "username", "asc")
        self.assertEqual(
            [getattr(c, "username") for c in self.collaborators],
            original_order,
        )

    def test_contribution_count_ascending(self):
        """Verify collaborators are sorted by contribution count in ascending order."""
        sorted_collaborators = sort_contributions(
            self.collaborators, "contribution_count", "asc"
        )
        self.assertEqual(
            [getattr(c, "username") for c in sorted_collaborators],
            ["user2", "user10", "Bob", "alice"],
        )

    def test_contribution_count_descending(self):
        """Verify collaborators are sorted by contribution count in descending order."""
        sorted_collaborators = sort_contributions(
            self.collaborators, "contribution_count", "desc"
        )
        self.assertEqual(
            [getattr(c, "username") for c in sorted_collaborators],
            ["alice", "Bob", "user10", "user2"],
        )

    def test_username_ascending(self):
        """Verify collaborators are sorted by username in ascending order."""
        sorted_collaborators = sort_contributions(self.collaborators, "username", "asc")
        self.assertEqual(
            [getattr(c, "username") for c in sorted_collaborators],
            ["alice", "Bob", "user2", "user10"],
        )

    def test_username_descending(self):
        """Verify collaborators are sorted by username in descending order."""
        sorted_collaborators = sort_contributions(
            self.collaborators, "username", "desc"
        )
        self.assertEqual(
            [getattr(c, "username") for c in sorted_collaborators],
            ["user10", "user2", "Bob", "alice"],
        )

    def test_new_contributor_ascending(self):
        """Verify collaborators are sorted by new-contributor status in ascending order."""
        sorted_collaborators = sort_contributions(
            self.collaborators, "new_contributor", "asc"
        )
        self.assertEqual(
            [getattr(c, "username") for c in sorted_collaborators],
            ["alice", "user10", "user2", "Bob"],
        )

    def test_new_contributor_descending(self):
        """Verify collaborators are sorted by new-contributor status in descending order."""
        sorted_collaborators = sort_contributions(
            self.collaborators, "new_contributor", "desc"
        )
        self.assertEqual(
            [getattr(c, "username") for c in sorted_collaborators],
            ["Bob", "alice", "user10", "user2"],
        )


if __name__ == "__main__":
    unittest.main()
