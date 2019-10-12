"""
Author:     Shawn Bhagat
Date:       7/23/19
Purpose:    A custom test result output logger to be used with automated tests.
            It reduces the need to type repetitive specially formatted content.
"""


class TestLogger:
    """Class that takes care of all test logging."""
        
    def __init__(self, name_col_width=35, result_col_width=10):
        """Define test constants and variables."""

        # Define types of results
        self.RESULT_PASS = "PASS"
        self.RESULT_FAIL = "FAIL"

        # Define column names and widths
        self.col_names = ["Test", "Result"]
        self.col_widths = [name_col_width, result_col_width]

    def print_separator(self, c='-'):
        """Print test separator line."""
        print(f"{c * sum(self.col_widths)}")

    def print_header(self):
        """Print column names."""
        print()
        print(f"{self.col_names[0].ljust(self.col_widths[0])}", end='')
        print(f"{self.col_names[1].ljust(self.col_widths[1])}", end='')
        print()
        self.print_separator(c='=')

    def print_test_name(self, test_name):
        """Print test name."""
        print(f"{test_name.ljust(self.col_widths[0])}", end='', flush=True)

    def print_test_result(self, test_result):
        """Print test result."""
        print(f"{test_result.ljust(self.col_widths[1])}")