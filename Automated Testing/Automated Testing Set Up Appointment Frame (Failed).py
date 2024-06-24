import unittest
from unittest.mock import MagicMock
import tkinter as tk

class User:
    def __init__(self, main_window, cursor=None):
        self.root_window = main_window
        self.cursor = cursor or self.create_cursor()
        self.user_id = 123  # Example user_id
        self.all_appointment_frames = {}
        self.current_status = 'Request'
        self.format_date = MagicMock(return_value="2023-06-23")
        self.timedelta_to_time = MagicMock(return_value=MagicMock(strftime=MagicMock(return_value="10am")))

    def create_cursor(self):
        # Placeholder for actual cursor creation code
        pass

    def set_up_appointment_frame(self):
        def display_appointments(status):
            for widget in a_scrollable_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()

            status_map = {
                'Request': 'pending',
                'Ongoing': 'ongoing',
                'Completed': 'completed',
                'Rejected': 'rejected',
                'Canceled': 'canceled'
            }

            query_asc = f"""
                        SELECT ar_id, ar_detail, ar_date, ar_time, ar_doctor, 
                        ar_ifreject, appointment_prescription,
                        clinic_name, doctor_name
                        FROM appointment_request
                        WHERE ar_status = '{status_map[status]}' AND user_id = %s
                        ORDER BY ar_date, ar_time;
                        """

            if status == 'Request' or status == 'Ongoing':
                self.cursor.execute(query_asc, (self.user_id,))
                appointments = self.cursor.fetchall()
            else:
                self.cursor.execute(query_asc, (self.user_id,))
                appointments = self.cursor.fetchall()

            for i, appointment in enumerate(appointments):
                ar_id = appointment['ar_id']
                ar_detail = appointment['ar_detail']
                ar_date = self.format_date(str(appointment['ar_date']))
                ar_time = self.timedelta_to_time(appointment['ar_time'])
                ar_time = ar_time.strftime("%I%p").lstrip('0').lower()
                clinic_name = appointment['clinic_name']
                doctor_name = ('Dr. ' + appointment['doctor_name']) if appointment.get('ar_doctor') else '-'

                card_frame = tk.Frame(a_scrollable_frame, bg='white', highlightbackground='#00C196',
                                      highlightthickness=1)
                card_frame.grid(row=i + 1, column=0, columnspan=5, padx=20, pady=10, sticky='ew')

                id_label = tk.Label(card_frame, text=f"Appointment ID: {ar_id}", font=('Open Sans', 16, 'bold'),
                                    bg='white', fg='#333333')
                id_label.grid(row=0, column=0, sticky='w', padx=15, pady=(10, 5))

        # Create a canvas and a scrollbar
        a_canvas = tk.Canvas(self.root_window, borderwidth=0, background="#ffffff", width=1030, height=500, highlightthickness=0)
        a_scrollable_frame = tk.Frame(a_canvas, background="#ffffff")

        a_canvas.create_window((0, 0), window=a_scrollable_frame, anchor="nw")
        a_canvas.pack(side="left", fill="both", expand=True)

        display_appointments(self.current_status)

class TestSetupAppointmentFrame(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = User(self.root)
        self.app.cursor = MagicMock()

    def test_display_appointments_failure_no_appointments(self):
        self.app.cursor.fetchall.return_value = []  # No appointments returned from the database

        self.app.set_up_appointment_frame()
        self.app.cursor.execute.assert_called_once()
        self.assertFalse(self.app.format_date.called)  # Format date should not be called since there are no appointments

    def test_display_appointments_failure_missing_key(self):
        # Mock the fetchall method to simulate database return values with missing keys
        self.app.cursor.fetchall.return_value = [
            {'ar_id': 1, 'ar_detail': 'Checkup', 'ar_date': '2023-06-23', 'ar_time': '10:00', 'clinic_name': 'Health Clinic'}
        ]

        with self.assertRaises(KeyError):
            self.app.set_up_appointment_frame()

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()
