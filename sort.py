"""This is the module that contains functions related to tables sorting."""

import re


def sort_contributions(collaborators, sort_column, sort_order):
    """
    This function returns a case-insensitive sorted list by chosen column and order, using natural sorting.

    Args:
        collaborators (list): A list of objects, where each object represents a collaborator.
                              Each object should have the attributes 'username', 'contribution_count', and 'commits'.
        sort_column (str): The start date of the date range for the contributor list.
        sort_order (str): The end date of the date range for the contributor list.

    Returns:
        sorted_collaborators (list): A list of objects of the same format as the one received as argument.

    """
    is_reverse = False if sort_order == "asc" else True #defaults to descending order if invalid

    def assign_type(split_text):
        return int(split_text) if split_text.isdigit() else split_text.casefold()

    def split_and_type_alphanumerical_components(input_entry):
        return [assign_type(c) for c in re.split('([0-9]+)', str(input_entry))]

    return sorted(collaborators, key=lambda x: split_and_type_alphanumerical_components(getattr(x, sort_column)), reverse=is_reverse)
