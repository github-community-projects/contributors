"""This module builds out the default data structure for the contributors stats object."""

# [
#   {
#     "username" : "zkoppert",
#     "new_contributor" : "False",
#     "avatar_url" : "https://avatars.githubusercontent.com/u/29484535?v=4",
#     "contribution_count" : 1261,
#     "commit_url" : "https://github.com/github-community-projects/contributors/commits?author=zkoppert&since=2023-10-01&until=2023-10-05"
#     "sponsor_info" : "https://github.com/sponsors/zkoppert"
#   }
# ]


from typing import List

import requests


class ContributorStats:
    """
    A class to represent a contributor_stats object correlating to a single contributors stats.

    Attributes:
        username (str): The username of the contributor
        new_contributor (bool): Whether the contributor is new or returning
        avatar_url (str): The url of the contributor's avatar
        contribution_count (int): The number of contributions the contributor has made
        commit_url (str): The url of the contributor's commits
        sponsor_info (str): The url of the contributor's sponsor page

    """

    def __new__(cls, *args, **kwargs):  # pylint: disable=unused-argument
        """Create a new contributor_stats object"""
        return super().__new__(cls)

    def __init__(
        self,
        username: str,
        new_contributor: bool,
        avatar_url: str,
        contribution_count: int,
        commit_url: str,
        sponsor_info: str,
    ):
        """Initialize the contributor_stats object"""
        self.username = username
        self.new_contributor = new_contributor
        self.avatar_url = avatar_url
        self.contribution_count = contribution_count
        self.commit_url = commit_url
        self.sponsor_info = sponsor_info

    def __repr__(self) -> str:
        """Return the representation of the contributor_stats object"""
        return (
            f"contributor_stats(username={self.username}, "
            f"new_contributor={self.new_contributor}, "
            f"avatar_url={self.avatar_url}, "
            f"contribution_count={self.contribution_count}, "
            f"commit_url={self.commit_url}, "
            f"sponsor_info={self.sponsor_info})"
        )

    def __eq__(self, other) -> bool:
        """Check if two contributor_stats objects are equal"""
        return (
            self.username == other.username
            and self.new_contributor == other.new_contributor
            and self.avatar_url == other.avatar_url
            and self.contribution_count == other.contribution_count
            and self.commit_url == other.commit_url
        )


def is_new_contributor(username: str, returning_contributors: list) -> bool:
    """
    Check if the contributor is new or returning

    Args:
        username (str): The username of the contributor
        returning_contributors (list): A list of ContributorStats objects
            representing contributors who have contributed to the repository
            before the start_date

    """
    for contributor in returning_contributors:
        if username in contributor.username:
            return False
    return True


def merge_contributors(contributors: list) -> list:
    """
    Merge contributors with the same username from multiple repositories.

    Args:
        contributors (list): A list of lists of ContributorStats objects

    Returns:
        merged_contributors (list): A list of ContributorStats objects with no duplicate usernames
    """
    merged_contributors: List[ContributorStats] = []
    for contributor_list in contributors:
        for contributor in contributor_list:
            # if the contributor is already in the merged list, merge their relevant attributes
            if contributor.username in [c.username for c in merged_contributors]:
                for merged_contributor in merged_contributors:
                    if merged_contributor.username == contributor.username:
                        # Merge the contribution counts via addition
                        merged_contributor.contribution_count += (
                            contributor.contribution_count
                        )
                        # Merge the commit urls via concatenation
                        merged_contributor.commit_url = (
                            f"{merged_contributor.commit_url}, {contributor.commit_url}"
                        )
                        # Merge the new_contributor attribute via OR
                        merged_contributor.new_contributor = (
                            merged_contributor.new_contributor
                            or contributor.new_contributor
                        )

            else:
                merged_contributors.append(contributor)

    return merged_contributors


def get_sponsor_information(contributors: list, token: str, ghe: str) -> list:
    """
    Get the sponsor information for each contributor

    Args:
        contributors (list): A list of ContributorStats objects
        github_connection (object): The authenticated GitHub connection object from PyGithub

    Returns:
        contributors (list): A list of ContributorStats objects with sponsor information
    """
    for contributor in contributors:
        # query the graphql api for the user's sponsor information
        query = """
        query($username: String!){
            repositoryOwner(login: $username) {
                ... on User {
                hasSponsorsListing
                }
            }
        }
        """
        variables = {"username": contributor.username}

        # Send the GraphQL request
        api_endpoint = f"{ghe}/api/v3" if ghe else "https://api.github.com"
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(
            f"{api_endpoint}/graphql",
            json={"query": query, "variables": variables},
            headers=headers,
            timeout=60,
        )

        # Check for errors in the GraphQL response
        if response.status_code != 200 or "errors" in response.json():
            raise ValueError("GraphQL query failed")

        data = response.json()["data"]

        endpoint = ghe if ghe else "https://github.com"
        # if the user has a sponsor page, add it to the contributor object
        if data["repositoryOwner"]["hasSponsorsListing"]:
            contributor.sponsor_info = f"{endpoint}/sponsors/{contributor.username}"

    return contributors
