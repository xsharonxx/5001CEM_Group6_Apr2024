import unittest
from datetime import timedelta, time
import tkinter as tk
from CaD_FinalVersion import User


class TestTimedeltaToTime(unittest.TestCase):
    def setUp(self):
        # Create a hidden root window
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window

        # Pass the hidden root window to the User class
        self.obj = User(main_window=self.root)

    def tearDown(self):
        # Destroy the hidden root window after each test
        self.root.destroy()

    def test_seconds_timedelta(self):
        td = timedelta(seconds=3605)
        expected_time = time(1, 0, 5)
        result = self.obj.timedelta_to_time(td)

        # Print actual and expected results
        print(f"Test Seconds - Expected: {expected_time}, Actual: {result}")
        print(f"Test Seconds - Expected Type: {type(expected_time)}, Actual Type: {type(result)}")

        # Check the result value
        self.assertEqual(result, expected_time)

        # Check the result type
        self.assertIsInstance(result, time)

    def test_minutes_and_seconds_timedelta(self):
        td = timedelta(minutes=76, seconds=30)
        expected_time = time(1, 16, 30)
        result = self.obj.timedelta_to_time(td)

        # Print actual and expected results
        print(f"Test Minutes and Seconds - Expected: {expected_time}, Actual: {result}")
        print(f"Test Minutes and Seconds - Expected Type: {type(expected_time)}, Actual Type: {type(result)}")

        # Check the result value
        self.assertEqual(result, expected_time)

        # Check the result type
        self.assertIsInstance(result, time)

    def test_hours_minutes_seconds_timedelta(self):
        td = timedelta(hours=1, minutes=30, seconds=15)
        expected_time = time(1, 30, 15)
        result = self.obj.timedelta_to_time(td)

        # Print actual and expected results
        print(f"Test Hours, Minutes, and Seconds - Expected: {expected_time}, Actual: {result}")
        print(f"Test Hours, Minutes, and Seconds - Expected Type: {type(expected_time)}, Actual Type: {type(result)}")

        # Check the result value
        self.assertEqual(result, expected_time)

        # Check the result type
        self.assertIsInstance(result, time)


if __name__ == '__main__':
    unittest.main()
