import unittest
def format_date(date):
    full_date = date.split('-')
    year = full_date[0]
    month = full_date[1]
    day = full_date[2]
    months = {'01': 'January',
              '02': 'February',
              '03': 'March',
              '04': 'April',
              '05': 'May',
              '06': 'June',
              '07': 'July',
              '08': 'August',
              '09': 'September',
              '10': 'October',
              '11': 'November',
              '12': 'December'}
    month = months[month]
    return f"{day} {month} {year}"

class TestDateFormat(unittest.TestCase):
    def test_format_date(self):
        # Test cases with different input dates
        test_cases = [
            ("2023-01-15", "15 January 2023"),
            ("2022-12-25", "25 December 2022"),
            ("2024-06-22", "22 June 2024"),
            # Add more test cases as needed
        ]

        for date_str, expected_output in test_cases:
            with self.subTest(date_str=date_str):
                actual_output = format_date(date_str)  # Replace None with self if part of a class
                self.assertEqual(actual_output, expected_output)

    def test_edge_cases(self):
        # Test edge cases, like leap year, boundary conditions, etc.
        edge_cases = [
            ("2000-02-29", "29 February 2000"),
            ("2024-02-29", "29 February 2024"),
            # Add more edge cases as needed
        ]

        for date_str, expected_output in edge_cases:
            with self.subTest(date_str=date_str):
                actual_output = format_date(date_str)  # Replace None with self if part of a class
                self.assertEqual(actual_output, expected_output)


# Optional: If you want to run the tests from command line
if __name__ == '__main__':
    unittest.main()


