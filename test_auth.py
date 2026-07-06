"""Test cases for the auth module."""

import unittest
from unittest.mock import MagicMock, patch

import auth
import requests
from github import GithubException


class TestAuth(unittest.TestCase):
    """
    Test case for the auth module.
    """

    @patch("auth.Auth")
    @patch("auth.Github")
    def test_auth_to_github_with_token(self, mock_github_cls, mock_auth_cls):
        """
        Test the auth_to_github function when the token is provided.
        """
        mock_token = MagicMock()
        mock_auth_cls.Token.return_value = mock_token
        mock_github = MagicMock()
        mock_github_cls.return_value = mock_github

        result = auth.auth_to_github("token", "", "", b"", "", False)

        mock_auth_cls.Token.assert_called_once_with("token")
        mock_github_cls.assert_called_once_with(auth=mock_token)
        self.assertEqual(result, mock_github)

    def test_auth_to_github_without_token(self):
        """
        Test the auth_to_github function when the token is not provided.
        Expect a ValueError to be raised.
        """
        with self.assertRaises(ValueError) as context_manager:
            auth.auth_to_github("", "", "", b"", "", False)
        the_exception = context_manager.exception
        self.assertEqual(
            str(the_exception),
            "GH_TOKEN or the set of [GH_APP_ID, GH_APP_INSTALLATION_ID, GH_APP_PRIVATE_KEY] environment variables are not set",
        )

    @patch("auth.Auth")
    @patch("auth.Github")
    def test_auth_to_github_with_ghe(self, mock_github_cls, mock_auth_cls):
        """
        Test the auth_to_github function when the GitHub Enterprise URL is provided.
        """
        mock_token = MagicMock()
        mock_auth_cls.Token.return_value = mock_token
        mock_github = MagicMock()
        mock_github_cls.return_value = mock_github

        result = auth.auth_to_github(
            "token", "", "", b"", "https://github.example.com", False
        )

        mock_auth_cls.Token.assert_called_once_with("token")
        mock_github_cls.assert_called_once_with(
            base_url="https://github.example.com/api/v3", auth=mock_token
        )
        self.assertEqual(result, mock_github)

    @patch("auth.Auth")
    @patch("auth.Github")
    def test_auth_to_github_with_ghe_and_ghe_app(self, mock_github_cls, mock_auth_cls):
        """
        Test the auth_to_github function when the GitHub Enterprise URL is provided and the app was created in GitHub Enterprise URL.
        """
        mock_app_auth = MagicMock()
        mock_installation_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_app_auth.get_installation_auth.return_value = mock_installation_auth
        mock_github = MagicMock()
        mock_github_cls.return_value = mock_github

        result = auth.auth_to_github(
            "", "123", "123", b"123", "https://github.example.com", True
        )

        mock_auth_cls.AppAuth.assert_called_once_with(123, "123")
        mock_app_auth.get_installation_auth.assert_called_once_with(123)
        mock_github_cls.assert_called_once_with(
            base_url="https://github.example.com/api/v3", auth=mock_installation_auth
        )
        self.assertEqual(result, mock_github)

    @patch("auth.Auth")
    @patch("auth.Github")
    def test_auth_to_github_with_app(self, mock_github_cls, mock_auth_cls):
        """
        Test the auth_to_github function when app credentials are provided
        """
        mock_app_auth = MagicMock()
        mock_installation_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_app_auth.get_installation_auth.return_value = mock_installation_auth
        mock_github = MagicMock()
        mock_github_cls.return_value = mock_github

        result = auth.auth_to_github(
            "", "123", "123", b"123", "https://github.example.com", False
        )

        mock_auth_cls.AppAuth.assert_called_once_with(123, "123")
        mock_app_auth.get_installation_auth.assert_called_once_with(123)
        mock_github_cls.assert_called_once_with(auth=mock_installation_auth)
        self.assertEqual(result, mock_github)

    @patch("auth.Auth")
    @patch("auth.Github")
    def test_auth_to_github_with_app_int_app_id(self, mock_github_cls, mock_auth_cls):
        """
        Test that an integer app_id is converted properly for Auth.AppAuth.
        """
        mock_app_auth = MagicMock()
        mock_installation_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_app_auth.get_installation_auth.return_value = mock_installation_auth
        mock_github = MagicMock()
        mock_github_cls.return_value = mock_github

        result = auth.auth_to_github("", 123, 456, b"private_key", "", False)

        mock_auth_cls.AppAuth.assert_called_once_with(123, "private_key")
        mock_app_auth.get_installation_auth.assert_called_once_with(456)
        mock_github_cls.assert_called_once_with(auth=mock_installation_auth)
        self.assertEqual(result, mock_github)

    @patch("auth.Auth")
    @patch("auth.GithubIntegration")
    def test_get_github_app_installation_token(
        self, mock_integration_cls, mock_auth_cls
    ):
        """
        Test the get_github_app_installation_token function.
        """
        dummy_token = "dummytoken"
        mock_app_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_integration = MagicMock()
        mock_integration_cls.return_value = mock_integration
        mock_access_token = MagicMock()
        mock_access_token.token = dummy_token
        mock_integration.get_access_token.return_value = mock_access_token

        result = auth.get_github_app_installation_token(
            "", "123", b"gh_private_key", "456"
        )

        mock_auth_cls.AppAuth.assert_called_once_with(123, "gh_private_key")
        mock_integration_cls.assert_called_once_with(auth=mock_app_auth)
        mock_integration.get_access_token.assert_called_once_with(456)
        self.assertEqual(result, dummy_token)

    @patch("auth.Auth")
    @patch("auth.GithubIntegration")
    def test_get_github_app_installation_token_request_failure(
        self, mock_integration_cls, mock_auth_cls
    ):
        """
        Test the get_github_app_installation_token function returns None when the request fails.
        """
        mock_app_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_integration = MagicMock()
        mock_integration_cls.return_value = mock_integration
        mock_integration.get_access_token.side_effect = GithubException(
            500, "Request failed", None
        )

        result = auth.get_github_app_installation_token(
            ghe="https://api.github.com",
            gh_app_id="12345",
            gh_app_private_key_bytes=b"private_key",
            gh_app_installation_id="678910",
        )

        self.assertIsNone(result)

    @patch("auth.Auth")
    @patch("auth.GithubIntegration")
    def test_get_github_app_installation_token_network_failure(
        self, mock_integration_cls, mock_auth_cls
    ):
        """
        Test the get_github_app_installation_token function returns None on network errors.
        """
        mock_app_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_integration = MagicMock()
        mock_integration_cls.return_value = mock_integration
        mock_integration.get_access_token.side_effect = (
            requests.exceptions.ConnectionError("Network unreachable")
        )

        result = auth.get_github_app_installation_token(
            ghe="",
            gh_app_id="12345",
            gh_app_private_key_bytes=b"private_key",
            gh_app_installation_id="678910",
        )

        self.assertIsNone(result)

    @patch("auth.Auth")
    @patch("auth.GithubIntegration")
    def test_get_github_app_installation_token_with_ghe(
        self, mock_integration_cls, mock_auth_cls
    ):
        """
        Test the get_github_app_installation_token function with a GHE URL.
        """
        dummy_token = "dummytoken"
        mock_app_auth = MagicMock()
        mock_auth_cls.AppAuth.return_value = mock_app_auth
        mock_integration = MagicMock()
        mock_integration_cls.return_value = mock_integration
        mock_access_token = MagicMock()
        mock_access_token.token = dummy_token
        mock_integration.get_access_token.return_value = mock_access_token

        result = auth.get_github_app_installation_token(
            "https://github.example.com", "123", b"gh_private_key", "456"
        )

        mock_auth_cls.AppAuth.assert_called_once_with(123, "gh_private_key")
        mock_integration_cls.assert_called_once_with(
            base_url="https://github.example.com/api/v3", auth=mock_app_auth
        )
        mock_integration.get_access_token.assert_called_once_with(456)
        self.assertEqual(result, dummy_token)


if __name__ == "__main__":
    unittest.main()
