"""
A GitHub Action that given an organization or repository,
produces information about the contributors over the specified time period.
"""

import datetime
import os
import re
from os.path import dirname, join

from dotenv import load_dotenv


def get_bool_env_var(env_var_name: str, default: bool = False) -> bool:
    """Get a boolean environment variable.

    Args:
        env_var_name: The name of the environment variable to retrieve.
        default: The default value to return if the environment variable is not set.

    Returns:
        The value of the environment variable as a boolean.
    """
    ev = os.environ.get(env_var_name, "")
    if ev == "" and default:
        return default
    return ev.strip().lower() == "true"


def get_int_env_var(env_var_name: str) -> int | None:
    """Get an integer environment variable.

    Args:
        env_var_name: The name of the environment variable to retrieve.

    Returns:
        The value of the environment variable as an integer or None.
    """
    env_var = os.environ.get(env_var_name)
    if env_var is None or not env_var.strip():
        return None
    try:
        return int(env_var)
    except ValueError:
        return None


def validate_date_format(env_var_name: str) -> str:
    """Validate the date format of the environment variable.

    Does nothing if the environment variable is not set.

    Args:
        env_var_name: The name of the environment variable to retrieve.

    Returns:
        The value of the environment variable as a string.
    """
    date_to_validate = os.getenv(env_var_name, "")

    if not date_to_validate:
        return date_to_validate

    pattern = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(date_to_validate, pattern).replace(
            tzinfo=datetime.timezone.utc
        )
    except ValueError as exc:
        raise ValueError(
            f"{env_var_name} environment variable not in the format YYYY-MM-DD"
        ) from exc
    return date_to_validate


def validate_date_range(start_date: str, end_date: str) -> None:
    """Validate that start_date is before end_date.

    Does nothing if either date is not set.

    Args:
        start_date: The start date string in YYYY-MM-DD format.
        end_date: The end date string in YYYY-MM-DD format.

    Raises:
        ValueError: If end_date is before or equal to start_date.
    """
    if not start_date or not end_date:
        return

    pattern = "%Y-%m-%d"
    try:
        start = (
            datetime.datetime.strptime(start_date, pattern)
            .replace(tzinfo=datetime.timezone.utc)
            .date()
        )
        end = (
            datetime.datetime.strptime(end_date, pattern)
            .replace(tzinfo=datetime.timezone.utc)
            .date()
        )
    except ValueError as exc:
        raise ValueError(
            "start_date and end_date must be in the format YYYY-MM-DD"
        ) from exc

    if end <= start:
        raise ValueError(
            f"END_DATE ('{end_date}') must be after START_DATE ('{start_date}')"
        )


def validate_output_filename(output_filename: str) -> str:
    """Validate OUTPUT_FILENAME and return a safe filename."""
    if not output_filename:
        return "contributors.md"

    filename = output_filename.strip()
    if not filename:
        return "contributors.md"

    if os.path.isabs(filename):
        raise ValueError("OUTPUT_FILENAME must be a filename only, not a path")

    if "/" in filename or "\\" in filename:
        raise ValueError("OUTPUT_FILENAME must be a filename only, not a path")

    if not re.fullmatch(r"[A-Za-z0-9._-]+", filename):
        raise ValueError("OUTPUT_FILENAME contains invalid characters")

    return filename


def get_env_vars(
    test: bool = False,
) -> tuple[
    str | None,
    list[str],
    int | None,
    int | None,
    bytes,
    bool,
    str,
    str,
    str,
    str,
    bool,
    bool,
    str,
    bool,
]:
    """
    Get the environment variables for use in the action.

    Args:
        None

    Returns:
        organization (str): the organization to get contributor information for
        repository_list (list[str]): A list of the repositories to get contributor information for
        gh_app_id (int | None): The GitHub App ID to use for authentication
        gh_app_installation_id (int | None): The GitHub App Installation ID to use for authentication
        gh_app_private_key_bytes (bytes): The GitHub App Private Key as bytes to use for authentication
        gh_app_enterprise_only (bool): Set this to true if the GH APP is created on GHE and needs to communicate with GHE api only
        token (str): The GitHub token to use for authentication
        ghe (str): The GitHub Enterprise URL to use for authentication
        start_date (str): The start date to get contributor information from
        end_date (str): The end date to get contributor information to
        sponsor_info (str): Whether to get sponsor information on the contributor
        link_to_profile (str): Whether to link username to Github profile in markdown output
    """

    if not test:
        dotenv_path = join(dirname(__file__), ".env")
        load_dotenv(dotenv_path)

    organization = os.getenv("ORGANIZATION")
    repositories_str = os.getenv("REPOSITORY")
    # Either organization or repository must be set
    if not organization and not repositories_str:
        raise ValueError(
            "ORGANIZATION and REPOSITORY environment variables were not set. Please set one"
        )

    gh_app_id = get_int_env_var("GH_APP_ID")
    gh_app_private_key_bytes = os.environ.get("GH_APP_PRIVATE_KEY", "").encode("utf8")
    gh_app_installation_id = get_int_env_var("GH_APP_INSTALLATION_ID")
    gh_app_enterprise_only = get_bool_env_var("GITHUB_APP_ENTERPRISE_ONLY")

    if gh_app_id and (not gh_app_private_key_bytes or not gh_app_installation_id):
        raise ValueError(
            "GH_APP_ID set and GH_APP_INSTALLATION_ID or GH_APP_PRIVATE_KEY variable not set"
        )

    token = os.getenv("GH_TOKEN", "")
    if (
        not gh_app_id
        and not gh_app_private_key_bytes
        and not gh_app_installation_id
        and not token
    ):
        raise ValueError("GH_TOKEN environment variable not set")

    ghe = os.getenv("GH_ENTERPRISE_URL", default="").strip()

    start_date = validate_date_format("START_DATE")
    end_date = validate_date_format("END_DATE")
    validate_date_range(start_date, end_date)

    sponsor_info = get_bool_env_var("SPONSOR_INFO", False)
    link_to_profile = get_bool_env_var("LINK_TO_PROFILE", False)
    output_filename = validate_output_filename(
        os.getenv("OUTPUT_FILENAME", "contributors.md")
    )
    show_avatar = get_bool_env_var("SHOW_AVATAR", False)

    # Separate repositories_str into a list based on the comma separator
    repositories_list = []
    if repositories_str:
        repositories_list = [
            repository.strip() for repository in repositories_str.split(",")
        ]

    return (
        organization,
        repositories_list,
        gh_app_id,
        gh_app_installation_id,
        gh_app_private_key_bytes,
        gh_app_enterprise_only,
        token,
        ghe,
        start_date,
        end_date,
        sponsor_info,
        link_to_profile,
        output_filename,
        show_avatar,
    )
