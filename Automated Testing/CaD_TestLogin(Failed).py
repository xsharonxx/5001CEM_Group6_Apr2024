import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from CaD_FinalVersion import LoginRegister


class TestLogin(unittest.TestCase):
    def setUp(self):
        # Mocking the iconphoto method
        self.iconphoto_patcher = patch.object(tk.Tk, 'iconphoto')
        self.mock_iconphoto = self.iconphoto_patcher.start()

        self.window = LoginRegister()
        self.mock_login_ui = MagicMock()
        self.mock_login_ui.l_email_entry = MagicMock()
        self.mock_login_ui.l_password_entry = MagicMock()
        self.mock_login_ui.l_validate_login_label = MagicMock()

        # Mocking the database cursor
        self.cursor_patcher = patch('CaD_FinalVersion.database.cursor', new=MagicMock())
        self.mock_cursor = self.cursor_patcher.start()
        self.mock_cursor.fetchone.return_value = None

        # Mock the config method of the label
        self.mock_login_ui.l_validate_login_label.config = MagicMock()

        # Assign the mocked login UI to the show_login method
        self.window.show_login = MagicMock(return_value=self.mock_login_ui)
        self.window.show_login()

    def tearDown(self):
        self.cursor_patcher.stop()
        self.iconphoto_patcher.stop()

    def mock_login(self):
        if self.mock_login_ui.l_email_entry.cget('fg') == '#333333' and self.mock_login_ui.l_password_entry.cget('fg') == '#333333':
            user_email = self.mock_login_ui.l_email_entry.get().lower()
            user_password = self.mock_login_ui.l_password_entry.get()
            if user_email.endswith('@gmail.com'):
                self.mock_cursor.execute('''SELECT user_password FROM user WHERE user_email=%s''', (user_email,))
                password = self.mock_cursor.fetchone()
                if password:
                    if user_password == password[0]:
                        self.mock_cursor.execute('''SELECT user_id, user_type FROM user WHERE user_email=%s AND user_password=%s''',
                                                 (user_email, user_password))
                        user_id_type = self.mock_cursor.fetchone()
                        if user_id_type:
                            self.mock_login_ui.l_validate_login_label.config(text='')
                            self.mock_login_ui.l_validate_login_label.update_idletasks()
                    else:
                        self.mock_login_ui.l_validate_login_label.config(text='Incorrect Password')
                else:
                    self.mock_login_ui.l_validate_login_label.config(text='Email does not exist')
            else:
                self.mock_login_ui.l_validate_login_label.config(text='Invalid Email Format')
        else:
            self.mock_login_ui.l_validate_login_label.config(text='Please fill in all the details')

    def test_empty_email_and_password(self):
        self.mock_login_ui.l_email_entry.get.return_value = ''
        self.mock_login_ui.l_password_entry.get.return_value = ''
        self.mock_login_ui.l_email_entry.cget.return_value = '#858585'
        self.mock_login_ui.l_password_entry.cget.return_value = '#858585'

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')

    def test_empty_email(self):
        self.mock_login_ui.l_email_entry.get.return_value = ''
        self.mock_login_ui.l_password_entry.get.return_value = 'password'
        self.mock_login_ui.l_email_entry.cget.return_value = '#858585'
        self.mock_login_ui.l_password_entry.cget.return_value = '#333333'

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')

    def test_empty_password(self):
        self.mock_login_ui.l_email_entry.get.return_value = 'email'
        self.mock_login_ui.l_password_entry.get.return_value = ''
        self.mock_login_ui.l_email_entry.cget.return_value = '#333333'
        self.mock_login_ui.l_password_entry.cget.return_value = '#858585'

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')

    def test_invalid_email_format(self):
        self.mock_login_ui.l_email_entry.get.return_value = 'email'
        self.mock_login_ui.l_password_entry.get.return_value = 'password'
        self.mock_login_ui.l_email_entry.cget.return_value = '#333333'
        self.mock_login_ui.l_password_entry.cget.return_value = '#333333'

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')

    def test_not_exist_email(self):
        self.mock_login_ui.l_email_entry.get.return_value = 'email@gmail.com'
        self.mock_login_ui.l_password_entry.get.return_value = 'password'
        self.mock_login_ui.l_email_entry.cget.return_value = '#333333'
        self.mock_login_ui.l_password_entry.cget.return_value = '#333333'

        self.mock_cursor.fetchone.side_effect = [None]

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')

    def test_incorrect_password(self):
        self.mock_login_ui.l_email_entry.get.return_value = 'test@gmail.com'
        self.mock_login_ui.l_password_entry.get.return_value = '00000000'
        self.mock_login_ui.l_email_entry.cget.return_value = '#333333'
        self.mock_login_ui.l_password_entry.cget.return_value = '#333333'

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        self.mock_cursor.fetchone.side_effect = [('890890890',)]

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')

    def test_success_login(self):
        self.mock_login_ui.l_email_entry.get.return_value = 'test@gmail.com'
        self.mock_login_ui.l_password_entry.get.return_value = '890890890'
        self.mock_login_ui.l_email_entry.cget.return_value = '#333333'
        self.mock_login_ui.l_password_entry.cget.return_value = '#333333'

        self.mock_cursor.fetchone.side_effect = [('890890890',), (1, 'user')]

        # Assign the mock login function to simulate the login process
        self.mock_login_ui.login = self.mock_login

        # Call the mock login function
        self.mock_login_ui.login()

        # Verify the label's config method was called with the expected argument
        self.mock_login_ui.l_validate_login_label.config.assert_called_with(text='Unexpected text')


if __name__ == '__main__':
    unittest.main()
