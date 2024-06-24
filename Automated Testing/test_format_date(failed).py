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

    def test_format_date_failure(self):
        # Test a case where the function should fail
        input_date = "2023-06-15"
        expected_output = "15 June 2023"
        actual_output = format_date(input_date)
        self.assertNotEqual(actual_output, expected_output, "Both are not same value")

# Optional: If you want to run the tests from command line
if __name__ == '__main__':
    unittest.main()

