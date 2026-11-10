"""Test the write_to_json function in json_writer.py."""

import json
import os
import unittest

from contributor_stats import ContributorStats
from json_writer import write_to_json


class TestWriteToJson(unittest.TestCase):
    """Test the write_to_json function."""

    def setUp(self):
        """Set up data for the tests."""
        self.filename = "test.json"
        self.data = {
            "start_date": "2022-01-01",
            "end_date": "2022-01-31",
            "organization": "test_org",
            "repository_list": ["repo1", "repo2"],
            "sponsor_info": False,
            "link_to_profile": False,
            "sort_column": "contribution_count",
            "sort_order": "desc",
            "contributors": [
                {
                    "username": "test_user",
                    "new_contributor": False,
                    "avatar_url": "https://test_url.com",
                    "contribution_count": 10,
                    "commit_url": "https://test_commit_url.com",
                    "sponsor_info": "",
                }
            ],
        }

    def test_write_to_json(self):
        """Test that write_to_json writes the correct data to a JSON file."""
        contributors = (
            ContributorStats(
                username="test_user",
                avatar_url="https://test_url.com",
                contribution_count=10,
                commit_url="https://test_commit_url.com",
                sponsor_info="",
            ),
        )

        write_to_json(
            contributors=contributors,
            filename=self.filename,
            start_date=self.data["start_date"],
            end_date=self.data["end_date"],
            organization=self.data["organization"],
            repository_list=self.data["repository_list"],
            sponsor_info=self.data["sponsor_info"],
            link_to_profile=self.data["link_to_profile"],
            sort_column=self.data["sort_column"],
            sort_order=self.data["sort_order"],
        )
        with open(self.filename, "r", encoding="utf-8") as f:
            result = json.load(f)
        self.assertDictEqual(result, self.data)

    def tearDown(self):
        os.remove(self.filename)


if __name__ == "__main__":
    unittest.main()
