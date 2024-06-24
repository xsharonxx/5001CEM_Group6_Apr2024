import unittest
from datetime import datetime, timedelta

def get_working(working_hours):
    time_format_12 = '%I%p'
    # Parse the working hours
    parts = working_hours.split(', ')
    if len(parts) > 2:
        working_hour = parts[1].split('-')
        start_work = working_hour[0].strip()
        start_work = datetime.strptime(start_work, time_format_12).time()
        end_work = working_hour[1].strip()
        end_work = (datetime.strptime(end_work, time_format_12) - timedelta(hours=1)).time()
        rest_days = parts[2].split()[-1]
        whole = [start_work, end_work, rest_days]
    elif len(parts) > 1:
        working_hour = parts[1].split('-')
        start_work = working_hour[0].strip()
        start_work = datetime.strptime(start_work, time_format_12).time()
        end_work = working_hour[1].strip()
        end_work = (datetime.strptime(end_work, time_format_12) - timedelta(hours=1)).time()
        whole = [start_work, end_work]
    else:
        whole = []
    return whole

class TestGetWorking(unittest.TestCase):

    def test_full_info(self):
        working_hours = "Mon-Fri, 09AM-05PM, off Sat-Sun"
        expected_output = [datetime.strptime("09AM", "%I%p").time(),
                           (datetime.strptime("05PM", "%I%p") - timedelta(hours=1)).time(),
                           "Sat-Sun"]
        self.assertEqual(get_working(working_hours), expected_output)

    def test_no_rest_days(self):
        working_hours = "Mon-Fri, 09AM-05PM"
        expected_output = [datetime.strptime("09AM", "%I%p").time(),
                           (datetime.strptime("05PM", "%I%p") - timedelta(hours=1)).time()]
        self.assertEqual(get_working(working_hours), expected_output)

    def test_invalid_format(self):
        working_hours = "09AM-05PM"
        expected_output = []
        self.assertEqual(get_working(working_hours), expected_output)

    def test_empty_string(self):
        working_hours = ""
        expected_output = []
        self.assertEqual(get_working(working_hours), expected_output)

# Optional: If you want to run the tests from command line
if __name__ == '__main__':
    unittest.main()

