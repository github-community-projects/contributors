"""This is the test module for the env module."""

import os
import unittest
from unittest.mock import patch

import env


class TestEnv(unittest.TestCase):
    """
    Test case for the env module.
    """

    def setUp(self):
        env_keys = [
            "DRY_RUN",
            "END_DATE",
            "GH_APP_ID",
            "GH_ENTERPRISE_URL",
            "GH_APP_INSTALLATION_ID",
            "GH_APP_PRIVATE_KEY",
            "GITHUB_APP_ENTERPRISE_ONLY",
            "GH_TOKEN",
            "ORGANIZATION",
            "OUTPUT_FILENAME",
            "REPOSITORY",
            "START_DATE",
            "SHOW_AVATAR",
            "SORT_COLUMN",
            "SORT_ORDER",
            "SKIP_SUMMARY",
        ]
        for key in env_keys:
            if key in os.environ:
                del os.environ[key]

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "2022-01-01",
            "END_DATE": "2022-12-31",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
            "SHOW_AVATAR": "False",
            "SORT_COLUMN": "username",
            "SORT_ORDER": "asc",
            "SKIP_SUMMARY": "True",
        },
        clear=True,
    )
    def test_get_env_vars(self):
        """
        Test the get_env_vars function when all environment variables are set correctly.
        """

        (
            organization,
            repository_list,
            gh_app_id,
            gh_app_installation_id,
            gh_app_private_key,
            gh_app_enterprise_only,
            token,
            ghe,
            start_date,
            end_date,
            sponsor_info,
            link_to_profile,
            _output_filename,
            _show_avatar,
            sort_column,
            sort_order,
            skip_summary,
        ) = env.get_env_vars()

        self.assertEqual(organization, "org")
        self.assertEqual(repository_list, ["repo", "repo2"])
        self.assertIsNone(gh_app_id)
        self.assertIsNone(gh_app_installation_id)
        self.assertEqual(gh_app_private_key, b"")
        self.assertFalse(gh_app_enterprise_only)
        self.assertEqual(token, "token")
        self.assertEqual(ghe, "")
        self.assertEqual(start_date, "2022-01-01")
        self.assertEqual(end_date, "2022-12-31")
        self.assertFalse(sponsor_info)
        self.assertTrue(link_to_profile)
        self.assertEqual(sort_column, "username")
        self.assertEqual(sort_order, "asc")
        self.assertTrue(skip_summary)

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "2022-01-01",
            "END_DATE": "2022-12-31",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
            "SHOW_AVATAR": "False",
            "SORT_COLUMN": "username",
            "SORT_ORDER": "asc",
            "SKIP_SUMMARY": "True",
        },
        clear=True,
    )
    def test_get_env_vars_missing_values(self):
        """
        Test the get_env_vars function when none of the environment variables are set.
        Expect a ValueError to be raised.
        """

        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(str(the_exception), "GH_TOKEN environment variable not set")

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "2022/01/01",
            "END_DATE": "2022-12-31",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
            "SHOW_AVATAR": "False",
            "SORT_COLUMN": "username",
            "SORT_ORDER": "asc",
            "SKIP_SUMMARY": "True",
        },
        clear=True,
    )
    def test_get_env_vars_invalid_start_date(self):
        """
        Test the get_env_vars function when invalid start date given.
        Expect a ValueError to be raised.
        """

        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "START_DATE environment variable not in the format YYYY-MM-DD",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "",
            "END_DATE": "",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
            "SHOW_AVATAR": "False",
            "SORT_COLUMN": "username",
            "SORT_ORDER": "asc",
            "SKIP_SUMMARY": "True",
        },
        clear=True,
    )
    def test_get_env_vars_no_dates(self):
        """
        Test the get_env_vars function when all environment variables are set correctly
        and start_date and end_date are not set.
        """

        (
            organization,
            repository_list,
            gh_app_id,
            gh_app_installation_id,
            gh_app_private_key,
            gh_app_enterprise_only,
            token,
            ghe,
            start_date,
            end_date,
            sponsor_info,
            link_to_profile,
            _output_filename,
            _show_avatar,
            sort_column,
            sort_order,
            skip_summary,
        ) = env.get_env_vars()

        self.assertEqual(organization, "org")
        self.assertEqual(repository_list, ["repo", "repo2"])
        self.assertIsNone(gh_app_id)
        self.assertIsNone(gh_app_installation_id)
        self.assertEqual(gh_app_private_key, b"")
        self.assertFalse(gh_app_enterprise_only)
        self.assertEqual(token, "token")
        self.assertEqual(ghe, "")
        self.assertEqual(start_date, "")
        self.assertEqual(end_date, "")
        self.assertFalse(sponsor_info)
        self.assertTrue(link_to_profile)
        self.assertEqual(sort_column, "username")
        self.assertEqual(sort_order, "asc")
        self.assertTrue(skip_summary)

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_APP_ID": "",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "token",
            "GH_ENTERPRISE_URL": "",
            "START_DATE": "",
            "END_DATE": "",
            "SPONSOR_INFO": "False",
            "LINK_TO_PROFILE": "True",
            "OUTPUT_FILENAME": "custom-report.md",
            "SORT_COLUMN": "username",
            "SORT_ORDER": "asc",
            "SKIP_SUMMARY": "True",
        },
        clear=True,
    )
    def test_get_env_vars_custom_output_filename(self):
        """Test that OUTPUT_FILENAME overrides the default output filename."""
        (
            _organization,
            _repository_list,
            _gh_app_id,
            _gh_app_installation_id,
            _gh_app_private_key,
            _gh_app_enterprise_only,
            _token,
            _ghe,
            _start_date,
            _end_date,
            _sponsor_info,
            _link_to_profile,
            output_filename,
            _show_avatar,
            _sort_column,
            _sort_order,
            _skip_summary,
        ) = env.get_env_vars()

        self.assertEqual(output_filename, "custom-report.md")

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "../../../etc/passwd",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_path_traversal_rejected(self):
        """Test that OUTPUT_FILENAME rejects path traversal attempts."""
        with self.assertRaises(ValueError):
            env.get_env_vars()

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "/tmp/output.md",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_absolute_path_rejected(self):
        """Test that OUTPUT_FILENAME rejects absolute paths."""
        with self.assertRaises(ValueError):
            env.get_env_vars()

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "reports/output.md",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_directory_separator_rejected(self):
        """Test that OUTPUT_FILENAME rejects filenames with directory separators."""
        with self.assertRaises(ValueError):
            env.get_env_vars()

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "file;rm -rf /.md",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_special_chars_rejected(self):
        """Test that OUTPUT_FILENAME rejects filenames with special characters."""
        with self.assertRaises(ValueError):
            env.get_env_vars()

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_empty_defaults(self):
        """Test that empty OUTPUT_FILENAME defaults to contributors.md."""
        (
            _organization,
            _repository_list,
            _gh_app_id,
            _gh_app_installation_id,
            _gh_app_private_key,
            _gh_app_enterprise_only,
            _token,
            _ghe,
            _start_date,
            _end_date,
            _sponsor_info,
            _link_to_profile,
            output_filename,
            _show_avatar,
            _sort_column,
            _sort_order,
            _skip_summary,
        ) = env.get_env_vars()

        self.assertEqual(output_filename, "contributors.md")

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "  ",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_whitespace_defaults(self):
        """Test that whitespace OUTPUT_FILENAME defaults to contributors.md."""
        (
            _organization,
            _repository_list,
            _gh_app_id,
            _gh_app_installation_id,
            _gh_app_private_key,
            _gh_app_enterprise_only,
            _token,
            _ghe,
            _start_date,
            _end_date,
            _sponsor_info,
            _link_to_profile,
            output_filename,
            _show_avatar,
            _sort_column,
            _sort_order,
            _skip_summary,
        ) = env.get_env_vars()

        self.assertEqual(output_filename, "contributors.md")

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "GH_TOKEN": "token",
            "OUTPUT_FILENAME": "bad@name.md",
        },
        clear=True,
    )
    def test_get_env_vars_output_filename_invalid_chars_rejected(self):
        """Test that OUTPUT_FILENAME rejects invalid characters."""
        with self.assertRaises(ValueError):
            env.get_env_vars()

    @patch.dict(os.environ, {}, clear=True)
    def test_get_env_vars_missing_org_or_repo(self):
        """Test that an error is raised if required environment variables are not set"""
        with self.assertRaises(ValueError) as cm:
            env.get_env_vars(test=True)
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "ORGANIZATION and REPOSITORY environment variables were not set. Please set one",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "my_organization",
            "GH_APP_ID": "12345",
            "GH_APP_INSTALLATION_ID": "",
            "GH_APP_PRIVATE_KEY": "",
            "GH_TOKEN": "",
        },
        clear=True,
    )
    def test_get_env_vars_auth_with_github_app_installation_missing_inputs(self):
        """Test that an error is raised there are missing inputs for the gh app"""
        with self.assertRaises(ValueError) as context_manager:
            env.get_env_vars()
        the_exception = context_manager.exception
        self.assertEqual(
            str(the_exception),
            "GH_APP_ID set and GH_APP_INSTALLATION_ID or GH_APP_PRIVATE_KEY variable not set",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo",
            "GH_TOKEN": "token",
            "START_DATE": "2025-01-01",
            "END_DATE": "2024-01-01",
        },
        clear=True,
    )
    def test_get_env_vars_end_date_before_start_date(self):
        """Test that an error is raised when END_DATE is before START_DATE"""
        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "END_DATE ('2024-01-01') must be after START_DATE ('2025-01-01')",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo",
            "GH_TOKEN": "token",
            "START_DATE": "2024-01-01",
            "END_DATE": "2024-01-01",
        },
        clear=True,
    )
    def test_get_env_vars_equal_start_and_end_date(self):
        """Test that an error is raised when START_DATE equals END_DATE"""
        with self.assertRaises(ValueError) as cm:
            env.get_env_vars()
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "END_DATE ('2024-01-01') must be after START_DATE ('2024-01-01')",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo",
            "GH_TOKEN": "token",
            "START_DATE": "2024-01-01",
            "END_DATE": "2025-01-01",
        },
        clear=True,
    )
    def test_get_env_vars_valid_date_range(self):
        """Test that valid date range (START_DATE before END_DATE) is accepted"""
        (
            _organization,
            _repository_list,
            _gh_app_id,
            _gh_app_installation_id,
            _gh_app_private_key,
            _gh_app_enterprise_only,
            _token,
            _ghe,
            start_date,
            end_date,
            _sponsor_info,
            _link_to_profile,
            _output_filename,
            _show_avatar,
            _sort_column,
            _sort_order,
            _skip_summary,
        ) = env.get_env_vars()
        self.assertEqual(start_date, "2024-01-01")
        self.assertEqual(end_date, "2025-01-01")

    @patch.dict(os.environ, {"TEST_INT": "12.34"}, clear=True)
    def test_get_int_env_var_returns_none_for_invalid_int(self):
        """Test that invalid integer env values return None."""
        self.assertIsNone(env.get_int_env_var("TEST_INT"))

    def test_validate_date_range_invalid_date_format_raises(self):
        """Test that invalid date formats raise a ValueError."""
        with self.assertRaises(ValueError) as cm:
            env.validate_date_range("2024/01/01", "2024-02-01")
        the_exception = cm.exception
        self.assertEqual(
            str(the_exception),
            "start_date and end_date must be in the format YYYY-MM-DD",
        )

    @patch.dict(
        os.environ,
        {
            "ORGANIZATION": "org",
            "REPOSITORY": "repo,repo2",
            "GH_TOKEN": "token",
            "SORT_COLUMN": "Whatever",
            "SORT_ORDER": "ASc",
        },
        clear=True,
    )
    def test_get_env_vars_with_absent_or_invalid_sort_and_skip_summary_params(self):
        """
        Test the get_env_vars function checking that default sorting and skip_summary params
        are correctly applied in case of invalid (sort_column) or absent (skip_summary) definition, and that lowercase
        conversion is applied (sort_order)
        """

        (
            _organization,
            _repository_list,
            _gh_app_id,
            _gh_app_installation_id,
            _gh_app_private_key,
            _gh_app_enterprise_only,
            _token,
            _ghe,
            _start_date,
            _end_date,
            _sponsor_info,
            _link_to_profile,
            _output_filename,
            _show_avatar,
            sort_column,
            sort_order,
            skip_summary,
        ) = env.get_env_vars()

        self.assertEqual(sort_column, "contribution_count")
        self.assertEqual(sort_order, "asc")
        self.assertFalse(skip_summary)


if __name__ == "__main__":
    unittest.main()
