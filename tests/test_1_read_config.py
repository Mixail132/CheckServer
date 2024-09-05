"""
Check weather the configuration variables
have been completely read from 'ini' file.
"""


def test_config_file_has_completely_read(
    vars_read_for_test: list,
    vars_read_for_work: list,
) -> None:
    """Checks the vars number and weather they've been completely read."""
    for var in vars_read_for_test:
        assert var in vars_read_for_work

    for var in vars_read_for_work:
        assert var in vars_read_for_test

    assert len(vars_read_for_work) == len(vars_read_for_test)


def test_there_are_no_unpair_brackets(config_file_as_a_text) -> None:
    """Compares open and close square brackets quantity."""

    open_brackets = config_file_as_a_text.count("[")
    close_brackets = config_file_as_a_text.count("]")

    assert open_brackets == close_brackets
