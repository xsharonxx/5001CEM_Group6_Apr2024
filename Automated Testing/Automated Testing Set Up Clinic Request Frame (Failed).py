import unittest
from unittest.mock import MagicMock
import tkinter as tk

class Clinic:
    def __init__(self, main_window, cursor=None):
        self.root_window = main_window
        self.cursor = cursor or self.create_cursor()
        self.all_clinic_request_frame = {}
        self.format_date = MagicMock(return_value="2023-06-23")

    def create_cursor(self):
        # Placeholder for actual cursor creation code
        pass

    def set_up_clinic_request_frame(self):
        def show_clinic_request():
            for widget in self.clinic_request_scrollable_frame.winfo_children():
                widget.destroy()

            # Fetch clinic requests
            query = """SELECT cr_id, cr_type, cr_reason, cr_datetime, cr_detail, 
                       clinic_name, clinic_contact, user_email, clinic_id
                       FROM clinic_request
                       WHERE cr_status = 'pending'
                       ORDER BY cr_datetime ASC;"""
            self.cursor.execute(query)
            clinic_requests = self.cursor.fetchall()

            if not clinic_requests:
                no_requests_label = tk.Label(self.clinic_request_scrollable_frame, text="No clinic requests found.",
                                             font=('Open Sans', 12, 'bold'), bg='white', fg='red')
                no_requests_label.pack(padx=440, pady=30)
            else:
                for i, request in enumerate(clinic_requests):
                    cr_id = request['cr_id']
                    cr_type = request['cr_type']
                    cr_reason = request['cr_reason']
                    cr_datetime = request['cr_datetime']
                    cr_datetime = self.format_date(str(cr_datetime))
                    cr_detail = request['cr_detail']
                    clinic_name = request['clinic_name']
                    clinic_contact = request['clinic_contact']
                    clinic_email = request['user_email']
                    clinic_id = request['clinic_id']

                    card_frame = tk.Frame(self.clinic_request_scrollable_frame, bg='white', highlightbackground='#00C196',
                                          highlightthickness=1)
                    card_frame.grid(row=i + 1, column=0, columnspan=5, padx=25, pady=10, sticky='ew')

                    id_label = tk.Label(card_frame, text=f"Request ID: {cr_id}", font=('Open Sans', 16, 'bold'), bg='white',
                                        fg='#333333')
                    id_label.grid(row=0, column=0, sticky='w', padx=15, pady=(10, 5))

        # Create a canvas and a scrollbar
        clinic_request_canvas = tk.Canvas(self.root_window, borderwidth=0, background="#ffffff", width=1030, height=510, highlightthickness=0)
        self.clinic_request_scrollable_frame = tk.Frame(clinic_request_canvas, background="#ffffff")

        clinic_request_canvas.create_window((0, 0), window=self.clinic_request_scrollable_frame, anchor="nw")
        clinic_request_canvas.pack(side="left", fill="both", expand=True)

        show_clinic_request()

class TestSetupClinicRequestFrame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = Clinic(self.root)
        self.app.cursor = MagicMock()

    def test_show_clinic_request_failure_no_requests(self):
        self.app.cursor.fetchall.return_value = []  # No requests returned from the database

        self.app.set_up_clinic_request_frame()
        self.app.cursor.execute.assert_called_once()
        self.assertFalse(self.app.format_date.called)  # Format date should not be called since there are no requests

        # Check if the "No clinic requests found" label is present
        labels = [child.cget("text") for child in self.app.clinic_request_scrollable_frame.winfo_children() if isinstance(child, tk.Label)]
        self.assertIn("No clinic requests found.", labels, "Expected 'No clinic requests found.' not found in the labels.")

    def test_show_clinic_request_failure_missing_key(self):
        # Mock the fetchall method to simulate database return values with missing keys
        self.app.cursor.fetchall.return_value = [
            {'cr_id': 1, 'cr_type': 'join', 'cr_reason': 'Expanding services', 'cr_datetime': '2023-06-23', 'clinic_name': 'New Clinic', 'clinic_contact': '1234567890', 'user_email': 'clinic@example.com'}
        ]

        # Ensure KeyError is raised due to the missing 'cr_detail' key
        try:
            self.app.set_up_clinic_request_frame()
        except KeyError as e:
            self.fail(f"KeyError was raised: {e}")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()






















