import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from io import BytesIO
from tkinter import filedialog
import os
from tkinter import messagebox
import datetime
from tkcalendar import Calendar
from datetime import datetime, timedelta, time
import io
import imghdr

database = mysql.connector.connect(host="localhost", user="root", password="Yenling12345", database="cad")
cursor = database.cursor()


def load_image(description, width, height):
    cursor.execute('''SELECT app_image_data FROM app_image WHERE app_image_description=%s''', (description,))
    image_data = cursor.fetchone()
    if image_data:
        image_stream = BytesIO(image_data[0])
        img = Image.open(image_stream)
        resized_img = img.resize((width, height), Image.LANCZOS)
        tk_image = ImageTk.PhotoImage(resized_img)
        return tk_image


class LoginRegister:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Call a Doctor')
        self.window.geometry('1050x600')
        icon = load_image('icon', 48, 48)
        self.window.iconphoto(False, icon)

        self.frame = tk.Frame(self.window, width=1050, height=600, bg='white')
        self.frame.pack()

        self.get_started_background = load_image('bg get started', 1050, 600)
        self.icon = load_image('icon', 100, 90)
        self.lfr_background = load_image('bg login_register as', 1050, 600)
        self.eye_closed_image = load_image('eye closed', 24, 24)
        self.eye_opened_image = load_image('eye opened', 24, 24)

        self.image_var = None
        self.user_window = None
        self.clinic_window = None
        self.doctor_window = None
        self.admin_window = None

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('small_green.TButton', border=0, relief='flat', background='#0EBE7F', foreground='#FFFFFF',
                        font=('Rubik', 12, 'bold'))
        style.map('small_green.TButton', background=[('active', '#66C5A3')])
        style.configure('big_green.TButton', border=0, relief='flat', background='#0EBE7F', foreground='#FFFFFF',
                        font=('Rubik', 20, 'bold'))
        style.map('big_green.TButton', background=[('active', '#66C5A3')])
        style.configure('grey_word.TButton', border=0, relief='flat', background='white', foreground='#7E869F',
                        font=('Rubik', 9))
        style.map('grey_word.TButton', background=[('active', 'white')], foreground=[('active', '#4F5871')])
        style.configure('black_word.TButton', border=0, relief='flat', background='#08D5A7', foreground='#333333',
                        font=('Rubik', 8, 'bold'))
        style.map('black_word.TButton', background=[('active', '#08D5A7')], foreground=[('active', 'white')])
        style.configure('eye_closed_grey.TButton', border=0, relief='flat', background='#F5F5F5', image=self.eye_closed_image)
        style.map('eye_closed_grey.TButton', background=[('active', '#F5F5F5')])
        style.configure('eye_opened_grey.TButton', border=0, relief='flat', background='#F5F5F5', image=self.eye_opened_image)
        style.map('eye_opened_grey.TButton', background=[('active', '#F5F5F5')])
        style.configure('eye_closed_green.TButton', border=0, relief='flat', background='#D0F9EF', image=self.eye_closed_image)
        style.map('eye_closed_green.TButton', background=[('active', '#D0F9EF')])
        style.configure('eye_opened_green.TButton', border=0, relief='flat', background='#D0F9EF', image=self.eye_opened_image)
        style.map('eye_opened_green.TButton', background=[('active', '#D0F9EF')])
        style.configure('selection.TButton', border=0, relief='flat', background='#D0F9EF', foreground='#3DAEC7',
                        font=('Rubik', 12, 'bold'))
        style.map('selection.TButton', background=[('active', '#D0F9EF')], foreground=[('active', '#0B8FAC')])

    def run(self):
        self.show_get_started()
        self.window.mainloop()

    def reset(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        self.image_var = None

    def show_get_started(self):
        self.reset()
        gs_background_label = tk.Label(self.frame, image=self.get_started_background)
        gs_background_label.pack()

        gs_icon_label = tk.Label(self.frame, image=self.icon, bg='white')
        gs_icon_label.place(x=760, y=50)
        gs_text1 = tk.Label(self.frame, text='Call a Doctor', font=('Rubik', 40, 'bold'), bg='white', fg='#333333')
        gs_text1.place(x=645, y=150)
        gs_text2 = tk.Label(self.frame, text='Your Ultimate Doctor', font=('Rubik', 18), bg='white', fg='#888EA1')
        gs_text2.place(x=700, y=240)
        gs_text3 = tk.Label(self.frame, text='Appointment Booking App', font=('Rubik', 18), bg='white', fg='#888EA1')
        gs_text3.place(x=672, y=275)

        gs_get_started_button = ttk.Button(self.frame, text='Get Started', style='big_green.TButton', width=18, padding=6,
                                           cursor='hand2', command=lambda: self.show_register_as())
        gs_get_started_button.place(x=675, y=370)
        gs_login_grey_button = ttk.Button(self.frame, text='Login', style='grey_word.TButton', cursor='hand2', width=5,
                                          command=lambda: self.show_login())
        gs_login_grey_button.place(x=790, y=425)

    def show_register_as(self):
        self.reset()
        ra_background_label = tk.Label(self.frame, image=self.lfr_background)
        ra_background_label.pack()

        ra_text1 = tk.Label(self.frame, text='Register as', font=('Open Sans', 30, 'bold'), bg='white', fg='#333333')
        ra_text1.place(x=680, y=70)

        ra_user_button = ttk.Button(self.frame, text='Normal User', style='big_green.TButton', cursor='hand2', width=18, padding=12,
                                    command=lambda: self.show_registering_user())
        ra_user_button.place(x=640, y=200)
        ra_text2 = tk.Label(self.frame, text='OR', font=('Rubik', 14), bg='white', fg='#888EA1')
        ra_text2.place(x=770, y=290)
        ra_clinic_button = ttk.Button(self.frame, text='Clinic', style='big_green.TButton', cursor='hand2', width=18, padding=12,
                                      command=lambda: self.show_registering_clinic())
        ra_clinic_button.place(x=640, y=350)

        ra_text3 = tk.Label(self.frame, text='Have an account?', bg='#08D5A7', fg='#333333', font=('Rubik', 8, 'bold'))
        ra_text3.place(x=840, y=570)
        ra_login_black_button = ttk.Button(self.frame, text='Login', style='black_word.TButton', cursor='hand2', width=8,
                                           command=lambda: self.show_login())
        ra_login_black_button.place(x=940, y=565)

    def show_login(self):
        def login():
            self.window.focus_set()

            if l_email_entry.cget('fg') == '#333333' and l_password_entry.cget('fg') == '#333333':
                user_email = l_email_entry.get().lower()
                user_password = l_password_entry.get()
                if user_email.endswith('@gmail.com'):
                    cursor.execute('''SELECT user_password FROM user WHERE user_email=%s''', (user_email,))
                    password = cursor.fetchone()
                    if password:
                        if user_password == password[0]:
                            cursor.execute('''SELECT user_id, user_type FROM user WHERE user_email=%s AND user_password=%s''',
                                           (user_email, user_password))
                            user_id_type = cursor.fetchone()
                            if user_id_type:
                                l_validate_login_label.config(text='')
                                l_validate_login_label.update_idletasks()
                                self.window.withdraw()
                                user_id = user_id_type[0]
                                user_type = user_id_type[1]
                                if user_type == 'user':
                                    if self.user_window:
                                        self.user_window.run()
                                    else:
                                        self.user_window = User(self.window, user_id)
                                        self.user_window.run()
                                elif user_type == 'clinic':
                                    if self.clinic_window:
                                        self.clinic_window.run()
                                    else:
                                        self.clinic_window = Clinic(self.window, user_id)
                                        self.clinic_window.run()
                                elif user_type == 'doctor':
                                    if self.doctor_window:
                                        self.doctor_window.run()
                                    else:
                                        self.doctor_window = Doctor(self.window, user_id)
                                        self.doctor_window.run()
                                elif user_type == 'admin':
                                    if self.admin_window:
                                        self.admin_window.run()
                                    else:
                                        self.admin_window = Admin(self.window, user_id)
                                        self.admin_window.run()
                                self.show_login()
                        else:
                            l_validate_login_label.config(text='Incorrect Password ')
                    else:
                        l_validate_login_label.config(text='Email does not exist')
                else:
                    l_validate_login_label.config(text='Invalid Email Format')
            else:
                l_validate_login_label.config(text='Please fill in all the details')

        self.reset()
        l_background_label = tk.Label(self.frame, image=self.lfr_background)
        l_background_label.pack()

        l_text1 = tk.Label(self.frame, text='Login', font=('Open Sans', 30, 'bold'), bg='white', fg='#333333')
        l_text1.place(x=725, y=70)
        l_text2 = tk.Label(self.frame, text='Hi, Welcome Back!', font=('Rubik', 14), bg='white', fg='#888EA1')
        l_text2.place(x=700, y=130)

        l_email_label = tk.Label(self.frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        l_email_label.place(x=620, y=200)
        l_email_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                       highlightthickness=0.5)
        l_email_entry_frame.place(x=625, y=230)
        l_email_entry = tk.Entry(l_email_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35)
        l_email_entry.place(x=10, y=12)
        l_email_entry.insert(0, 'Enter Your Email')
        l_email_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', l_email_entry))
        l_email_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', l_email_entry, 'Enter Your Email'))
        l_email_entry.bind('<Return>', lambda event: login())

        l_password_label = tk.Label(self.frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        l_password_label.place(x=620, y=295)
        l_password_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        l_password_entry_frame.place(x=625, y=325)
        l_password_entry = tk.Entry(l_password_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35,
                                    show='')
        l_password_entry.place(x=10, y=12)
        l_password_entry.insert(0, 'Enter Your Password')
        l_password_eye_closed_button = ttk.Button(l_password_entry_frame, style='eye_closed_grey.TButton', cursor='hand2')
        l_password_eye_closed_button.place(x=270, y=2)
        l_password_eye_opened_button = ttk.Button(l_password_entry_frame, style='eye_opened_grey.TButton', cursor='hand2')
        l_password_visibility = tk.Label(l_password_entry_frame, text='Close')
        l_password_eye_closed_button.config(command=lambda: self.show_hide_password(l_password_entry, l_password_eye_opened_button,
                                                                                    l_password_eye_closed_button, l_password_visibility))
        l_password_eye_opened_button.config(command=lambda: self.show_hide_password(l_password_entry, l_password_eye_opened_button,
                                                                                    l_password_eye_closed_button, l_password_visibility))
        l_password_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', l_password_entry, l_password_visibility))
        l_password_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', l_password_entry, 'Enter Your Password'))
        l_password_entry.bind('<Return>', lambda event: login())

        l_login_button = ttk.Button(self.frame, text='Login', style='small_green.TButton', cursor='hand2', width=20, padding=5,
                                    command=lambda: login())
        l_login_button.place(x=690, y=410)
        l_validate_login_label = tk.Label(self.frame, text='', bg='white', fg='red', font=('Open Sans', 8), anchor='center',
                                          width=32)
        l_validate_login_label.place(x=689, y=389)

        l_forgot_password_grey_button = ttk.Button(self.frame, text='Forgot Password', style='grey_word.TButton', cursor='hand2',
                                                   width=15, command=lambda: self.show_forgot_password())
        l_forgot_password_grey_button.place(x=725, y=445)

        l_text3 = tk.Label(self.frame, text='Don\'t have an account?', bg='#08D5A7', fg='#333333', font=('Rubik', 8, 'bold'))
        l_text3.place(x=810, y=570)
        l_register_as_black_button = ttk.Button(self.frame, text='Register', style='black_word.TButton', cursor='hand2', width=8,
                                                command=lambda: self.show_register_as())
        l_register_as_black_button.place(x=940, y=565)

    def show_forgot_password(self):
        def update_password():
            self.window.focus_set()

            if fp_email_entry.cget('fg') == '#333333'\
                    and fp_password_entry.cget('fg') == '#333333' and fp_confirmed_entry.cget('fg') == '#333333':
                user_email = fp_email_entry.get().lower()
                if user_email.endswith('@gmail.com'):
                    cursor.execute('''SELECT user_id FROM user WHERE user_email=%s''', (user_email,))
                    user_id = cursor.fetchone()
                    if user_id:
                        if len(fp_password_entry.get()) >= 8:
                            if fp_password_entry.get() == fp_confirmed_entry.get():
                                fp_validate_update_label.config(text='')
                                new_password = fp_password_entry.get()
                                cursor.execute('''UPDATE user SET user_password=%s WHERE user_id=%s''', (new_password, user_id[0]))
                                database.commit()
                                messagebox.showinfo("Success", 'Password updated successfully')
                                self.show_login()
                            else:
                                fp_validate_update_label.config(text='Password does not match')
                        else:
                            fp_validate_update_label.config(text='Minimum 8 characters of Password')
                    else:
                        fp_validate_update_label.config(text='Email does not exist')
                else:
                    fp_validate_update_label.config(text='Invalid Email Format')
            else:
                fp_validate_update_label.config(text='Please fill in all the details')

        self.reset()
        fp_background_label = tk.Label(self.frame, image=self.lfr_background)
        fp_background_label.pack()

        fp_text1 = tk.Label(self.frame, text='Forgot Password', font=('Open Sans', 30, 'bold'), bg='white', fg='#333333')
        fp_text1.place(x=620, y=35)

        fp_email_label = tk.Label(self.frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        fp_email_label.place(x=620, y=135)
        fp_email_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        fp_email_entry_frame.place(x=625, y=165)
        fp_email_entry = tk.Entry(fp_email_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35)
        fp_email_entry.place(x=10, y=12)
        fp_email_entry.insert(0, 'Enter Your Email')
        fp_email_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', fp_email_entry))
        fp_email_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', fp_email_entry, 'Enter Your Email'))
        fp_email_entry.bind('<Return>', lambda event: update_password())

        fp_password_label = tk.Label(self.frame, text='New Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        fp_password_label.place(x=620, y=230)
        fp_password_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        fp_password_entry_frame.place(x=625, y=260)
        fp_password_entry = tk.Entry(fp_password_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35,
                                     show='')
        fp_password_entry.place(x=10, y=12)
        fp_password_entry.insert(0, 'Enter New Password')
        fp_password_eye_closed_button = ttk.Button(fp_password_entry_frame, style='eye_closed_grey.TButton', cursor='hand2')
        fp_password_eye_closed_button.place(x=270, y=2)
        fp_password_eye_opened_button = ttk.Button(fp_password_entry_frame, style='eye_opened_grey.TButton', cursor='hand2')
        fp_password_visibility = tk.Label(fp_password_entry_frame, text='Close')
        fp_password_eye_closed_button.config(command=lambda: self.show_hide_password(fp_password_entry, fp_password_eye_opened_button,
                                                                                     fp_password_eye_closed_button,
                                                                                     fp_password_visibility))
        fp_password_eye_opened_button.config(command=lambda: self.show_hide_password(fp_password_entry, fp_password_eye_opened_button,
                                                                                     fp_password_eye_closed_button,
                                                                                     fp_password_visibility))
        fp_password_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', fp_password_entry, fp_password_visibility))
        fp_password_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', fp_password_entry, 'Enter New Password'))
        fp_password_entry.bind('<Return>', lambda event: update_password())

        fp_confirmed_label = tk.Label(self.frame, text='Re-enter New Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        fp_confirmed_label.place(x=620, y=325)
        fp_confirmed_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        fp_confirmed_entry_frame.place(x=625, y=355)
        fp_confirmed_entry = tk.Entry(fp_confirmed_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35,
                                      show='')
        fp_confirmed_entry.place(x=10, y=12)
        fp_confirmed_entry.insert(0, 'Re-enter New Password')
        fp_confirmed_eye_closed_button = ttk.Button(fp_confirmed_entry_frame, style='eye_closed_grey.TButton', cursor='hand2')
        fp_confirmed_eye_closed_button.place(x=270, y=2)
        fp_confirmed_eye_opened_button = ttk.Button(fp_confirmed_entry_frame, style='eye_opened_grey.TButton', cursor='hand2')
        fp_confirmed_visibility = tk.Label(fp_confirmed_entry_frame, text='Close')
        fp_confirmed_eye_closed_button.config(command=lambda: self.show_hide_password(fp_confirmed_entry, fp_confirmed_eye_opened_button,
                                                                                      fp_confirmed_eye_closed_button,
                                                                                      fp_confirmed_visibility))
        fp_confirmed_eye_opened_button.config(command=lambda: self.show_hide_password(fp_confirmed_entry, fp_confirmed_eye_opened_button,
                                                                                      fp_confirmed_eye_closed_button,
                                                                                      fp_confirmed_visibility))
        fp_confirmed_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', fp_confirmed_entry, fp_confirmed_visibility))
        fp_confirmed_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', fp_confirmed_entry,
                                                                                   'Re-enter New Password'))
        fp_confirmed_entry.bind('<Return>', lambda event: update_password())

        fp_back_button = ttk.Button(self.frame, text='Back', style='small_green.TButton', cursor='hand2', width=20, padding=5,
                                    command=lambda: self.show_login())
        fp_back_button.place(x=690, y=440)
        fp_update_pass_button = ttk.Button(self.frame, text='Update Password', style='small_green.TButton', cursor='hand2', width=20,
                                           padding=5, command=lambda: update_password())
        fp_update_pass_button.place(x=690, y=490)
        fp_validate_update_label = tk.Label(self.frame, text='', font=('Open Sans', 8), bg='white', fg='red', anchor='center', width=32)
        fp_validate_update_label.place(x=689, y=419)

        fp_text3 = tk.Label(self.frame, text='Don\'t have an account?', bg='#08D5A7', fg='#333333', font=('Rubik', 8, 'bold'))
        fp_text3.place(x=810, y=570)
        fp_register_as_black_button = ttk.Button(self.frame, text='Register', style='black_word.TButton', cursor='hand2', width=8,
                                                 command=lambda: self.show_register_as())
        fp_register_as_black_button.place(x=940, y=565)

    def show_registering_user(self):
        def register_user():
            self.window.focus_set()

            if ru_name_entry.cget('fg') == '#333333' and ru_ic_passport_entry.cget('fg') == '#333333' \
                    and ru_gender_entry.cget('fg') == '#333333' and ru_address_entry.cget('fg') == '#333333' \
                    and ru_contact_entry.cget('fg') == '#333333' and ru_email_entry.cget('fg') == '#333333' \
                    and ru_password_entry.cget('fg') == '#333333' and ru_confirmed_entry.cget('fg') == '#333333':
                user_email = ru_email_entry.get().lower()
                if user_email.endswith('@gmail.com'):
                    cursor.execute('''SELECT user_email FROM user WHERE user_email=%s''', (user_email, ))
                    existing_email = cursor.fetchone()
                    if not existing_email:
                        if len(ru_password_entry.get()) >= 8:
                            if ru_password_entry.get() == ru_confirmed_entry.get():
                                ru_validate_register_label.config(text='')
                                cursor.execute('''INSERT INTO user (user_email, user_password, user_type) VALUES (%s, %s, %s)''',
                                               (user_email, ru_password_entry.get(), 'user'))
                                database.commit()
                                cursor.execute('''SELECT user_id FROM user WHERE user_email=%s''', (user_email, ))
                                user_id = cursor.fetchone()
                                if user_id:
                                    cursor.execute('''INSERT INTO patient (patient_name, patient_ic_passport, patient_gender, 
                                                   patient_address, patient_contact, user_id) VALUES (%s, %s, %s, %s, %s, %s)''',
                                                   (ru_name_entry.get(), ru_ic_passport_entry.get(), ru_gender_entry.cget('text'),
                                                    ru_address_entry.get('1.0', 'end'), ru_contact_entry.get(), user_id[0]))
                                    database.commit()
                                    messagebox.showinfo('Success', 'Register User Account Successfully')
                                    self.show_login()
                            else:
                                ru_validate_register_label.config(text='Password does not match')
                        else:
                            ru_validate_register_label.config(text='Minimum 8 character of Password')
                    else:
                        ru_validate_register_label.config(text='Email exists, please try another')
                else:
                    ru_validate_register_label.config(text='Invalid email format')
            else:
                ru_validate_register_label.config(text='Please fill in all the details')

        self.reset()

        ru_text1 = tk.Label(self.frame, text='Register User Account', font=('Open Sans', 30, 'bold'), bg='white', fg='#333333')
        ru_text1.place(x=30, y=20)

        ru_name_label = tk.Label(self.frame, text='Name', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_name_label.place(x=120, y=100)
        ru_name_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                       highlightthickness=0.5)
        ru_name_entry_frame.place(x=125, y=130)
        ru_name_entry = tk.Entry(ru_name_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_name_entry.place(x=10, y=12)
        ru_name_entry.insert(0, 'Enter Your Name')
        ru_name_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', ru_name_entry))
        ru_name_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', ru_name_entry, 'Enter Your Name'))
        ru_name_entry.bind('<Return>', lambda event: register_user())

        ru_ic_passport_label = tk.Label(self.frame, text='IC or Passport Number', font=('Open Sans', 12, 'bold'), bg='white',
                                        fg='#000000')
        ru_ic_passport_label.place(x=120, y=190)
        ru_ic_passport_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                              highlightthickness=0.5)
        ru_ic_passport_entry_frame.place(x=125, y=220)
        ru_ic_passport_entry = tk.Entry(ru_ic_passport_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0,
                                        width=35)
        ru_ic_passport_entry.place(x=10, y=12)
        ru_ic_passport_entry.insert(0, 'Enter Your IC or Passport Number')
        ru_ic_passport_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', ru_ic_passport_entry))
        ru_ic_passport_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', ru_ic_passport_entry,
                                                                                     'Enter Your IC or Passport Number'))
        ru_ic_passport_entry.bind('<Return>', lambda event: register_user())

        ru_gender_label = tk.Label(self.frame, text='Gender', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_gender_label.place(x=120, y=280)
        ru_gender_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                         highlightthickness=0.5)
        ru_gender_entry_frame.place(x=125, y=310)
        ru_gender_entry = tk.Label(ru_gender_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
        ru_gender_entry.place(x=8, y=10)
        ru_gender_entry.config(text='Select Your Gender')
        ru_gender_button = ttk.Button(ru_gender_entry_frame, text='▼', style='selection.TButton', width=4, cursor='hand2',
                                      command=lambda: self.display_menu(ru_gender_entry_frame, 1, 40, ru_gender_menu))
        ru_gender_button.place(x=265, y=5)
        ru_gender_menu = tk.Menu(self.frame, tearoff=0, bg='#D0F9EF', fg='#333333', font=('Open Sans', 10))
        ru_gender_menu.add_command(label="Male", command=lambda: self.select_menu_option(ru_gender_entry, 'Male'))
        ru_gender_menu.add_command(label="Female", command=lambda: self.select_menu_option(ru_gender_entry, 'Female'))
        ru_gender_menu.add_separator()
        ru_gender_menu.add_command(label="Clear", command=lambda: self.select_menu_option(ru_gender_entry, 'Clear',
                                                                                          'Select Your Gender'))
        ru_gender_menu.add_command(label="Cancel\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ", command=ru_gender_menu.unpost)

        ru_address_label = tk.Label(self.frame, text='Address', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_address_label.place(x=120, y=370)
        ru_address_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=85, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        ru_address_entry_frame.place(x=125, y=400)
        ru_address_entry = tk.Text(ru_address_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35,
                                   height=4, wrap='word')
        ru_address_entry.place(x=10, y=10)
        ru_address_entry.insert('1.0', 'Enter Your Address')
        ru_address_entry.bind('<FocusIn>', lambda event: self.focus_entry('text', ru_address_entry))
        ru_address_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('text', ru_address_entry, 'Enter Your Address'))
        ru_address_entry.bind('<Return>', lambda event: register_user())

        ru_contact_label = tk.Label(self.frame, text='Contact Number', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_contact_label.place(x=590, y=100)
        ru_contact_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        ru_contact_entry_frame.place(x=595, y=130)
        ru_contact_entry = tk.Entry(ru_contact_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_contact_entry.place(x=10, y=12)
        ru_contact_entry.insert(0, 'Enter Your Contact Number')
        ru_contact_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', ru_contact_entry))
        ru_contact_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', ru_contact_entry, 'Enter Your Contact Number'))
        ru_contact_entry.bind('<Return>', lambda event: register_user())

        ru_email_label = tk.Label(self.frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_email_label.place(x=590, y=190)
        ru_email_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        ru_email_entry_frame.place(x=595, y=220)
        ru_email_entry = tk.Entry(ru_email_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_email_entry.place(x=10, y=12)
        ru_email_entry.insert(0, 'Enter Your Email')
        ru_email_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', ru_email_entry))
        ru_email_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', ru_email_entry, 'Enter Your Email'))
        ru_email_entry.bind('<Return>', lambda event: register_user())

        ru_password_label = tk.Label(self.frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_password_label.place(x=590, y=280)
        ru_password_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        ru_password_entry_frame.place(x=595, y=310)
        ru_password_entry = tk.Entry(ru_password_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35,
                                     show='')
        ru_password_entry.place(x=10, y=12)
        ru_password_entry.insert(0, 'Enter Your Password')
        ru_password_eye_closed_button = ttk.Button(ru_password_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        ru_password_eye_closed_button.place(x=270, y=2)
        ru_password_eye_opened_button = ttk.Button(ru_password_entry_frame, style='eye_opened_green.TButton', cursor='hand2')
        ru_password_visibility = tk.Label(ru_password_entry_frame, text='Close')
        ru_password_eye_closed_button.config(command=lambda: self.show_hide_password(ru_password_entry, ru_password_eye_opened_button,
                                                                                     ru_password_eye_closed_button,
                                                                                     ru_password_visibility))
        ru_password_eye_opened_button.config(command=lambda: self.show_hide_password(ru_password_entry, ru_password_eye_opened_button,
                                                                                     ru_password_eye_closed_button,
                                                                                     ru_password_visibility))
        ru_password_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', ru_password_entry, ru_password_visibility))
        ru_password_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', ru_password_entry, 'Enter Your Password'))
        ru_password_entry.bind('<Return>', lambda event: register_user())

        ru_confirmed_label = tk.Label(self.frame, text='Confirm Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_confirmed_label.place(x=590, y=370)
        ru_confirmed_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        ru_confirmed_entry_frame.place(x=595, y=400)
        ru_confirmed_entry = tk.Entry(ru_confirmed_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35,
                                      show='')
        ru_confirmed_entry.place(x=10, y=12)
        ru_confirmed_entry.insert(0, 'Re-enter Your Password')
        ru_confirmed_eye_closed_button = ttk.Button(ru_confirmed_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        ru_confirmed_eye_closed_button.place(x=270, y=2)
        ru_confirmed_eye_opened_button = ttk.Button(ru_confirmed_entry_frame, style='eye_opened_green.TButton', cursor='hand2')
        ru_confirmed_visibility = tk.Label(ru_confirmed_entry_frame, text='Close')
        ru_confirmed_eye_closed_button.config(command=lambda: self.show_hide_password(ru_confirmed_entry, ru_confirmed_eye_opened_button,
                                                                                      ru_confirmed_eye_closed_button,
                                                                                      ru_confirmed_visibility))
        ru_confirmed_eye_opened_button.config(command=lambda: self.show_hide_password(ru_confirmed_entry, ru_confirmed_eye_opened_button,
                                                                                      ru_confirmed_eye_closed_button,
                                                                                      ru_confirmed_visibility))
        ru_confirmed_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', ru_confirmed_entry, ru_confirmed_visibility))
        ru_confirmed_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', ru_confirmed_entry,
                                                                                   'Re-enter Your Password'))
        ru_confirmed_entry.bind('<Return>', lambda event: register_user())

        ru_back_button = ttk.Button(self.frame, text='Back', style='small_green.TButton', cursor='hand2', width=15, padding=8,
                                    command=lambda: self.show_register_as())
        ru_back_button.place(x=40, y=530)
        ru_register_button = ttk.Button(self.frame, text='Register', style='small_green.TButton', cursor='hand2', width=15, padding=8,
                                        command=lambda: register_user())
        ru_register_button.place(x=850, y=530)
        ru_validate_register_label = tk.Label(self.frame, text='', font=('Open Sans', 8), anchor='center', width=30, bg='white', fg='red')
        ru_validate_register_label.place(x=835, y=509)

    def show_registering_clinic(self):
        def register_clinic():
            self.window.focus_set()

            if rc_name_entry.cget('fg') == '#333333' and rc_operation_entry.cget('fg') == '#333333' \
                    and rc_address_entry.cget('fg') == '#333333' and rc_describe_entry.cget('fg') == '#333333' \
                    and rc_contact_entry.cget('fg') == '#333333' and rc_image_entry.cget('fg') == '#333333' \
                    and rc_email_entry.cget('fg') == '#333333' and rc_password_entry.cget('fg') == '#333333' \
                    and rc_confirmed_entry.cget('fg') == '#333333':
                img = self.image_var
                if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                    with open(img, 'rb') as file:
                        img_binary_data = file.read()
                    clinic_email = rc_email_entry.get().lower()
                    if clinic_email.endswith('@gmail.com'):
                        cursor.execute('''SELECT user_email FROM user WHERE user_email=%s''', (clinic_email, ))
                        existing_email = cursor.fetchone()
                        if not existing_email:
                            if len(rc_password_entry.get()) >= 8:
                                if rc_password_entry.get() == rc_confirmed_entry.get():
                                    rc_validate_register_label.config(text='')
                                    cursor.execute('''INSERT INTO user (user_email, user_password, user_type) VALUES (%s, %s, %s)''',
                                                   (clinic_email, rc_password_entry.get(), 'clinic'))
                                    database.commit()
                                    cursor.execute('''SELECT user_id FROM user WHERE user_email=%s''', (clinic_email,))
                                    user_id = cursor.fetchone()
                                    if user_id:
                                        cursor.execute('''INSERT INTO clinic (clinic_name, clinic_operation, clinic_address, 
                                                       clinic_description, clinic_contact, clinic_image, clinic_status, user_id) 
                                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''',
                                                       (rc_name_entry.get(), rc_operation_entry.get(), rc_address_entry.get('1.0', 'end'),
                                                        rc_describe_entry.get('1.0', 'end'), rc_contact_entry.get(), img_binary_data,
                                                        0, user_id[0]))
                                        database.commit()
                                        cursor.execute('''SELECT clinic_id FROM clinic WHERE user_id=%s''', (user_id[0], ))
                                        clinic_id = cursor.fetchone()
                                        cursor.execute('''INSERT INTO clinic_request (cr_type, cr_reason, cr_datetime, cr_detail, 
                                                       cr_ifreject, cr_status, clinic_id) 
                                                       VALUES (%s, %s, %s, %s, %s, %s, %s)''',
                                                       ('join', 'new registered', datetime.datetime.now(), None, None, 'pending',
                                                        clinic_id[0]))
                                        database.commit()
                                        messagebox.showinfo('Success', 'Register Clinic Account Successfully')
                                        self.show_login()
                                else:
                                    rc_validate_register_label.config(text='Password does not match')
                            else:
                                rc_validate_register_label.config(text='Minimum 8 characters of Password')
                        else:
                            rc_validate_register_label.config(text='Email exists, please try another')
                    else:
                        rc_validate_register_label.config(text='Invalid email format')
                else:
                    rc_validate_register_label.config(text='Invalid image format')
            else:
                rc_validate_register_label.config(text='Please fill in all the details')

        self.reset()

        rc_text1 = tk.Label(self.frame, text='Register Clinic Account', font=('Open Sans', 30, 'bold'), bg='white', fg='#333333')
        rc_text1.place(x=30, y=20)

        rc_name_label = tk.Label(self.frame, text='Clinic Name', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_name_label.place(x=120, y=90)
        rc_name_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                       highlightthickness=0.5)
        rc_name_entry_frame.place(x=125, y=115)
        rc_name_entry = tk.Entry(rc_name_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_name_entry.place(x=10, y=12)
        rc_name_entry.insert(0, 'Enter Clinic Name')
        rc_name_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', rc_name_entry))
        rc_name_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', rc_name_entry, 'Enter Clinic Name'))
        rc_name_entry.bind('<Return>', lambda event: register_clinic())

        rc_operation_label = tk.Label(self.frame, text='Operation Hours', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_operation_label.place(x=120, y=170)
        rc_operation_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        rc_operation_entry_frame.place(x=125, y=195)
        rc_operation_entry = tk.Entry(rc_operation_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0,
                                      width=35)
        rc_operation_entry.place(x=10, y=12)
        rc_operation_entry.insert(0, 'Enter Operation Hours')
        rc_operation_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', rc_operation_entry))
        rc_operation_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', rc_operation_entry, 'Enter Operation Hours'))
        rc_operation_entry.bind('<Return>', lambda event: register_clinic())

        rc_address_label = tk.Label(self.frame, text='Address', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_address_label.place(x=120, y=250)
        rc_address_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=85, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        rc_address_entry_frame.place(x=125, y=275)
        rc_address_entry = tk.Text(rc_address_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=36,
                                   height=4, wrap='word')
        rc_address_entry.place(x=10, y=10)
        rc_address_entry.insert('1.0', 'Enter Clinic Address')
        rc_address_entry.bind('<FocusIn>', lambda event: self.focus_entry('text', rc_address_entry))
        rc_address_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('text', rc_address_entry, 'Enter Clinic Address'))
        rc_address_entry.bind('<Return>', lambda event: register_clinic())

        rc_describe_label = tk.Label(self.frame, text='Short Description', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_describe_label.place(x=120, y=370)
        rc_describe_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=85, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        rc_describe_entry_frame.place(x=125, y=395)
        rc_describe_entry = tk.Text(rc_describe_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35,
                                    height=4, wrap='word')
        rc_describe_entry.place(x=10, y=10)
        rc_describe_entry.insert('1.0', 'Enter Short Description')
        rc_describe_entry.bind('<FocusIn>', lambda event: self.focus_entry('text', rc_describe_entry))
        rc_describe_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('text', rc_describe_entry, 'Enter Short Description'))
        rc_describe_entry.bind('<Return>', lambda event: register_clinic())

        rc_contact_label = tk.Label(self.frame, text='Contact Number', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_contact_label.place(x=590, y=90)
        rc_contact_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        rc_contact_entry_frame.place(x=595, y=115)
        rc_contact_entry = tk.Entry(rc_contact_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_contact_entry.place(x=10, y=12)
        rc_contact_entry.insert(0, 'Enter Contact Number')
        rc_contact_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', rc_contact_entry))
        rc_contact_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', rc_contact_entry, 'Enter Contact Number'))
        rc_contact_entry.bind('<Return>', lambda event: register_clinic())

        rc_image_label = tk.Label(self.frame, text='Image', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_image_label.place(x=590, y=170)
        rc_image_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        rc_image_entry_frame.place(x=595, y=195)
        rc_image_entry = tk.Label(rc_image_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
        rc_image_entry.place(x=8, y=10)
        rc_image_entry.config(text='Upload Clinic Image')
        rc_image_button = ttk.Button(rc_image_entry_frame, text='⇫', style='selection.TButton', width=4, cursor='hand2',
                                     command=lambda: self.upload_image(rc_image_entry))
        rc_image_button.place(x=265, y=4)

        rc_email_label = tk.Label(self.frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_email_label.place(x=590, y=250)
        rc_email_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        rc_email_entry_frame.place(x=595, y=275)
        rc_email_entry = tk.Entry(rc_email_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_email_entry.place(x=10, y=12)
        rc_email_entry.insert(0, 'Enter Your Email')
        rc_email_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', rc_email_entry))
        rc_email_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', rc_email_entry, 'Enter Your Email'))
        rc_email_entry.bind('<Return>', lambda event: register_clinic())

        rc_password_label = tk.Label(self.frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_password_label.place(x=590, y=330)
        rc_password_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        rc_password_entry_frame.place(x=595, y=355)
        rc_password_entry = tk.Entry(rc_password_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35,
                                     show='')
        rc_password_entry.place(x=10, y=12)
        rc_password_entry.insert(0, 'Enter Your Password')
        rc_password_eye_closed_button = ttk.Button(rc_password_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        rc_password_eye_closed_button.place(x=270, y=2)
        rc_password_eye_opened_button = ttk.Button(rc_password_entry_frame, style='eye_opened_green.TButton', cursor='hand2')
        rc_password_visibility = tk.Label(rc_password_entry_frame, text='Close')
        rc_password_eye_closed_button.config(command=lambda: self.show_hide_password(rc_password_entry, rc_password_eye_opened_button,
                                                                                     rc_password_eye_closed_button,
                                                                                     rc_password_visibility))
        rc_password_eye_opened_button.config(command=lambda: self.show_hide_password(rc_password_entry, rc_password_eye_opened_button,
                                                                                     rc_password_eye_closed_button,
                                                                                     rc_password_visibility))
        rc_password_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', rc_password_entry, rc_password_visibility))
        rc_password_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', rc_password_entry, 'Enter Your Password'))
        rc_password_entry.bind('<Return>', lambda event: register_clinic())

        rc_confirmed_label = tk.Label(self.frame, text='Confirm Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_confirmed_label.place(x=590, y=410)
        rc_confirmed_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        rc_confirmed_entry_frame.place(x=595, y=435)
        rc_confirmed_entry = tk.Entry(rc_confirmed_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35,
                                      show='')
        rc_confirmed_entry.place(x=10, y=12)
        rc_confirmed_entry.insert(0, 'Re-enter Your Password')
        rc_confirmed_eye_closed_button = ttk.Button(rc_confirmed_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        rc_confirmed_eye_closed_button.place(x=270, y=2)
        rc_confirmed_eye_opened_button = ttk.Button(rc_confirmed_entry_frame, style='eye_opened_green.TButton', cursor='hand2')
        rc_confirmed_visibility = tk.Label(rc_confirmed_entry_frame, text='Close')
        rc_confirmed_eye_closed_button.config(command=lambda: self.show_hide_password(rc_confirmed_entry, rc_confirmed_eye_opened_button,
                                                                                      rc_confirmed_eye_closed_button,
                                                                                      rc_confirmed_visibility))
        rc_confirmed_eye_opened_button.config(command=lambda: self.show_hide_password(rc_confirmed_entry, rc_confirmed_eye_opened_button,
                                                                                      rc_confirmed_eye_closed_button,
                                                                                      rc_confirmed_visibility))
        rc_confirmed_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', rc_confirmed_entry, rc_confirmed_visibility))
        rc_confirmed_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', rc_confirmed_entry,
                                                                                   'Re-enter Your Password'))
        rc_confirmed_entry.bind('<Return>', lambda event: register_clinic())

        rc_back_button = ttk.Button(self.frame, text='Back', style='small_green.TButton', cursor='hand2', width=15, padding=8,
                                    command=lambda: self.show_register_as())
        rc_back_button.place(x=40, y=530)
        rc_register_button = ttk.Button(self.frame, text='Register', style='small_green.TButton', cursor='hand2', width=15, padding=8,
                                        command=lambda: register_clinic())
        rc_register_button.place(x=850, y=530)
        rc_validate_register_label = tk.Label(self.frame, text='', font=('Open Sans', 8), anchor='center', width=30, bg='white', fg='red')
        rc_validate_register_label.place(x=835, y=509)

    def display_menu(self, frame, x, y, menu):
        root_x = frame.winfo_rootx()
        root_y = frame.winfo_rooty()
        adjusted_x = root_x + x
        adjusted_y = root_y + y

        menu.post(adjusted_x, adjusted_y)

    def focus_entry(self, entry_type, entry, visibility=None):
        if entry_type == 'entry':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
        elif entry_type == 'text':
            if entry.cget('fg') == '#858585':
                entry.delete('1.0', 'end')
                entry.config(fg='#333333')
        elif entry_type == 'password':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
                if visibility.cget('text') == 'Open':
                    entry.config(show='')
                elif visibility.cget('text') == 'Close':
                    entry.config(show='*')

    def leave_focus_entry(self, entry_type, entry, text):
        if entry_type == 'entry':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585')
                entry.insert(0, text)
        elif entry_type == 'text':
            value = entry.get('1.0', 'end')
            if value.strip() == '':
                entry.delete('1.0', 'end')
                entry.config(fg='#858585')
                entry.insert('1.0', text)
        elif entry_type == 'password':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585', show='')
                entry.insert(0, text)

    def show_hide_password(self, entry, eye_open_button, eye_close_button, visibility):
        if visibility.cget('text') == 'Close' and entry.cget('fg') == '#858585':
            eye_open_button.place(x=270, y=2)
            eye_close_button.place_forget()
            entry.config(show='')
            visibility.config(text='Open')
        elif visibility.cget('text') == 'Open' and entry.cget('fg') == '#858585':
            eye_open_button.place_forget()
            eye_close_button.place(x=270, y=2)
            entry.config(show='')
            visibility.config(text='Close')
        elif visibility.cget('text') == 'Open':
            eye_open_button.place_forget()
            eye_close_button.place(x=270, y=2)
            entry.config(show='*')
            visibility.config(text='Close')
        elif visibility.cget('text') == 'Close':
            eye_open_button.place(x=270, y=2)
            eye_close_button.place_forget()
            entry.config(show='')
            visibility.config(text='Open')

    def select_menu_option(self, label, option, text=None):
        if option == 'Clear':
            label.config(text=text, fg='#858585')
        else:
            label.config(text=option, fg='#333333')

    def upload_image(self, label):
        img = filedialog.askopenfilename(initialdir="/gui/images", title="Select an Image",
                                         filetypes=(("JPEG files", "*.jpg;*.jpeg"), ("png files", "*.png"), ("all files", "*.*")))
        if img:
            img_name = os.path.basename(img)
            label.config(text=img_name, fg='#333333')
            self.image_var = img


class User:
    def __init__(self, main_window, user_id):
        self.root_window = main_window
        self.user_id = user_id

        self.cursor = database.cursor(dictionary=True)

        self.window = tk.Toplevel(self.root_window)
        self.window.title('Call a Doctor')
        self.window.geometry('1050x600')
        icon = load_image('icon', 48, 48)
        self.window.iconphoto(False, icon)

        self.nf_icon = load_image('nf icon', 80, 70)
        self.search_button = load_image('search button', 18, 18)
        self.clear_search = load_image('clear search', 15, 15)

        self.clinic_images = {}
        self.doctor_images = {}

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('navigation.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        font=('Open Sans', 20, 'bold'))
        style.map('navigation.TButton', background=[('active', 'white')], foreground=[('active', '#77C7B5')])
        style.configure('back.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        font=('Open Sans', 18, 'bold'))
        style.map('back.TButton', background=[('active', 'white')], foreground=[('active', '#77C7B5')])
        style.configure('green_button.TButton', border=0, relief='flat', background='#7EE5CE', foreground='white',
                        font=('Open Sans', 14, 'bold'))
        style.map('green_button.TButton', background=[('active', '#77C7B5')])
        style.configure('selection.TButton', border=0, relief='flat', background='#D0F9EF', foreground='#3DAEC7',
                        font=('Rubik', 12, 'bold'))
        style.map('selection.TButton', background=[('active', '#D0F9EF')], foreground=[('active', '#0B8FAC')])
        style.configure('time.TButton', border=0, relief='flat', font=('Open Sans', 10), background='#B1FFEE',
                        foreground='#858585')
        style.map('time.TButton', background=[('disabled', '#FDD6D1'), ('active', '#B1FFEE')],
                  foreground=[('disabled', '#858585'), ('active', '#858585')])
        style.configure('selected_time.TButton', border=0, relief='flat', font=('Open Sans', 10), background='#7EE5CE',
                        foreground='#333333')
        style.map('selected_time.TButton', background=[('active', '#7EE5CE')], foreground=[('active', '#333333')])

        self.navigation_frame = tk.Frame(self.window, width=1050, height=90, bg='white')
        self.navigation_frame.pack()
        self.navigation_bar = tk.Frame(self.navigation_frame, height=5, bg='#166E82')

        nf_icon = tk.Label(self.navigation_frame, image=self.nf_icon, bg='white', cursor='hand2')
        nf_icon.place(x=10, y=10)
        nf_icon.bind('<Button-1>', lambda event: self.refresh())
        nf_name = tk.Label(self.navigation_frame, text='CaD', font=('Open Sans', 30, 'bold'), bg='white', fg='#166E82', cursor='hand2')
        nf_name.place(x=90, y=20)
        nf_name.bind('<Button-1>', lambda event: self.refresh())
        nf_clinic_button = ttk.Button(self.navigation_frame, text='Clinic', style='navigation.TButton', width=5,
                                      command=lambda: self.show_activity_frame(90, 567, self.clinic_frame))
        nf_clinic_button.place(x=565, y=30)
        nf_appointment_button = ttk.Button(self.navigation_frame, text='Appointment Request', style='navigation.TButton', width=20,
                                           command=lambda: self.show_activity_frame(315, 656, self.appointment_frame))
        nf_appointment_button.place(x=655, y=30)
        nf_me_button = ttk.Button(self.navigation_frame, text='Me', style='navigation.TButton', width=3,
                                  command=lambda: self.show_activity_frame(60, 976, self.me_frame))
        nf_me_button.place(x=975, y=30)

        self.clinic_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.all_clinic_frames = {}

        self.appointment_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.current_status = 'Request'  # Default status
        self.all_appointment_frames = {}

        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

        self.all_scrollable_frame = {}
        self.all_scrollable_frame[self.clinic_frame] = 1
        self.all_scrollable_frame[self.appointment_frame] = 0
        self.all_scrollable_frame[self.me_frame] = 0

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

        self.cursor.close()
        self.current_status = 'Request'

        self.clinic_images = {}
        self.doctor_images = {}

        self.all_clinic_frames = {}
        self.all_appointment_frames = {}

        self.all_scrollable_frame = {}
        self.all_scrollable_frame[self.clinic_frame] = 1
        self.all_scrollable_frame[self.appointment_frame] = 0
        self.all_scrollable_frame[self.me_frame] = 0

    def run(self):
        self.window.deiconify()
        self.refresh()

    def refresh(self):
        cursor.execute('''UPDATE appointment_request ar
                       JOIN patient p ON ar.patient_id = p.patient_id
                       SET ar.ar_status = 'canceled'
                       WHERE CONCAT(ar.ar_date, ' ', ar.ar_time) < NOW()
                       AND ar.ar_status IN ('pending', 'ongoing')
                       AND p.user_id = %s''', (self.user_id, ))
        database.commit()

        self.set_up_appointment_frame()
        self.set_up_me_frame()
        self.set_up_clinic_frame()

        if self.all_scrollable_frame[self.clinic_frame] == 1:
            self.show_activity_frame(90, 567, self.clinic_frame)
        elif self.all_scrollable_frame[self.appointment_frame] == 1:
            self.show_activity_frame(315, 656, self.appointment_frame)
        elif self.all_scrollable_frame[self.me_frame] == 1:
            self.show_activity_frame(60, 976, self.me_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.appointment_frame.pack_forget()
        self.me_frame.pack_forget()
        self.clinic_frame.pack_forget()

        frame.pack()
        frame.focus_set()

        key = list(self.all_scrollable_frame.keys())
        for k in key:
            if k == frame:
                self.all_scrollable_frame[k] = 1
            else:
                self.all_scrollable_frame[k] = 0

        if frame == self.clinic_frame:
            keys = list(self.all_clinic_frames.keys())
            for k in keys:
                active = self.all_clinic_frames[k][3]
                if active:
                    self.switch(k, self.all_clinic_frames)
        elif frame == self.appointment_frame:
            keys = list(self.all_appointment_frames.keys())
            for k in keys:
                active = self.all_appointment_frames[k][3]
                if active:
                    self.switch(k, self.all_appointment_frames)

    def switch(self, frame, frame_list):
        frames = list(frame_list.keys())
        for f in frames:
            if f == frame:
                frame_list[f][3] = 1
                frame_list[f][0].pack()
            else:
                frame_list[f][3] = 0
                frame_list[f][0].pack_forget()
        content = frame_list[frame][2]
        canvas = frame_list[frame][1]
        content.update_idletasks()
        if len(content.winfo_children()) == 0:
            canvas.configure(scrollregion=(0, 0, 0, 0))
        else:
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas))

    def set_up_clinic_frame(self):

        def clear_search():
            search_entry.delete(0, tk.END)
            show_clinics()
            clinic_canvas.yview_moveto(0)

        def search():
            show_clinics()
            clinic_canvas.yview_moveto(0)

        def show_clinics():
            self.leave_focus_entry('entry', search_entry, 'Search')
            clinics_frame.focus_set()
            for w in clinic_content_frame.winfo_children():
                w.destroy()

            if search_entry.cget('fg') == '#858585':
                clear_search_button.place_forget()
                cursor.execute('''SELECT * FROM clinic WHERE clinic_status=%s ORDER BY clinic_name ASC''', (1, ))
                clinics = cursor.fetchall()
            elif search_entry.cget('fg') == '#333333':
                clear_search_button.place(x=170, y=8)
                search_query = search_entry.get().strip()
                cursor.execute('''SELECT * FROM clinic WHERE clinic_status=%s AND (clinic_name LIKE %s OR clinic_address LIKE %s)
                               ORDER BY clinic_name ASC''',
                               (1, '%'+search_query+'%', '%'+search_query+'%'))
                clinics = cursor.fetchall()

            x_value = 15
            count = 1
            if clinics:
                for clinic in clinics:
                    if count % 2 == 0:
                        y_value = 25
                    else:
                        y_value = 0

                    clinic_id = clinic[0]

                    image_stream = BytesIO(clinic[6])
                    img = Image.open(image_stream)
                    resized_img = img.resize((240, 200), Image.LANCZOS)
                    tk_image = ImageTk.PhotoImage(resized_img)
                    self.clinic_images[clinic_id] = tk_image

                    clinic_frame = tk.Frame(clinic_content_frame, height=200, width=1000, bg='white', highlightbackground='#166E82',
                                            highlightthickness=0.5, cursor='hand2')
                    clinic_frame.pack(padx=x_value, pady=y_value, fill='y', expand=True)

                    clinic_image = tk.Label(clinic_frame, image=self.clinic_images[clinic_id], bg='white')
                    clinic_image.grid(row=0, column=0, padx=20, pady=10, rowspan=4)
                    clinic_name = tk.Label(clinic_frame, text=clinic[1], font=('Open Sans', 20, 'bold'), bg='white', fg='#000000')
                    clinic_name.grid(row=0, column=1, sticky='w', columnspan=2, pady=(20, 10))
                    clinic_address_label = tk.Label(clinic_frame, text='Address: ', font=('Open Sans', 16), bg='white', fg='#000000')
                    clinic_address_label.grid(row=1, column=1, sticky='nw', pady=(0, 5))
                    clinic_address = tk.Label(clinic_frame, text=clinic[3].strip(), font=('Open Sans', 16), bg='white', fg='#000000',
                                              anchor='w', width=51, wraplength=620, justify='left')
                    clinic_address.grid(row=1, column=2, sticky='nw', pady=(0, 5))
                    clinic_operation_label = tk.Label(clinic_frame, text='Hours: ', font=('Open Sans', 16), bg='white',
                                                      fg='#000000')
                    clinic_operation_label.grid(row=2, column=1, sticky='w', pady=(0, 5))
                    clinic_operation = tk.Label(clinic_frame, text=clinic[2], font=('Open Sans', 16), bg='white', fg='#000000')
                    clinic_operation.grid(row=2, column=2, sticky='w', pady=(0, 5))
                    clinic_contact_label = tk.Label(clinic_frame, text='Contact: ', font=('Open Sans', 16),
                                                    bg='white', fg='#000000')
                    clinic_contact_label.grid(row=3, column=1, sticky='w', pady=(5, 20))
                    clinic_contact = tk.Label(clinic_frame, text=clinic[5], font=('Open Sans', 16), bg='white', fg='#000000')
                    clinic_contact.grid(row=3, column=2, sticky='w', pady=(5, 20))

                    clinic_frame.bind('<Button-1>', lambda event, c=clinic: show_new_detail(c))
                    for widgets in clinic_frame.winfo_children():
                        widgets.bind('<Button-1>', lambda event, c=clinic: show_new_detail(c))

                    count += 1

            self.switch('clinic', self.all_clinic_frames)

        def show_new_detail(c):
            show_detail(c)
            detail_canvas.yview_moveto(0)

        def show_detail(c):
            d_back_button.config(command=lambda: show_clinics())
            schedule_button.config(command=lambda: show_schedule(c))

            for w in detail_content_frame.winfo_children():
                w.destroy()

            clinic_id = c[0]
            clinic_frame = tk.Frame(detail_content_frame, height=200, width=1000, bg='white')
            clinic_frame.pack(padx=15, fill='y', expand=True)
            clinic_image = tk.Label(clinic_frame, image=self.clinic_images[clinic_id], bg='white')
            clinic_image.grid(row=0, column=0, padx=20, pady=10, rowspan=4)
            clinic_name = tk.Label(clinic_frame, text=c[1], font=('Open Sans', 20, 'bold'), bg='white', fg='#000000')
            clinic_name.grid(row=0, column=1, sticky='w', columnspan=2, pady=(20, 10))
            clinic_address_label = tk.Label(clinic_frame, text='Address: ', font=('Open Sans', 16), bg='white', fg='#000000')
            clinic_address_label.grid(row=1, column=1, sticky='nw', pady=(0, 5))
            clinic_address = tk.Label(clinic_frame, text=c[3].strip(), font=('Open Sans', 16), bg='white', fg='#000000',
                                      anchor='w', width=51, wraplength=620, justify='left')
            clinic_address.grid(row=1, column=2, sticky='nw', pady=(0, 5))
            clinic_operation_label = tk.Label(clinic_frame, text='Hours: ', font=('Open Sans', 16), bg='white',
                                              fg='#000000')
            clinic_operation_label.grid(row=2, column=1, sticky='w', pady=(0, 5))
            clinic_operation = tk.Label(clinic_frame, text=c[2], font=('Open Sans', 16), bg='white', fg='#000000')
            clinic_operation.grid(row=2, column=2, sticky='w', pady=(0, 5))
            clinic_contact_label = tk.Label(clinic_frame, text='Contact: ', font=('Open Sans', 16),
                                            bg='white', fg='#000000')
            clinic_contact_label.grid(row=3, column=1, sticky='w', pady=(5, 20))
            clinic_contact = tk.Label(clinic_frame, text=c[5], font=('Open Sans', 16), bg='white', fg='#000000')
            clinic_contact.grid(row=3, column=2, sticky='w', pady=(5, 20))
            clinic_describe = tk.Label(clinic_frame, text=c[4].strip(), font=('Open Sans', 12), bg='white', fg='#677294',
                                       anchor='w', wraplength=970, justify='left')
            clinic_describe.grid(row=4, column=0, columnspan=3, sticky='w', padx=20)

            doctors_frame = tk.Frame(detail_content_frame, width=1000, bg='white')
            doctors_frame.pack(pady=20, fill='y', expand=True)
            doctor_title = tk.Label(doctors_frame, text='Doctors', font=('Open Sans', 16, 'bold', 'underline'),
                                    bg='white', fg='#000000')
            doctor_title.pack(anchor='center', pady=10)
            cursor.execute('''SELECT * FROM doctor WHERE clinic_id=%s AND doctor_status=%s ORDER BY doctor_name''', (clinic_id, 1))
            doctors = cursor.fetchall()
            count = 1
            for doctor in doctors:
                if count % 2 == 0:
                    y_value = 10
                else:
                    y_value = 0

                doctor_frame = tk.Frame(doctors_frame, width=700, bg='white')
                doctor_frame.pack(pady=y_value, fill='y', expand=True)

                doctor_id = doctor[0]

                image_stream = BytesIO(doctor[9])
                img = Image.open(image_stream)
                resized_img = img.resize((120, 120), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(resized_img)
                self.doctor_images[doctor_id] = tk_image

                doctor_image = tk.Label(doctor_frame, image=self.doctor_images[doctor_id], bg='white')
                doctor_image.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
                doctor_name = tk.Label(doctor_frame, text='Dr. '+doctor[1], font=('Open Sans', 14, 'bold'), bg='white', fg='#000000')
                doctor_name.grid(row=0, column=1, columnspan=2, sticky='w', pady=(5, 5))
                doctor_contact_label = tk.Label(doctor_frame, text='Contact: ', font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_contact_label.grid(row=1, column=1, sticky='w', pady=(0, 3))
                doctor_contact = tk.Label(doctor_frame, text=doctor[5], font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_contact.grid(row=1, column=2, sticky='w', pady=(0, 3))
                doctor_working_label = tk.Label(doctor_frame, text='Hours: ', font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_working_label.grid(row=2, column=1, sticky='w', pady=(0, 3))
                doctor_working = tk.Label(doctor_frame, text=doctor[6], font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_working.grid(row=2, column=2, sticky='w', pady=(0, 3))
                doctor_language_label = tk.Label(doctor_frame, text='Language: ', font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_language_label.grid(row=3, column=1, sticky='w', pady=(0, 5))
                languages = sorted(doctor[7].split(', '))
                doctor_language = tk.Label(doctor_frame, text=', '.join(languages), font=('Open Sans', 12), bg='white', fg='#000000',
                                           width=35, anchor='w')
                doctor_language.grid(row=3, column=2, sticky='w', pady=(0, 5))
                specializations = sorted(doctor[8].split(', '))
                doctor_specialize = tk.Label(doctor_frame, text='Specialize In\n'+'\n'.join([f"•{value}" for value in specializations]),
                                             font=('Open Sans', 12), bg='white', fg='#000000', anchor='e', width=20, justify='left')
                doctor_specialize.grid(row=1, column=3, rowspan=3, sticky='nw', padx=30, pady=(0, 5))

                count += 1

            self.switch('detail', self.all_clinic_frames)

        def submit(c, d=None):
            schedule_frame.focus_set()
            set_up_time_button(c, d)
            if schedule_doctor.cget('fg') == '#333333' and schedule_date.cget('fg') == '#333333' \
                    and schedule_time.cget('fg') == '#333333':
                date = schedule_calendar.get_date()
                time = datetime.strptime(schedule_time.cget('text'), "%I%p").time()
                current = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute('''SELECT patient_id FROM patient WHERE user_id=%s''', (self.user_id, ))
                patient_id = cursor.fetchone()[0]
                if d is not None:
                    if schedule_describe.cget('fg') == '#333333':
                        description = schedule_describe.get('1.0', 'end')
                    else:
                        description = None
                    cursor.execute('''INSERT INTO appointment_request (ar_date, ar_time, ar_detail, ar_status, 
                                                       ar_doctor, ar_ifreject, ar_datetime, patient_id, clinic_id) 
                                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                   (date, time, description, 'pending', 1, None, current, patient_id, c[0]))
                    database.commit()
                    cursor.execute('''SELECT ar_id FROM appointment_request WHERE ar_datetime=%s and patient_id=%s and clinic_id=%s''',
                                   (current, patient_id, c[0]))
                    ar_id = cursor.fetchone()[0]
                    cursor.execute('''INSERT INTO appointment (appointment_prescription, appointment_complete, ar_id, doctor_id) 
                                                       VALUES (%s, %s, %s, %s)''', (None, 0, ar_id, d[0]))
                    database.commit()
                else:
                    if schedule_describe.cget('fg') == '#333333':
                        description = schedule_describe.get('1.0', 'end')
                    else:
                        description = None
                    cursor.execute('''INSERT INTO appointment_request (ar_date, ar_time, ar_detail, ar_status, 
                                                       ar_doctor, ar_ifreject, ar_datetime, patient_id, clinic_id) 
                                                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                   (date, time, description, 'pending', 0, None, current, patient_id, c[0]))
                    database.commit()
                submit_error_label.config(text='')
                messagebox.showinfo('Success', 'Book Schedule Successfully')
                show_clinics()
            else:
                submit_error_label.config(text='Select all relevant details')

        def select_day(except_day, c, d=None):
            schedule_frame.focus_set()
            schedule_time.config(text='Select a time', fg='#858585')
            schedule_time_label.grid_forget()
            schedule_time_frame.grid_forget()
            schedule_time_buttons.grid_forget()
            schedule_describe.delete('1.0', tk.END)
            self.leave_focus_entry('text', schedule_describe, 'Optional')
            schedule_describe_label.grid_forget()
            schedule_describe_frame.grid_forget()

            selected = schedule_calendar.get_date()
            current_date = datetime.now().date()
            selected_date = current_date.replace(year=int(selected.split('-')[0]),
                                                 month=int(selected.split('-')[1]),
                                                 day=int(selected.split('-')[2]))
            wd_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
            if selected_date < current_date:
                schedule_date.config(fg='#8B0000', text='Selected date is passed')
            elif current_date <= selected_date <= current_date + timedelta(days=1):
                schedule_date.config(fg='#8B0000', text='Must be at least two days from now')
            else:
                if except_day['clinic'] != [] and selected_date.weekday() in except_day['clinic']:
                    schedule_date.config(fg='#8B0000', text='The clinic is closed on ' + wd_dict[selected_date.weekday()])
                elif except_day['doctor'] != [] and selected_date.weekday() in except_day['doctor']:
                    schedule_date.config(fg='#8B0000', text='The doctor is rest on ' + wd_dict[selected_date.weekday()])
                else:
                    schedule_date.config(fg='#333333', text=self.format_date(selected))
                    schedule_time_label.grid(row=3, column=1, sticky='w', pady=(0, 3), padx=110)
                    schedule_time_frame.grid(row=4, column=1, sticky='w', pady=(0, 3), padx=113)
                    schedule_time_buttons.grid(row=5, column=1, sticky='nw', pady=(3, 25), padx=113)
                    set_up_time_button(c, d)
                    submit_button.configure(command=lambda: submit(c, d))

            self.switch('schedule', self.all_clinic_frames)

        def display_date_frame(text, c, d=None):
            self.select_menu_option(schedule_doctor, text)
            schedule_calendar.selection_clear()
            schedule_date.config(fg='#858585', text='Select a date')
            schedule_time.config(text='Select a time', fg='#858585')
            schedule_time_label.grid_forget()
            schedule_time_frame.grid_forget()
            schedule_time_buttons.grid_forget()
            schedule_describe.delete('1.0', tk.END)
            self.leave_focus_entry('text', schedule_describe, 'Optional')
            schedule_describe_label.grid_forget()
            schedule_describe_frame.grid_forget()

            schedule_date_label.grid(row=3, column=0, sticky='w', pady=(0, 3), padx=50)
            schedule_date_frame.grid(row=4, column=0, sticky='w', pady=(0, 3), padx=53)
            schedule_calendar.grid(row=5, column=0, sticky='w', pady=(3, 25), padx=53)

            except_days = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}
            close_rest_day = {'clinic': [],
                              'doctor': []}

            operation = c[2].split(', ')
            if len(operation) > 2:
                close_day = operation[2].split()[-1]
                close_day = except_days[close_day]
                close_rest_day['clinic'].append(close_day)
            if d is not None:
                working = d[6].split(', ')
                if len(working) > 2:
                    rest_day = working[2].split()[-1]
                    rest_day = except_days[rest_day]
                    close_rest_day['doctor'].append(rest_day)
            schedule_calendar.bind('<<CalendarSelected>>', lambda event: select_day(close_rest_day, c, d))

            self.switch('schedule', self.all_clinic_frames)

        def set_up_time_button(c, d=None):
            for t in time_list:
                time_button_list[t][0].grid_forget()
                time_button_list[t][1] = -1
                time_button_list[t][0].state(['disabled'])
                time_button_list[t][0].config(style='time.TButton')
            time_format_12 = '%I%p'
            if d is not None:
                working = d[6].split(', ')
                if len(working) > 1:
                    working_hour = working[1].split('-')
                    start_work = working_hour[0].strip()
                    start_work = datetime.strptime(start_work, time_format_12).time()
                    end_work = working_hour[1].strip()
                    end_work = datetime.strptime(end_work, time_format_12) - timedelta(hours=1)
                    end_work = end_work.time()

                    cursor.execute('''SELECT ar.ar_time FROM appointment_request ar
                                   JOIN appointment a ON ar.ar_id = a.ar_id
                                   WHERE a.doctor_id=%s AND ar.ar_date=%s AND ar.ar_status IN ('pending', 'ongoing')''',
                                   (d[0], schedule_calendar.get_date()))
                    booked_time = cursor.fetchall()
                    booked_time_list = [self.timedelta_to_time(b_time[0]) for b_time in booked_time]

                    row_value = 0
                    column_value = 0
                    for t in time_list:
                        datetime_t = datetime.strptime(t, time_format_12).time()
                        if start_work <= datetime_t <= end_work:
                            time_button_list[t][0].grid(row=row_value, column=column_value, padx=(0, 5), pady=(0, 5), sticky='nw')
                            column_value += 1
                            if column_value == 4:
                                column_value = 0
                                row_value += 1
                            if datetime_t not in booked_time_list:
                                time_button_list[t][1] = 0
                                time_button_list[t][0].state(['!disabled'])
                else:
                    row_value = 0
                    column_value = 0
                    for t in time_list:
                        time_button_list[t][0].grid(row=row_value, column=column_value, padx=(0, 5), pady=(0, 5), sticky='nw')
                        column_value += 1
                        if column_value == 4:
                            column_value = 0
                            row_value += 1
                        time_button_list[t][1] = 0
                        time_button_list[t][0].state(['!disabled'])
            else:
                operation = c[2].split(', ')
                if operation[1] != '24 hours':
                    operation_hour = operation[1].split('-')
                    start_operate = operation_hour[0].strip()
                    start_operate = datetime.strptime(start_operate, time_format_12).time()
                    end_operate = operation_hour[1].strip()
                    end_operate = datetime.strptime(end_operate, time_format_12) - timedelta(hours=1)
                    end_operate = end_operate.time()

                    row_value = 0
                    column_value = 0
                    for t in time_list:
                        datetime_t = datetime.strptime(t, time_format_12).time()
                        if start_operate <= datetime_t <= end_operate:
                            time_button_list[t][0].grid(row=row_value, column=column_value, padx=(0, 5), pady=(0, 5), sticky='nw')
                            column_value += 1
                            if column_value == 4:
                                column_value = 0
                                row_value += 1
                            time_button_list[t][1] = 0
                            time_button_list[t][0].state(['!disabled'])
                else:
                    row_value = 0
                    column_value = 0
                    for t in time_list:
                        time_button_list[t][0].grid(row=row_value, column=column_value, padx=(0, 5), pady=(0, 5), sticky='nw')
                        column_value += 1
                        if column_value == 4:
                            column_value = 0
                            row_value += 1
                        time_button_list[t][1] = 0
                        time_button_list[t][0].state(['!disabled'])

        def select_time(t_key):
            selected_time = t_key
            schedule_time.config(fg='#333333', text=selected_time)
            for t in time_list:
                if t != selected_time and time_button_list[t][1] == 1:
                    time_button_list[t][1] = 0
                    time_button_list[t][0].config(style='time.TButton')
            time_button_list[selected_time][1] = 1
            time_button_list[selected_time][0].config(style='selected_time.TButton')
            schedule_describe_label.grid(row=6, column=0, columnspan=2, sticky='w', pady=(0, 3), padx=50)
            schedule_describe_frame.grid(row=7, column=0, columnspan=2, sticky='w', pady=(0, 25), padx=53)
            self.switch('schedule', self.all_clinic_frames)

        def show_schedule(c):
            s_back_button.config(command=lambda: show_detail(c))
            submit_button.config(command=lambda: submit(c))

            schedule_clinic.config(text=c[1])

            schedule_doctor.config(text='Select a doctor', fg='#858585')
            doctor_menu.delete(0, tk.END)
            doctor_menu.add_command(label='Random', command=lambda: display_date_frame('Random', c, None))
            cursor.execute('''SELECT * FROM doctor WHERE clinic_id=%s AND doctor_status=%s ORDER BY doctor_name''', (c[0], 1))
            doctors = cursor.fetchall()
            for doctor in doctors:
                doctor_name = "Dr. " + doctor[1]
                doctor_menu.add_command(label=doctor_name,
                                        command=lambda text=doctor_name, c=c, d=doctor: display_date_frame(text, c, d))
            doctor_menu.add_separator()
            doctor_menu.add_command(label="Cancel\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ", command=doctor_menu.unpost)

            schedule_date.config(text='Select a date', fg='#858585')
            schedule_date_label.grid_forget()
            schedule_date_frame.grid_forget()
            schedule_calendar.grid_forget()
            schedule_calendar.selection_clear()

            schedule_time.config(text='Select a time', fg='#858585')
            schedule_time_label.grid_forget()
            schedule_time_frame.grid_forget()
            schedule_time_buttons.grid_forget()

            schedule_describe.delete('1.0', tk.END)
            self.leave_focus_entry('text', schedule_describe, 'Optional')
            schedule_describe_label.grid_forget()
            schedule_describe_frame.grid_forget()

            submit_error_label.config(text='')

            self.switch('schedule', self.all_clinic_frames)
            schedule_canvas.yview_moveto(0)

        for widget in self.clinic_frame.winfo_children():
            widget.destroy()

        clinics_frame = tk.Frame(self.clinic_frame, width=1050, height=510, bg='white')
        search_frame = tk.Frame(clinics_frame, bg='#F5F5F5', width=230, height=35, highlightbackground="#C8C7C7",
                                highlightthickness=0.5)
        search_frame.place(x=785, y=15)
        search_entry = tk.Entry(search_frame, bg='#F5F5F5', font=('Roboto', 12), border=0, fg='#858585', width=16)
        search_entry.place(x=8, y=6)
        search_entry.insert(0, "Search")
        search_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', search_entry))
        search_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', search_entry, 'Search'))
        search_entry.bind('<Return>', lambda event: search())
        search_button = tk.Button(search_frame, bg='#F5F5F5', image=self.search_button, border=0, cursor='hand2',
                                  command=lambda: search())
        search_button.place(x=200, y=6)
        clear_search_button = tk.Button(search_frame, bg='#F5F5F5', image=self.clear_search, border=0, command=lambda: clear_search())
        clinic_canvas = tk.Canvas(clinics_frame, width=1030, height=430, bg='white', highlightthickness=0)
        clinic_canvas.place(x=0, y=75)
        clinic_scrollbar = tk.Scrollbar(clinics_frame, orient='vertical')
        clinic_scrollbar.place(x=1033, y=75, height=430)
        clinic_canvas.configure(yscrollcommand=clinic_scrollbar.set)
        clinic_scrollbar.configure(command=clinic_canvas.yview)
        clinic_content_frame = tk.Frame(clinic_canvas, bg='white')
        clinic_canvas.create_window((0, 0), window=clinic_content_frame, anchor="nw")
        self.all_clinic_frames['clinic'] = [clinics_frame, clinic_canvas, clinic_content_frame, 0]

        detail_frame = tk.Frame(self.clinic_frame, width=1050, height=510, bg='white')
        d_back_button = ttk.Button(detail_frame, text='< Back', style='back.TButton', cursor='hand2', width=6)
        d_back_button.place(x=20, y=15)
        schedule_button = ttk.Button(detail_frame, text='Schedule Appointment', cursor='hand2', style='green_button.TButton',
                                     width=26)
        schedule_button.place(x=720, y=18)
        detail_canvas = tk.Canvas(detail_frame, width=1030, height=430, bg='white', highlightthickness=0)
        detail_canvas.place(x=0, y=75)
        detail_scrollbar = tk.Scrollbar(detail_frame, orient='vertical')
        detail_scrollbar.place(x=1033, y=75, height=430)
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        detail_scrollbar.configure(command=detail_canvas.yview)
        detail_content_frame = tk.Frame(detail_canvas, bg='white')
        detail_canvas.create_window((0, 0), window=detail_content_frame, anchor="nw")
        self.all_clinic_frames['detail'] = [detail_frame, detail_canvas, detail_content_frame, 0]

        schedule_frame = tk.Frame(self.clinic_frame, width=1050, height=510, bg='white')
        s_back_button = ttk.Button(schedule_frame, text='< Back', style='back.TButton', cursor='hand2', width=6)
        s_back_button.place(x=20, y=15)
        submit_button = ttk.Button(schedule_frame, text='Submit', style='green_button.TButton', cursor='hand2', width=12)
        submit_button.place(x=874, y=18)
        submit_error_label = tk.Label(schedule_frame, text='', anchor='e', font=('Open Sans', 8), bg='white', fg='red', width=30)
        submit_error_label.place(x=680, y=27)
        schedule_canvas = tk.Canvas(schedule_frame, width=1030, height=430, bg='white', highlightthickness=0)
        schedule_canvas.place(x=0, y=75)
        schedule_scrollbar = tk.Scrollbar(schedule_frame, orient='vertical')
        schedule_scrollbar.place(x=1033, y=75, height=430)
        schedule_canvas.configure(yscrollcommand=schedule_scrollbar.set)
        schedule_scrollbar.configure(command=schedule_canvas.yview)
        schedule_content_frame = tk.Frame(schedule_canvas, bg='white')
        schedule_canvas.create_window((0, 0), window=schedule_content_frame, anchor="nw")
        self.all_clinic_frames['schedule'] = [schedule_frame, schedule_canvas, schedule_content_frame, 0]

        schedule_visit_label = tk.Label(schedule_content_frame, text='Schedule Visit', font=('Open Sans', 20, 'bold', 'underline'),
                                        bg='white', fg='#000000')
        schedule_visit_label.grid(row=0, column=0, columnspan=2, sticky='w', padx=50, pady=(10, 25))
        schedule_clinic_label = tk.Label(schedule_content_frame, text='Clinic', font=('Open Sans', 12, 'bold'),
                                         bg='white', fg='#000000')
        schedule_clinic_label.grid(row=1, column=0, sticky='w', pady=(0, 3), padx=50)
        schedule_clinic_frame = tk.Frame(schedule_content_frame, bg='#D0F9EF', width=380, height=45, highlightbackground='#C8C7C7',
                                         highlightthickness=0.5)
        schedule_clinic_frame.grid(row=2, column=0, sticky='w', pady=(0, 25), padx=53)
        schedule_clinic = tk.Label(schedule_clinic_frame, bg='#D0F9EF', fg='#333333', font=('Open Sans', 10))
        schedule_clinic.place(x=10, y=10)

        schedule_doctor_label = tk.Label(schedule_content_frame, text='Doctor', font=('Open Sans', 12, 'bold'),
                                         bg='white', fg='#000000')
        schedule_doctor_label.grid(row=1, column=1, sticky='w', pady=(0, 3), padx=110)
        schedule_doctor_frame = tk.Frame(schedule_content_frame, bg='#D0F9EF', width=380, height=45, highlightbackground='#C8C7C7',
                                         highlightthickness=0.5)
        schedule_doctor_frame.grid(row=2, column=1, sticky='w', pady=(0, 25), padx=113)
        schedule_doctor = tk.Label(schedule_doctor_frame, bg='#D0F9EF', font=('Open Sans', 10))
        schedule_doctor.place(x=10, y=10)
        schedule_doctor_button = ttk.Button(schedule_doctor_frame, text='▼', style='selection.TButton', width=4, cursor='hand2',
                                            command=lambda: self.display_menu(schedule_doctor_frame, 0, 40, doctor_menu))
        schedule_doctor_button.place(x=325, y=5)
        doctor_menu = tk.Menu(schedule_content_frame, tearoff=0, bg='#D0F9EF', fg='#333333', font=('Open Sans', 10))

        schedule_date_label = tk.Label(schedule_content_frame, text='Date', font=('Open Sans', 12, 'bold'),
                                       bg='white', fg='#000000')
        schedule_date_frame = tk.Frame(schedule_content_frame, bg='#D0F9EF', width=380, height=45, highlightbackground='#C8C7C7',
                                       highlightthickness=0.5)
        schedule_date = tk.Label(schedule_date_frame, bg='#D0F9EF', font=('Open Sans', 10))
        schedule_date.place(x=10, y=10)
        schedule_calendar = Calendar(schedule_content_frame, selectmode='day', date_pattern='yyyy-mm-dd', font=('Open Sans', 10))

        schedule_time_label = tk.Label(schedule_content_frame, text='Time', font=('Open Sans', 12, 'bold'),
                                       bg='white', fg='#000000')
        schedule_time_frame = tk.Frame(schedule_content_frame, bg='#D0F9EF', width=380, height=45, highlightbackground='#C8C7C7',
                                       highlightthickness=0.5)
        schedule_time = tk.Label(schedule_time_frame, bg='#D0F9EF', font=('Open Sans', 10))
        schedule_time.place(x=10, y=10)
        schedule_time_buttons = tk.Frame(schedule_content_frame, bg='white', width=380, height=200)
        time_button_list = {'8am': [], '9am': [], '10am': [],
                            '11am': [], '12pm': [], '1pm': [],
                            '2pm': [], '3pm': [], '4pm': [],
                            '5pm': [], '6pm': [], '7pm': [],
                            '8pm': []}
        time_list = time_button_list.keys()
        for time in time_list:
            time_button = ttk.Button(schedule_time_buttons, style='time.TButton', text=time, width=9, padding=10,
                                     command=lambda t_key=time: select_time(t_key))
            time_button.state(['disabled'])
            time_button_list[time].append(time_button)
            time_button_list[time].append(-1)

        schedule_describe_label = tk.Label(schedule_content_frame, text='Description', font=('Open Sans', 12, 'bold'),
                                           bg='white', fg='#000000')
        schedule_describe_frame = tk.Frame(schedule_content_frame, bg='#D0F9EF', width=928, height=150, highlightbackground='#C8C7C7',
                                           highlightthickness=0.5)
        schedule_describe = tk.Text(schedule_describe_frame, font=('Open Sans', 10), bg='#D0F9EF', border=0, width=128,
                                    height=8, wrap='word')
        schedule_describe.place(x=10, y=10)
        schedule_describe.bind('<FocusIn>', lambda event: self.focus_entry('text', schedule_describe))
        schedule_describe.bind('<FocusOut>', lambda event: self.leave_focus_entry('text', schedule_describe, 'Optional'))

        show_clinics()

    def set_up_appointment_frame(self):
        def filter_appointments(status):
            self.current_status = status
            display_appointments(status)
            update_tab_colors()
            a_canvas.yview_moveto(0)

        def update_tab_colors():
            for tab_button in tab_buttons:
                if tab_button.cget("text") == self.current_status:
                    tab_button.config(bg='#00C196', fg='white')
                else:
                    tab_button.config(bg='#E0FCF8', fg='#00C196')

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
                        SELECT ar.ar_id, ar.ar_detail, ar.ar_date, ar.ar_time, ar.ar_doctor, 
                        ar.ar_ifreject, a.appointment_prescription,
                        c.clinic_name, d.doctor_name
                        FROM appointment_request ar
                        LEFT JOIN clinic c ON ar.clinic_id = c.clinic_id
                        LEFT JOIN appointment a ON ar.ar_id = a.ar_id
                        LEFT JOIN doctor d ON a.doctor_id = d.doctor_id
                        LEFT JOIN patient p ON ar.patient_id = p.patient_id
                        WHERE ar.ar_status = '{status_map[status]}' AND p.user_id = %s
                        ORDER BY ar.ar_date, ar.ar_time;
                        """

            query_dsc = f"""
                        SELECT ar.ar_id, ar.ar_detail, ar.ar_date, ar.ar_time, ar.ar_doctor, 
                        ar.ar_ifreject, a.appointment_prescription,
                        c.clinic_name, d.doctor_name
                        FROM appointment_request ar
                        LEFT JOIN clinic c ON ar.clinic_id = c.clinic_id
                        LEFT JOIN appointment a ON ar.ar_id = a.ar_id
                        LEFT JOIN doctor d ON a.doctor_id = d.doctor_id
                        LEFT JOIN patient p ON ar.patient_id = p.patient_id
                        WHERE ar.ar_status = '{status_map[status]}' AND p.user_id = %s
                        ORDER BY ar.ar_date DESC, ar.ar_time DESC;
                        """

            if status == 'Request' or status == 'Ongoing':
                self.cursor.execute(query_asc, (self.user_id,))
                appointments = self.cursor.fetchall()
            else:
                self.cursor.execute(query_dsc, (self.user_id,))
                appointments = self.cursor.fetchall()

            for i, appointment in enumerate(appointments):
                ar_id = appointment['ar_id']
                ar_detail = appointment['ar_detail']
                ar_date = self.format_date(str(appointment['ar_date']))
                ar_time = self.timedelta_to_time(appointment['ar_time'])
                ar_time = ar_time.strftime("%I%p").lstrip('0').lower()
                clinic_name = appointment['clinic_name']
                doctor_name = ('Dr. ' + appointment['doctor_name']) if appointment['ar_doctor'] else '-'

                card_frame = tk.Frame(a_scrollable_frame, bg='white', highlightbackground='#00C196',
                                      highlightthickness=1)
                card_frame.grid(row=i + 1, column=0, columnspan=5, padx=20, pady=10, sticky='ew')
                card_frame.grid_columnconfigure(0, weight=1)
                card_frame.grid_columnconfigure(1, weight=1)
                card_frame.grid_columnconfigure(2, weight=1)
                card_frame.grid_columnconfigure(3, weight=1)

                id_label = tk.Label(card_frame, text=f"Appointment ID: {ar_id}", font=('Open Sans', 16, 'bold'),
                                    bg='white', fg='#333333')
                id_label.grid(row=0, column=0, sticky='w', padx=15, pady=(10, 5))

                clinic_label = tk.Label(card_frame, text=f"   Clinic: {clinic_name}", font=('Open Sans', 12, 'bold'), width=55,
                                        bg='white', fg='#333333', anchor='w')
                clinic_label.grid(row=1, column=0, sticky='w', padx=15, pady=5)

                doctor_label = tk.Label(card_frame, text=f"   Doctor: {doctor_name}", font=('Open Sans', 12),
                                        bg='white', fg='#333333')
                doctor_label.grid(row=2, column=0, sticky='w', padx=15, pady=5)

                date_label = tk.Label(card_frame, text=f"   Date: {ar_date}", font=('Open Sans', 12), bg='white',
                                      fg='#333333')
                date_label.grid(row=3, column=0, sticky='w', padx=15, pady=5)

                time_label = tk.Label(card_frame, text=f"   Time: {ar_time}", font=('Open Sans', 12), bg='white',
                                      fg='#333333')
                time_label.grid(row=4, column=0, sticky='w', padx=15, pady=(5, 15))

                description_label = tk.Label(card_frame, text="Description:", font=('Open Sans', 12), bg='white',
                                             fg='#333333')
                description_label.grid(row=1, column=4, columnspan=2, sticky='w', padx=10)

                description_frame = tk.Frame(card_frame)
                description_frame.grid(row=2, column=4, rowspan=3, sticky='nw', padx=15)

                description_text = tk.Text(description_frame, font=('Open Sans', 12), bg='white', fg='#333333', width=40,
                                           height=4, borderwidth=1, relief='solid')
                if ar_detail is not None:
                    description_text.insert('1.0', ar_detail)
                description_text.config(state=tk.DISABLED)
                description_text.pack(side="left", fill="both", expand=True)

                text_scrollbar = tk.Scrollbar(description_frame, command=description_text.yview)
                text_scrollbar.pack(side="right", fill="y")

                description_text.config(yscrollcommand=text_scrollbar.set)

                if status != 'Canceled':
                    time_label.grid(row=4, column=0, sticky='w', padx=15, pady=5)
                    if status == 'Request' or status == 'Ongoing':
                        cancel_button = tk.Button(card_frame, text='Cancel', font=('Open Sans', 12, 'bold'), bg='#F5443E',
                                                  fg='white', width=8, borderwidth=0, relief="flat", padx=50, pady=5,
                                                  command=lambda ar_id=ar_id: cancel_appointment(ar_id))
                        cancel_button.grid(row=5, column=4, columnspan=2, sticky='e', padx=15, pady=(0, 15))
                    elif status == 'Completed':
                        appointment_prescription = appointment['appointment_prescription']
                        prescription_label = tk.Label(card_frame, text="   Prescription:", font=('Open Sans', 12),
                                                      bg='white', fg='#333333')
                        prescription_label.grid(row=5, column=0, padx=15, pady=5, sticky='w')
                        prescription_frame = tk.Frame(card_frame)
                        prescription_frame.grid(row=6, column=0, columnspan=5, sticky='nw', padx=(30, 15), pady=(0, 15))
                        prescription_text = tk.Text(prescription_frame, font=('Open Sans', 12), bg='white', fg='#333333', width=103,
                                                    height=4, borderwidth=1, relief='solid')
                        prescription_text.insert('1.0', appointment_prescription)
                        prescription_text.config(state=tk.DISABLED)
                        prescription_text.pack(side="left", fill="both", expand=True)
                        prescription_scrollbar = tk.Scrollbar(prescription_frame, command=prescription_text.yview)
                        prescription_scrollbar.pack(side="right", fill="y")

                        prescription_text.config(yscrollcommand=prescription_scrollbar.set)
                    elif status == 'Rejected':
                        ar_ifreject = appointment['ar_ifreject']
                        reject_label = tk.Label(card_frame, text="   Reject Reason:", font=('Open Sans', 12), bg='white', fg='#333333')
                        reject_label.grid(row=5, column=0, padx=15, pady=5, sticky='w')
                        reject_frame = tk.Frame(card_frame)
                        reject_frame.grid(row=6, column=0, columnspan=5, sticky='nw', padx=(30, 15), pady=(0, 15))
                        reject_text = tk.Text(reject_frame, font=('Open Sans', 12), bg='white', fg='#333333', width=103,
                                              height=4, borderwidth=1, relief='solid')
                        reject_text.insert('1.0', ar_ifreject)
                        reject_text.config(state=tk.DISABLED)
                        reject_text.pack(side="left", fill="both", expand=True)
                        reject_scrollbar = tk.Scrollbar(reject_frame, command=reject_text.yview)
                        reject_scrollbar.pack(side="right", fill="y")

                        reject_text.config(yscrollcommand=reject_scrollbar.set)

            self.switch('appointment', self.all_appointment_frames)

        def cancel_appointment(ar_id):
            update_query = "UPDATE appointment_request SET ar_status = 'canceled' WHERE ar_id = %s"
            self.cursor.execute(update_query, (ar_id,))
            database.commit()

            display_appointments(self.current_status)

        for widget in self.appointment_frame.winfo_children():
            widget.destroy()

        tab_button_frame = tk.Frame(self.appointment_frame, background='#ffffff')
        tab_button_frame.pack(fill='x', expand='True')

        # Create a canvas and a scrollbar
        a_canvas = tk.Canvas(self.appointment_frame, borderwidth=0, background="#ffffff", width=1030, height=500, highlightthickness=0)
        a_scrollbar = tk.Scrollbar(self.appointment_frame, orient="vertical", command=a_canvas.yview)
        a_scrollable_frame = tk.Frame(a_canvas, background="#ffffff")

        a_canvas.create_window((0, 0), window=a_scrollable_frame, anchor="nw")
        a_canvas.configure(yscrollcommand=a_scrollbar.set)

        # Pack the canvas and scrollbar
        a_canvas.pack(side="left", fill="both", expand=True)
        a_scrollbar.pack(side="right", fill="y")
        self.all_appointment_frames['appointment'] = [self.appointment_frame, a_canvas, a_scrollable_frame, 0]

        # Create the navigation buttons
        tab_buttons = []
        tabs = ['Request', 'Ongoing', 'Completed', 'Rejected', 'Canceled']
        for i, tab in enumerate(tabs):
            tab_button = tk.Button(tab_button_frame, text=tab, font=('Open Sans', 12, 'bold'),
                                   bg='#00C196' if tab == self.current_status else '#E0FCF8',
                                   fg='white' if tab == self.current_status else '#00C196', width=12, borderwidth=0,
                                   relief="ridge", bd=2, highlightbackground='#00C196', highlightthickness=0, padx=5,
                                   pady=5, command=lambda t=tab: filter_appointments(t))
            tab_button.grid(row=0, column=i, padx=14, pady=10)
            tab_button.config(relief="flat", highlightthickness=0, borderwidth=0, padx=30, pady=5)
            tab_buttons.append(tab_button)

        display_appointments(self.current_status)

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()

    def on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def focus_entry(self, entry_type, entry, visibility=None):
        if entry_type == 'entry':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
        elif entry_type == 'text':
            if entry.cget('fg') == '#858585':
                entry.delete('1.0', 'end')
                entry.config(fg='#333333')
        elif entry_type == 'password':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
                if visibility.cget('text') == 'Open':
                    entry.config(show='')
                elif visibility.cget('text') == 'Close':
                    entry.config(show='*')

    def leave_focus_entry(self, entry_type, entry, text):
        if entry_type == 'entry':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585')
                entry.insert(0, text)
        elif entry_type == 'text':
            value = entry.get('1.0', 'end')
            if value.strip() == '':
                entry.delete('1.0', 'end')
                entry.config(fg='#858585')
                entry.insert('1.0', text)
        elif entry_type == 'password':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585', show='')
                entry.insert(0, text)

    def display_menu(self, frame, x, y, menu):
        root_x = frame.winfo_rootx()
        root_y = frame.winfo_rooty()
        adjusted_x = root_x + x
        adjusted_y = root_y + y

        menu.post(adjusted_x, adjusted_y)

    def select_menu_option(self, label, option, text=None):
        if option == 'Clear':
            label.config(text=text, fg='#858585')
        else:
            label.config(text=option, fg='#333333')

    def format_date(self, date):
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

    def timedelta_to_time(self, td_value):
        total_seconds = td_value.total_seconds()
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        return time(hours, minutes, seconds)


class Clinic:
    def __init__(self, main_window, user_id):
        self.root_window = main_window
        self.user_id = user_id
        cursor.execute('''SELECT clinic_id FROM clinic WHERE user_id=%s''', (self.user_id, ))
        self.clinic_id = cursor.fetchone()[0]

        self.window = tk.Toplevel(self.root_window)
        self.window.title('Call a Doctor')
        self.window.geometry('1050x600')
        icon = load_image('icon', 48, 48)
        self.window.iconphoto(False, icon)

        self.nf_icon = load_image('nf icon', 80, 70)
        self.eye_closed_image = load_image('eye closed', 24, 24)
        self.eye_opened_image = load_image('eye opened', 24, 24)
        self.calendar = load_image('calendar', 20, 20)
        self.back_image = load_image('back', 80, 40)

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('navigation.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        font=('Open Sans', 20, 'bold'))
        style.map('navigation.TButton', background=[('active', 'white')], foreground=[('active', '#77C7B5')])
        style.configure('white_word.TButton', border=0, relief='flat', background='#7EE5CE', foreground='white',
                        font=('Open Sans', 15, 'bold'))
        style.map('white_word.TButton', background=[('active', '#7EE5CE')], foreground=[('active', 'white')])
        style.configure('black_word.TButton', border=1, relief='flat', background='white', foreground='black',
                        font=('Open Sans', 12, 'bold'))
        style.map('black_word.TButton', background=[('active', 'white')], foreground=[('active', 'black')])
        style.configure('inactive.TButton', border=1, relief='flat', background='grey', foreground='black',
                        font=('Open Sans', 12, 'bold'))
        style.map('inactive.TButton', background=[('active', 'grey')], foreground=[('active', 'black')])
        style.configure('selected.TButton', border=1, relief='flat', background='#7EE5CE', foreground='white',
                        font=('Open Sans', 12, 'bold'))
        style.map('selected.TButton', background=[('active', '#7EE5CE')], foreground=[('active', 'white')])
        style.configure('back.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        image=self.back_image)
        style.map('back.TButton', background=[('active', 'white')], foreground=[('active', '#7EE5CE')])
        style.configure('selection.TButton', border=0, relief='flat', background='#D0F9EF', foreground='#3DAEC7',
                        font=('Rubik', 12, 'bold'))
        style.map('selection.TButton', background=[('active', '#D0F9EF')], foreground=[('active', '#0B8FAC')])
        style.configure('eye_closed_grey.TButton', border=0, relief='flat', background='#F5F5F5',
                        image=self.eye_closed_image)
        style.map('eye_closed_grey.TButton', background=[('active', '#F5F5F5')])
        style.configure('eye_opened_grey.TButton', border=0, relief='flat', background='#F5F5F5',
                        image=self.eye_opened_image)
        style.map('eye_opened_grey.TButton', background=[('active', '#F5F5F5')])
        style.configure('eye_closed_green.TButton', border=0, relief='flat', background='#D0F9EF',
                        image=self.eye_closed_image)
        style.map('eye_closed_green.TButton', background=[('active', '#D0F9EF')])
        style.configure('eye_opened_green.TButton', border=0, relief='flat', background='#D0F9EF',
                        image=self.eye_opened_image)
        style.map('eye_opened_green.TButton', background=[('active', '#D0F9EF')])
        style.configure('calendar.TButton', border=0, relief='flat', background='#D0F9EF',
                        image=self.calendar)
        style.map('calendar.TButton', background=[('active', '#D0F9EF')])

        self.navigation_frame = tk.Frame(self.window, width=1050, height=90, bg='white')
        self.navigation_frame.pack()
        self.navigation_bar = tk.Frame(self.navigation_frame, height=5, bg='#166E82')

        nf_icon = tk.Label(self.navigation_frame, image=self.nf_icon, bg='white', cursor='hand2')
        nf_icon.place(x=10, y=10)
        nf_icon.bind('<Button-1>', lambda event: self.refresh())
        nf_name = tk.Label(self.navigation_frame, text='CaD', font=('Open Sans', 30, 'bold'), bg='white', fg='#166E82', cursor='hand2')
        nf_name.place(x=90, y=20)
        nf_name.bind('<Button-1>', lambda event: self.refresh())
        nf_appointment_button = ttk.Button(self.navigation_frame, text='Appointment Request', style='navigation.TButton', width=20,
                                           command=lambda: self.show_activity_frame(315, 327, self.appointment_frame))
        nf_appointment_button.place(x=326, y=30)
        nf_timetable_button = ttk.Button(self.navigation_frame, text='Timetable', style='navigation.TButton', width=9,
                                         command=lambda: self.show_activity_frame(150, 646, self.timetable_frame))
        nf_timetable_button.place(x=645, y=30)
        nf_doctor_list_button = ttk.Button(self.navigation_frame, text='Doctor List', style='navigation.TButton', width=10,
                                           command=lambda: self.show_activity_frame(165, 803, self.doctor_list_frame))
        nf_doctor_list_button.place(x=802, y=30)

        nf_me_button = ttk.Button(self.navigation_frame, text='Me', style='navigation.TButton', width=3,
                                  command=lambda: self.show_activity_frame(60, 976, self.me_frame))
        nf_me_button.place(x=975, y=30)

        self.appointment_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

        self.timetable_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

        self.doctor_list_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.all_doctor_list_frames = {}
        self.doctor_image_var = None
        #self.tree = None

        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

        self.all_scrollable_frame = {}
        self.all_scrollable_frame[self.appointment_frame] = 1
        self.all_scrollable_frame[self.timetable_frame] = 0
        self.all_scrollable_frame[self.doctor_list_frame] = 0
        self.all_scrollable_frame[self.me_frame] = 0

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

        self.all_doctor_list_frames = {}
        self.doctor_image_var = None

        self.all_scrollable_frame = {}
        self.all_scrollable_frame[self.appointment_frame] = 1
        self.all_scrollable_frame[self.timetable_frame] = 0
        self.all_scrollable_frame[self.doctor_list_frame] = 0
        self.all_scrollable_frame[self.me_frame] = 0

    def run(self):
        self.window.deiconify()
        self.refresh()

    def refresh(self):
        self.set_up_appointment_frame()
        self.set_up_timetable_frame()
        self.set_up_doctor_list_frame()
        self.set_up_me_frame()

        if self.all_scrollable_frame[self.appointment_frame] == 1:
            self.show_activity_frame(315, 327, self.appointment_frame)
        elif self.all_scrollable_frame[self.timetable_frame] == 1:
            self.show_activity_frame(150, 646, self.timetable_frame)
        elif self.all_scrollable_frame[self.doctor_list_frame] == 1:
            self.show_activity_frame(165, 803, self.doctor_list_frame)
        elif self.all_scrollable_frame[self.me_frame] == 1:
            self.show_activity_frame(60, 976, self.me_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.appointment_frame.pack_forget()
        self.timetable_frame.pack_forget()
        self.doctor_list_frame.pack_forget()
        self.me_frame.pack_forget()

        frame.pack()
        frame.focus_set()

        key = list(self.all_scrollable_frame.keys())
        for k in key:
            if k == frame:
                self.all_scrollable_frame[k] = 1
            else:
                self.all_scrollable_frame[k] = 0

        if frame == self.doctor_list_frame:
            keys = list(self.all_doctor_list_frames.keys())
            for k in keys:
                active = self.all_doctor_list_frames[k][3]
                if active:
                    self.switch(k, self.all_doctor_list_frames)

    def switch(self, frame, frame_list):
        frames = list(frame_list.keys())
        for f in frames:
            if f == frame:
                frame_list[f][3] = 1
                frame_list[f][0].pack()
            else:
                frame_list[f][3] = 0
                frame_list[f][0].pack_forget()
        content = frame_list[frame][2]
        canvas = frame_list[frame][1]
        content.update_idletasks()
        if len(content.winfo_children()) == 0:
            canvas.configure(scrollregion=(0, 0, 0, 0))
        else:
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas))

    def set_up_appointment_frame(self):
        for widget in self.appointment_frame.winfo_children():
            widget.destroy()

    def set_up_timetable_frame(self):
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()

    def set_up_doctor_list_frame(self):
        def show_doctor_list():
            for widget in left_frame_content.winfo_children():
                widget.destroy()
            for widget in right_frame_content.winfo_children():
                widget.destroy()

            self.doctor_image_var = None

            cursor.execute('''SELECT doctor_id, doctor_name, doctor_status FROM doctor WHERE clinic_id=%s
                           ORDER BY doctor_status DESC, doctor_name ASC''', (self.clinic_id,))
            doctors = cursor.fetchall()

            # Populate left frame with doctors
            for doctor_id, doctor_name, doctor_status in doctors:
                button_style = 'black_word.TButton'
                if doctor_status == 0:
                    button_style = 'inactive.TButton'

                doctor_button = ttk.Button(left_frame_content, text=doctor_name, style=button_style, cursor='hand2',
                                           width=20, padding=5,
                                           command=lambda doctor_id=doctor_id: show_doctor_details(doctor_id))
                doctor_button.pack(pady=5)

            decide_left_right_list()
            self.switch('doctor_list', self.all_doctor_list_frames)

        # add doctor
        def show_add_doctor_frame():
            def register_doctor():
                if doctor_name_entry.cget('fg') == '#333333' and doctor_ic_passport_entry.cget('fg') == '#333333' \
                        and doctor_address_entry.cget('fg') == '#333333' and doctor_specialise_entry.cget('fg') == '#333333' \
                        and doctor_contact_entry.cget('fg') == '#333333' and doctor_image_entry.cget('fg') == '#333333' \
                        and doctor_email_entry.cget('fg') == '#333333' and doctor_password_entry.cget('fg') == '#333333' \
                        and doctor_confirmed_entry.cget('fg') == '#333333' and doctor_language_entry.cget('fg') == '#333333' \
                        and doctor_gender_entry.cget('fg') == '#333333' and doctor_working_hours_entry.cget('fg') == '#333333':
                    img = self.doctor_image_var
                    if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                        with open(img, 'rb') as file:
                            img_binary_data = file.read()
                        doctor_email = doctor_email_entry.get().lower()
                        if doctor_email.endswith('@gmail.com'):
                            cursor.execute('''SELECT user_email FROM user WHERE user_email=%s''', (doctor_email,))
                            existing_email = cursor.fetchone()
                            if not existing_email:
                                if len(doctor_password_entry.get()) >= 8:
                                    if doctor_password_entry.get() == doctor_confirmed_entry.get():
                                        doctor_validate_register_label.config(text='')
                                        cursor.execute(
                                            '''INSERT INTO user (user_email, user_password, user_type) VALUES (%s, %s, %s)''',
                                            (doctor_email, doctor_password_entry.get(), 'doctor'))
                                        database.commit()
                                        cursor.execute('''SELECT user_id FROM user WHERE user_email=%s''',
                                                       (doctor_email,))
                                        user_id = cursor.fetchone()
                                        if user_id:
                                            cursor.execute('''INSERT INTO doctor (doctor_name, doctor_gender, doctor_address, 
                                                           doctor_ic_passport, doctor_language, doctor_working_hour, doctor_contact, 
                                                           doctor_image, doctor_status, doctor_specialize, user_id, clinic_id) 
                                                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                                                           (doctor_name_entry.get(), doctor_gender_entry.cget('text'),
                                                            doctor_address_entry.get('1.0', 'end'), doctor_ic_passport_entry.get(),
                                                            doctor_language_entry.get(), doctor_working_hours_entry.get(),
                                                            doctor_contact_entry.get(), img_binary_data, 1,
                                                            doctor_specialise_entry.get(),
                                                            user_id[0], self.clinic_id))
                                            database.commit()
                                            messagebox.showinfo('Success', 'Register Doctor Account Successfully')
                                            show_doctor_list()
                                    else:
                                        doctor_validate_register_label.config(text='Password does not match')
                                else:
                                    doctor_validate_register_label.config(text='Minimum 8 characters of Password')
                            else:
                                doctor_validate_register_label.config(text='Email exists, please try another')
                        else:
                            doctor_validate_register_label.config(text='Invalid email format')
                    else:
                        doctor_validate_register_label.config(text='Invalid image format')
                else:
                    doctor_validate_register_label.config(text='Please fill in all the details')

            for widget in doctor_entries_frame.winfo_children():
                widget.destroy()

            self.doctor_image_var = None

            # Add doctor Label
            add_doctor_label = tk.Label(doctor_entries_frame, text='Add Doctor',
                                        font=('Open Sans', 20, 'underline', 'bold'), bg='white', fg='#000000')
            add_doctor_label.grid(row=0, column=0, columnspan=2, padx=35, pady=(10, 15), sticky='w')

            # Entry for doctor name
            doctor_name_label = tk.Label(doctor_entries_frame, text='Doctor Name', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
            doctor_name_label.grid(row=1, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_name_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_name_entry_frame.grid(row=2, column=0, padx=53, pady=(0, 5))
            doctor_name_entry = tk.Entry(doctor_name_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0,
                                         width=42)
            doctor_name_entry.place(x=10, y=13)
            doctor_name_entry.insert(0, 'Enter Doctor Name')
            doctor_name_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', doctor_name_entry))
            doctor_name_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', doctor_name_entry, 'Enter Doctor Name'))
            doctor_name_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for IC or Passport Number
            doctor_ic_passport_label = tk.Label(doctor_entries_frame, text='IC or Passport Number',
                                                font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
            doctor_ic_passport_label.grid(row=3, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_ic_passport_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_ic_passport_entry_frame.grid(row=4, column=0, padx=53, pady=(0, 5))
            doctor_ic_passport_entry = tk.Entry(doctor_ic_passport_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                                fg='#858585', border=0, width=42)
            doctor_ic_passport_entry.place(x=10, y=13)
            doctor_ic_passport_entry.insert(0, 'Enter IC or Passport Number')
            doctor_ic_passport_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', doctor_ic_passport_entry))
            doctor_ic_passport_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', doctor_ic_passport_entry,
                                                                                             'Enter IC or Passport Number'))
            doctor_ic_passport_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for gender
            doctor_gender_label = tk.Label(doctor_entries_frame, text='Gender', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
            doctor_gender_label.grid(row=5, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_gender_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_gender_entry_frame.grid(row=6, column=0, padx=53, pady=(0, 5))
            doctor_gender_entry = tk.Label(doctor_gender_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
            doctor_gender_entry.place(x=9, y=10)
            doctor_gender_entry.config(text='Select Gender')
            doctor_gender_button = ttk.Button(doctor_gender_entry_frame, text='▼', style='selection.TButton', width=4, cursor='hand2',
                                              command=lambda: self.display_menu(doctor_gender_entry_frame, 1, 40, doctor_gender_menu))
            doctor_gender_button.place(x=320, y=5)
            doctor_gender_menu = tk.Menu(doctor_entries_frame, tearoff=0, bg='#D0F9EF', fg='#333333', font=('Open Sans', 10))
            doctor_gender_menu.add_command(label="Male", command=lambda: self.select_menu_option(doctor_gender_entry, 'Male'))
            doctor_gender_menu.add_command(label="Female", command=lambda: self.select_menu_option(doctor_gender_entry, 'Female'))
            doctor_gender_menu.add_separator()
            doctor_gender_menu.add_command(label="Clear", command=lambda: self.select_menu_option(doctor_gender_entry, 'Clear',
                                                                                                  'Select Gender'))
            doctor_gender_menu.add_command(label="Cancel\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t   ",
                                           command=doctor_gender_menu.unpost)

            # Entry for address
            doctor_address_label = tk.Label(doctor_entries_frame, text='Address', font=('Open Sans', 12, 'bold'), bg='white',
                                            fg='#000000')
            doctor_address_label.grid(row=13, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_address_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=85)
            doctor_address_entry_frame.grid(row=14, column=0, padx=53, pady=(0, 40))
            doctor_address_entry = tk.Text(doctor_address_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                           border=0, width=42, height=4, wrap='word')
            doctor_address_entry.place(x=10, y=13)
            doctor_address_entry.insert('1.0', 'Enter Address')
            doctor_address_entry.bind('<FocusIn>', lambda event: self.focus_entry('text', doctor_address_entry))
            doctor_address_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('text', doctor_address_entry, 'Enter Address'))
            doctor_address_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for language
            doctor_language_label = tk.Label(doctor_entries_frame, text='Language', font=('Open Sans', 12, 'bold'),
                                             bg='white', fg='#000000')
            doctor_language_label.grid(row=9, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_language_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_language_entry_frame.grid(row=10, column=0, padx=53, pady=(0, 5))
            doctor_language_entry = tk.Entry(doctor_language_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                             border=0, width=42)
            doctor_language_entry.place(x=10, y=13)
            doctor_language_entry.insert(0, 'Enter Language')
            doctor_language_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', doctor_language_entry))
            doctor_language_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', doctor_language_entry,
                                                                                          'Enter Language'))
            doctor_language_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for working hours
            doctor_working_hours_label = tk.Label(doctor_entries_frame, text='Working Hours', font=('Open Sans', 12, 'bold'),
                                                  bg='white', fg='#000000')
            doctor_working_hours_label.grid(row=11, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_working_hours_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_working_hours_entry_frame.grid(row=12, column=0, padx=53, pady=(0, 5))
            doctor_working_hours_entry = tk.Entry(doctor_working_hours_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                                  fg='#858585', border=0, width=42)
            doctor_working_hours_entry.place(x=10, y=13)
            doctor_working_hours_entry.insert(0, 'Enter Working Hours')
            doctor_working_hours_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', doctor_working_hours_entry))
            doctor_working_hours_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', doctor_working_hours_entry,
                                                                                               'Enter Working Hours'))
            doctor_working_hours_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for specialise in
            doctor_specialise_label = tk.Label(doctor_entries_frame, text='Specialize in',
                                               font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
            doctor_specialise_label.grid(row=7, column=0, padx=50, pady=(5, 0), sticky='w')
            doctor_specialise_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_specialise_entry_frame.grid(row=8, column=0, padx=53, pady=(0, 5))
            doctor_specialise_entry = tk.Entry(doctor_specialise_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                               border=0, width=42)
            doctor_specialise_entry.place(x=10, y=13)
            doctor_specialise_entry.insert(0, 'Enter Specialization')
            doctor_specialise_entry.bind('<FocusIn>',
                                         lambda event: self.focus_entry('entry', doctor_specialise_entry))
            doctor_specialise_entry.bind('<FocusOut>',
                                         lambda event: self.leave_focus_entry('entry', doctor_specialise_entry,
                                                                              'Enter Specialization'))
            doctor_specialise_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for contact
            doctor_contact_label = tk.Label(doctor_entries_frame, text='Contact Number', font=('Open Sans', 12, 'bold'),
                                            bg='white', fg='#000000')
            doctor_contact_label.grid(row=1, column=4, padx=110, pady=(5, 0), sticky='w')
            doctor_contact_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_contact_entry_frame.grid(row=2, column=4, padx=113, pady=(0, 5))
            doctor_contact_entry = tk.Entry(doctor_contact_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                            border=0, width=42)
            doctor_contact_entry.place(x=10, y=12)
            doctor_contact_entry.insert(0, 'Enter Contact Number')
            doctor_contact_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', doctor_contact_entry))
            doctor_contact_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', doctor_contact_entry,
                                                                                         'Enter Contact Number'))
            doctor_contact_entry.bind('<Return>', lambda event: register_doctor())

            # Upload doctor image
            doctor_image_label = tk.Label(doctor_entries_frame, text='Image', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
            doctor_image_label.grid(row=3, column=4, padx=110, pady=(5, 0), sticky='w')
            doctor_image_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_image_entry_frame.grid(row=4, column=4, padx=113, pady=(0, 5))
            doctor_image_entry = tk.Label(doctor_image_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
            doctor_image_entry.place(x=8, y=10)
            doctor_image_entry.config(text='Upload Doctor Image')
            doctor_image_button = ttk.Button(doctor_image_entry_frame, text='⇫', style='selection.TButton', width=4,
                                             cursor='hand2', command=lambda: self.upload_doctor_image(doctor_image_entry, 60, 60,
                                                                                                      img_label))
            doctor_image_button.place(x=320, y=4)
            img_label = tk.Label(doctor_entries_frame, bg='white', anchor='w')
            img_label.grid(row=5, column=4, padx=113, pady=5, rowspan=2, sticky='w')

            # Entry for email
            doctor_email_label = tk.Label(doctor_entries_frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
            doctor_email_label.grid(row=7, column=4, padx=110, pady=(5, 0), sticky='w')
            doctor_email_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_email_entry_frame.grid(row=8, column=4, padx=113, pady=(0, 5))
            doctor_email_entry = tk.Entry(doctor_email_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                          border=0, width=42)
            doctor_email_entry.place(x=10, y=12)
            doctor_email_entry.insert(0, 'Enter Email')
            doctor_email_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', doctor_email_entry))
            doctor_email_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', doctor_email_entry, 'Enter Email'))
            doctor_email_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for password
            doctor_password_label = tk.Label(doctor_entries_frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white',
                                             fg='#000000')
            doctor_password_label.grid(row=9, column=4, padx=110, pady=(5, 0), sticky='w')
            doctor_password_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_password_entry_frame.grid(row=10, column=4, padx=113, pady=(0, 5))
            doctor_password_entry = tk.Entry(doctor_password_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                             border=0, width=42, show='')
            doctor_password_entry.place(x=10, y=12)
            doctor_password_entry.insert(0, 'Enter Password')
            doctor_password_eye_closed_button = ttk.Button(doctor_password_entry_frame, style='eye_closed_green.TButton',
                                                           cursor='hand2')
            doctor_password_eye_closed_button.place(x=330, y=2)
            doctor_password_eye_opened_button = ttk.Button(doctor_password_entry_frame, style='eye_opened_green.TButton',
                                                           cursor='hand2')
            doctor_password_visibility = tk.Label(doctor_password_entry_frame, text='Close')
            doctor_password_eye_closed_button.config(command=lambda: self.show_hide_password(doctor_password_entry,
                                                                                             doctor_password_eye_opened_button,
                                                                                             doctor_password_eye_closed_button,
                                                                                             doctor_password_visibility))
            doctor_password_eye_opened_button.config(command=lambda: self.show_hide_password(doctor_password_entry,
                                                                                             doctor_password_eye_opened_button,
                                                                                             doctor_password_eye_closed_button,
                                                                                             doctor_password_visibility))
            doctor_password_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', doctor_password_entry,
                                                                                   doctor_password_visibility))
            doctor_password_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', doctor_password_entry,
                                                                                          'Enter Password'))
            doctor_password_entry.bind('<Return>', lambda event: register_doctor())

            # Entry for confirmed Password
            doctor_confirmed_label = tk.Label(doctor_entries_frame, text='Confirm Password', font=('Open Sans', 12, 'bold'),
                                              bg='white', fg='#000000')
            doctor_confirmed_label.grid(row=11, column=4, padx=110, pady=(5, 0), sticky='w')
            doctor_confirmed_entry_frame = tk.Frame(doctor_entries_frame, bg='#D0F9EF', width=380, height=45)
            doctor_confirmed_entry_frame.grid(row=12, column=4, padx=113, pady=(0, 5))
            doctor_confirmed_entry = tk.Entry(doctor_confirmed_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                              border=0, width=42, show='')
            doctor_confirmed_entry.place(x=10, y=12)
            doctor_confirmed_entry.insert(0, 'Re-enter Password')
            doctor_confirmed_eye_closed_button = ttk.Button(doctor_confirmed_entry_frame, style='eye_closed_green.TButton',
                                                            cursor='hand2')
            doctor_confirmed_eye_closed_button.place(x=330, y=2)
            doctor_confirmed_eye_opened_button = ttk.Button(doctor_confirmed_entry_frame, style='eye_opened_green.TButton',
                                                            cursor='hand2')
            doctor_confirmed_visibility = tk.Label(doctor_confirmed_entry_frame, text='Close')
            doctor_confirmed_eye_closed_button.config(command=lambda: self.show_hide_password(doctor_confirmed_entry,
                                                                                              doctor_confirmed_eye_opened_button,
                                                                                              doctor_confirmed_eye_closed_button,
                                                                                              doctor_confirmed_visibility))
            doctor_confirmed_eye_opened_button.config(command=lambda: self.show_hide_password(doctor_confirmed_entry,
                                                                                              doctor_confirmed_eye_opened_button,
                                                                                              doctor_confirmed_eye_closed_button,
                                                                                              doctor_confirmed_visibility))
            doctor_confirmed_entry.bind('<FocusIn>', lambda event: self.focus_entry('password', doctor_confirmed_entry,
                                                                                    doctor_confirmed_visibility))
            doctor_confirmed_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('password', doctor_confirmed_entry,
                                                                                           'Re-enter Password'))
            doctor_confirmed_entry.bind('<Return>', lambda event: register_doctor())

            doctor_validate_register_label = tk.Label(add_back_frame, text='', font=('Open Sans', 8), anchor='e', width=30,
                                                      bg='white', fg='red')
            doctor_validate_register_label.place(x=700, y=30)

            add_button.config(command=lambda: register_doctor())

            decide_left_right_list()
            self.switch('new_doctor', self.all_doctor_list_frames)
            doctor_entries_canvas.yview_moveto(0)

        def show_doctor_details(doctor_id):
            def edit_doctor_details():
                d_name_entry.config(state='normal', fg='#333333')
                d_image_entry.config(fg='#333333')
                d_image_button.config(state='normal')
                d_ic_passport_entry.config(state='normal', fg='#333333')
                d_gender_entry.config(fg='#333333')
                d_gender_button.config(state='normal')
                d_contact_entry.config(state='normal', fg='#333333')
                d_address_entry.config(state='normal', fg='#333333')
                d_language_entry.config(state='normal', fg='#333333')
                d_working_hours_entry.config(state='normal', fg='#333333')
                d_specialise_entry.config(state='normal', fg='#333333')
                d_status_button.config(state='normal')
                d_status_entry.config(fg='#333333')

                save_button.grid(row=0, column=0, padx=20, pady=5, sticky='e', columnspan=2)
                edit_button.grid_forget()

            def save_doctor_details():
                # Check if all entry boxes have black foreground color (#333333)
                if all([entry.cget('fg') == '#333333' for entry in [d_name_entry, d_ic_passport_entry, d_image_entry, d_gender_entry,
                                                                    d_address_entry, d_language_entry, d_contact_entry,
                                                                    d_working_hours_entry, d_specialise_entry, d_status_entry]]):
                    d_name = d_name_entry.get()
                    d_ic_passport = d_ic_passport_entry.get()
                    d_gender = d_gender_entry.cget('text')
                    d_contact = d_contact_entry.get()
                    d_address = d_address_entry.get('1.0', 'end-1c')
                    d_language = d_language_entry.get()
                    d_working_hours = d_working_hours_entry.get()
                    d_specialise = d_specialise_entry.get()
                    d_status = 1 if d_status_entry.cget('text').lower() == "active" else 0

                    img_binary_data = None
                    # Check if a new image has been selected
                    if self.doctor_image_var:
                        img = self.doctor_image_var
                        if img.lower().endswith(('.jpg', '.jpeg', '.png')):
                            with open(img, 'rb') as file:
                                img_binary_data = file.read()

                    # Perform data validation
                    if all([d_name, d_ic_passport, d_gender, d_contact, d_address, d_language, d_working_hours, d_specialise]):
                        if img_binary_data is not None:
                            cursor.execute('''UPDATE doctor
                                           SET doctor_name=%s, doctor_address=%s, doctor_ic_passport=%s, doctor_language=%s,
                                           doctor_working_hour=%s, doctor_contact=%s, doctor_specialize=%s, doctor_image=%s,
                                           doctor_gender=%s, doctor_status=%s
                                           WHERE doctor_id = %s''',
                                           (d_name, d_address, d_ic_passport, d_language, d_working_hours, d_contact,
                                            d_specialise, img_binary_data, d_gender, d_status, doctor_id))
                        else:
                            cursor.execute('''UPDATE doctor
                                           SET doctor_name=%s, doctor_address=%s, doctor_ic_passport=%s, doctor_language=%s,
                                           doctor_working_hour=%s, doctor_contact=%s, doctor_specialize=%s,
                                           doctor_gender=%s, doctor_status=%s
                                           WHERE doctor_id = %s''',
                                           (d_name, d_address, d_ic_passport, d_language, d_working_hours,
                                            d_contact, d_specialise, d_gender, d_status, doctor_id))
                        database.commit()
                        edit_button.grid(row=0, column=0, padx=20, pady=5, sticky='e', columnspan=2)
                        save_button.grid_forget()

                        messagebox.showinfo('Success', 'Doctor details updated successfully')

                        show_doctor_list()
                        show_doctor_details(doctor_id)
                    else:
                        messagebox.showerror('Error', 'Please fill in all the details')

            for widget in right_frame_content.winfo_children():
                widget.destroy()

            self.doctor_image_var = None

            # Ensure doctor_id is passed correctly
            cursor.execute('''
                           SELECT doctor.doctor_name, doctor.doctor_gender, doctor.doctor_address, doctor.doctor_ic_passport, 
                                  doctor.doctor_language, doctor.doctor_working_hour, doctor.doctor_contact, 
                                  doctor.doctor_specialize, user.user_email, doctor.doctor_image, doctor.doctor_status 
                           FROM doctor 
                           JOIN user ON doctor.user_id = user.user_id 
                           WHERE doctor.doctor_id = %s''', (doctor_id,))
            doctor = cursor.fetchone()
            if doctor:
                doctor_name, doctor_gender, doctor_address, doctor_ic_passport, doctor_language, \
                    doctor_working_hour, doctor_contact, doctor_specialise, doctor_email, doctor_image, doctor_status = doctor

                d_information_title = tk.Label(right_frame_content, text='Doctor Information', bg='white',
                                               font=('Open Sans', 12, 'bold', 'underline'), width=65)
                d_information_title.grid(row=0, column=0, columnspan=2, padx=15)

                # Edit button
                edit_button = ttk.Button(right_frame_content, text='Edit', style='white_word.TButton', width=5, cursor='hand2',
                                         command=lambda: edit_doctor_details())
                edit_button.grid(row=0, column=0, padx=20, pady=5, sticky='e', columnspan=2)

                save_button = ttk.Button(right_frame_content, text='Save', style='white_word.TButton', width=5,
                                         cursor='hand2', command=lambda: save_doctor_details())

                d_email = tk.Label(right_frame_content, text="Email:", bg='white', font=("Open Sans", 12))
                d_email.grid(row=1, column=0, padx=15, pady=5, sticky='e')
                d_email_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_email_entry_frame.grid(row=1, column=1, padx=25, pady=5, sticky='w')
                d_email_entry = tk.Entry(d_email_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                         fg='#858585', border=0)
                d_email_entry.insert(0, doctor_email)
                d_email_entry.place(x=10, y=6)
                d_email_entry.config(state='disabled', disabledbackground='#D0F9EF')

                # Display the details in entry widgets
                d_name_label = tk.Label(right_frame_content, text="Doctor Name:", bg='white', font=("Open Sans", 12))
                d_name_label.grid(row=2, column=0, padx=15, pady=5, sticky='e')
                d_name_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_name_entry_frame.grid(row=2, column=1, padx=25, pady=5, sticky='w')
                d_name_entry = tk.Entry(d_name_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=48)
                d_name_entry.insert(0, doctor_name)
                d_name_entry.place(x=10, y=6)
                d_name_entry.config(state='disabled', disabledbackground='#D0F9EF')

                # Display the filename in the entry box
                d_image_label = tk.Label(right_frame_content, text="Image:", bg='white', font=("Open Sans", 12))
                d_image_label.grid(row=3, column=0, padx=15, pady=5, sticky='e')
                d_image_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_image_entry_frame.grid(row=3, column=1, padx=25, pady=5, sticky='w')
                d_image_entry = tk.Label(d_image_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0,
                                         width=48, justify='left', anchor='w')
                d_image_entry.place(x=10, y=6)
                file_type = imghdr.what(None, doctor_image)
                d_image_entry.config(text=f"{doctor_name}.{file_type}")
                d_image_button = ttk.Button(d_image_entry_frame, text='⇫', style='selection.TButton', width=4, cursor='hand2',
                                            command=lambda: self.upload_doctor_image(d_image_entry, 100, 100, img_label))
                d_image_button.place(x=350, y=0)
                d_image_button.config(state='disabled')

                img_label = tk.Label(right_frame_content, bg='white', anchor='w')
                img_label.grid(row=4, column=1, padx=25, pady=5, sticky='w')
                img = Image.open(io.BytesIO(doctor_image))
                img = img.resize((100, 100), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                img_label.config(image=img)
                img_label.image = img

                d_ic_passport = tk.Label(right_frame_content, text="IC/Passport Number:", bg='white',
                                         font=("Open Sans", 12))
                d_ic_passport.grid(row=5, column=0, padx=15, pady=5, sticky='e')
                d_ic_passport_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_ic_passport_entry_frame.grid(row=5, column=1, padx=25, pady=5, sticky='w')
                d_ic_passport_entry = tk.Entry(d_ic_passport_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                               fg='#858585', border=0, width=48)
                d_ic_passport_entry.insert(0, doctor_ic_passport)
                d_ic_passport_entry.place(x=10, y=6)
                d_ic_passport_entry.config(state='disabled', disabledbackground='#D0F9EF')

                d_gender_label = tk.Label(right_frame_content, text='Gender:', font=("Open Sans", 12), bg='white')
                d_gender_label.grid(row=6, column=0, padx=15, pady=5, sticky='e')
                d_gender_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_gender_entry_frame.grid(row=6, column=1, padx=25, pady=5, sticky='w')
                d_gender_entry = tk.Label(d_gender_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
                d_gender_entry.place(x=8, y=4)
                d_gender_entry.config(text=doctor_gender)
                d_gender_button = ttk.Button(d_gender_entry_frame, text='▼', style='selection.TButton', width=4,
                                             cursor='hand2', command=lambda: self.display_menu(d_gender_entry_frame, 0, 27,
                                                                                               d_gender_menu))
                d_gender_button.place(x=350, y=0)
                d_gender_menu = tk.Menu(right_frame_content, tearoff=0, bg='#D0F9EF', fg='#333333',
                                        font=('Open Sans', 10))
                d_gender_menu.add_command(label="Male", command=lambda: self.select_menu_option(d_gender_entry, 'Male'))
                d_gender_menu.add_command(label="Female", command=lambda: self.select_menu_option(d_gender_entry, 'Female'))
                d_gender_menu.add_separator()
                d_gender_menu.add_command(label="Cancel\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ",
                                          command=d_gender_menu.unpost)
                d_gender_button.config(state='disabled')

                d_contact = tk.Label(right_frame_content, text="Contact Number:", bg='white',
                                     font=("Open Sans", 12))
                d_contact.grid(row=7, column=0, padx=15, pady=5, sticky='e')
                d_contact_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_contact_entry_frame.grid(row=7, column=1, padx=25, pady=5, sticky='w')
                d_contact_entry = tk.Entry(d_contact_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                           fg='#858585', border=0, width=48)
                d_contact_entry.insert(0, doctor_contact)
                d_contact_entry.place(x=10, y=6)
                d_contact_entry.config(state='disabled', disabledbackground='#D0F9EF')

                d_address = tk.Label(right_frame_content, text="Address:", bg='white', font=("Open Sans", 12))
                d_address.grid(row=8, column=0, padx=15, pady=5, sticky='ne')
                d_address_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=60)
                d_address_entry_frame.grid(row=8, column=1, padx=25, pady=5, sticky='w')
                d_address_entry = tk.Text(d_address_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                          border=0, width=48, height=3, wrap='word')
                d_address_entry.insert('1.0', doctor_address)
                d_address_entry.place(x=10, y=6)
                d_address_entry.config(state='disabled')

                d_language = tk.Label(right_frame_content, text="Language:", bg='white', font=("Open Sans", 12))
                d_language.grid(row=9, column=0, padx=15, pady=5, sticky='e')
                d_language_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_language_entry_frame.grid(row=9, column=1, padx=25, pady=5, sticky='w')
                d_language_entry = tk.Entry(d_language_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585',
                                           border=0, width=48)
                d_language_entry.insert(0, doctor_language)
                d_language_entry.place(x=10, y=6)
                d_language_entry.config(state='disabled', disabledbackground='#D0F9EF')

                d_workingHours = tk.Label(right_frame_content, text="Working Hours:", bg='white', font=("Open Sans", 12))
                d_workingHours.grid(row=10, column=0, padx=15, pady=5, sticky='e')
                d_working_hours_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_working_hours_entry_frame.grid(row=10, column=1, padx=25, pady=5, sticky='w')
                d_working_hours_entry = tk.Entry(d_working_hours_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                                fg='#858585', border=0, width=48)
                d_working_hours_entry.insert(0, doctor_working_hour)
                d_working_hours_entry.place(x=10, y=6)
                d_working_hours_entry.config(state='disabled', disabledbackground='#D0F9EF')

                d_specialise = tk.Label(right_frame_content, text="Specialize In:", bg='white', font=("Open Sans", 12))
                d_specialise.grid(row=11, column=0, padx=15, pady=5, sticky='e')
                d_specialise_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_specialise_entry_frame.grid(row=11, column=1, padx=25, pady=5, sticky='w')
                d_specialise_entry = tk.Entry(d_specialise_entry_frame, font=('Open Sans', 10), bg='#D0F9EF',
                                             fg='#858585', border=0, width=48)
                d_specialise_entry.insert(0, doctor_specialise)
                d_specialise_entry.place(x=10, y=6)
                d_specialise_entry.config(state='disabled', disabledbackground='#D0F9EF')

                d_status = tk.Label(right_frame_content, text="Status:", bg='white', font=("Open Sans", 12))
                d_status.grid(row=12, column=0, padx=15, pady=(5, 25), sticky='e')
                d_status_entry_frame = tk.Frame(right_frame_content, bg='#D0F9EF', width=400, height=30)
                d_status_entry_frame.grid(row=12, column=1, padx=25, pady=(5, 25), sticky='w')
                d_status_entry = tk.Label(d_status_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
                d_status_entry.place(x=8, y=4)
                d_status_text = "Active" if doctor_status == 1 else "Inactive"
                d_status_entry.config(text=d_status_text)
                d_status_button = ttk.Button(d_status_entry_frame, text='▼', style='selection.TButton', width=4, cursor='hand2',
                                             command=lambda: self.display_menu(d_status_entry_frame, 0, 27, d_status_menu))
                d_status_button.place(x=350, y=0)
                d_status_menu = tk.Menu(right_frame_content, tearoff=0, bg='#D0F9EF', fg='#333333',
                                        font=('Open Sans', 10))
                d_status_menu.add_command(label="Active", command=lambda: self.select_menu_option(d_status_entry, 'Active'))
                d_status_menu.add_command(label="Inactive",
                                          command=lambda: self.select_menu_option(d_status_entry, 'Inactive'))
                d_status_menu.add_separator()
                d_status_menu.add_command(label="Cancel\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ",
                                          command=d_status_menu.unpost)
                d_status_button.config(state='disabled')

                decide_left_right_list()
                self.switch('doctor_list', self.all_doctor_list_frames)
                right_canvas.yview_moveto(0)

        def decide_left_right_list():
            if len(right_frame_content.winfo_children()) == 0:
                self.all_doctor_list_frames['doctor_list'] = [doctor_list_frame, left_canvas, left_frame_content, 0]
            else:
                self.all_doctor_list_frames['doctor_list'] = [doctor_list_frame, right_canvas, right_frame_content, 0]

        for widget in self.doctor_list_frame.winfo_children():
            widget.destroy()

        # Doctor List Frame
        doctor_list_frame = tk.Frame(self.doctor_list_frame, width=1050, height=510, bg='white')
        add_doctor_button = ttk.Button(doctor_list_frame, text='Add Doctor', style='white_word.TButton',
                                       cursor='hand2', width=15, padding=5, command=lambda: show_add_doctor_frame())
        add_doctor_button.place(x=840, y=20)

        doctor_frame = tk.Frame(doctor_list_frame, width=900, height=395, bg='white', highlightthickness=0.5)
        doctor_frame.place(x=80, y=80)

        left_frame = tk.Frame(doctor_frame, width=200, height=395, bg='white')
        left_frame.place(x=0, y=0)
        left_canvas = tk.Canvas(left_frame, width=200, height=395, bg='white', highlightthickness=0)
        left_canvas.place(x=0, y=0)
        left_scrollbar = tk.Scrollbar(left_frame, orient='vertical', command=left_canvas.yview)
        left_scrollbar.place(x=185, y=0, height=395)
        left_canvas.configure(yscrollcommand=left_scrollbar.set)
        left_frame_content = tk.Frame(left_canvas, bg='white')
        left_canvas.create_window((0, 0), window=left_frame_content, anchor='nw')

        right_frame = tk.Frame(doctor_frame, width=700, height=395, bg='white')
        right_frame.place(x=200, y=0)
        right_canvas = tk.Canvas(right_frame, width=700, height=395, bg='white', highlightthickness=0)
        right_canvas.place(x=0, y=0)
        right_scrollbar = tk.Scrollbar(right_frame, orient='vertical', command=right_canvas.yview)
        right_scrollbar.place(x=685, y=0, height=395)
        right_canvas.configure(yscrollcommand=right_scrollbar.set)
        right_frame_content = tk.Frame(right_canvas, bg='white')
        right_canvas.create_window((0, 0), window=right_frame_content, anchor='nw')

        # Add doctor frame
        add_doctor_frame = tk.Frame(self.doctor_list_frame, width=1050, height=510, bg='white')
        add_back_frame = tk.Frame(add_doctor_frame, bg='white', width=1050, height=65,
                                  highlightbackground="white", highlightthickness=0)
        add_back_frame.place(x=0, y=0)
        add_button = ttk.Button(add_back_frame, text='Add', style='white_word.TButton',
                                cursor='hand2', width=10, padding=4)
        add_button.place(x=895, y=20)
        back_button = ttk.Button(add_back_frame, style='back.TButton', cursor='hand2',
                                 command=lambda: show_doctor_list())
        back_button.place(x=20, y=10)

        # Create a canvas
        doctor_entries_canvas = tk.Canvas(add_doctor_frame, bg='white', width=1050, height=445, highlightthickness=0)
        doctor_entries_canvas.place(x=0, y=80)
        # Add scrollbar to the canvas
        scrollbar = tk.Scrollbar(add_doctor_frame, orient='vertical', command=doctor_entries_canvas.yview)
        scrollbar.place(x=1030, y=80, height=445)
        doctor_entries_canvas.configure(yscrollcommand=scrollbar.set)
        # Create a frame to hold the entries
        doctor_entries_frame = tk.Frame(doctor_entries_canvas, bg='white')
        # Add the frame to the canvas
        doctor_entries_canvas.create_window((0, 0), window=doctor_entries_frame, anchor='nw')
        self.all_doctor_list_frames['new_doctor'] = [add_doctor_frame, doctor_entries_canvas, doctor_entries_frame, 0]

        show_doctor_list()

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()

    def on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def display_menu(self, frame, x, y, menu):
        root_x = frame.winfo_rootx()
        root_y = frame.winfo_rooty()
        adjusted_x = root_x + x
        adjusted_y = root_y + y

        menu.post(adjusted_x, adjusted_y)

    def select_menu_option(self, label, option, text=None):
        if option == 'Clear':
            label.config(text=text, fg='#858585')
        else:
            label.config(text=option, fg='#333333')

    def focus_entry(self, entry_type, entry, visibility=None):
        if entry_type == 'entry':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
        elif entry_type == 'text':
            if entry.cget('fg') == '#858585':
                entry.delete('1.0', 'end')
                entry.config(fg='#333333')
        elif entry_type == 'password':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
                if visibility.cget('text') == 'Open':
                    entry.config(show='')
                elif visibility.cget('text') == 'Close':
                    entry.config(show='*')

    def leave_focus_entry(self, entry_type, entry, text):
        if entry_type == 'entry':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585')
                entry.insert(0, text)
        elif entry_type == 'text':
            value = entry.get('1.0', 'end')
            if value.strip() == '':
                entry.delete('1.0', 'end')
                entry.config(fg='#858585')
                entry.insert('1.0', text)
        elif entry_type == 'password':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585', show='')
                entry.insert(0, text)

    def show_hide_password(self, entry, eye_open_button, eye_close_button, visibility):
        if visibility.cget('text') == 'Close' and entry.cget('fg') == '#858585':
            eye_open_button.place(x=320, y=2)
            eye_close_button.place_forget()
            entry.config(show='')
            visibility.config(text='Open')
        elif visibility.cget('text') == 'Open' and entry.cget('fg') == '#858585':
            eye_open_button.place_forget()
            eye_close_button.place(x=320, y=2)
            entry.config(show='')
            visibility.config(text='Close')
        elif visibility.cget('text') == 'Open':
            eye_open_button.place_forget()
            eye_close_button.place(x=320, y=2)
            entry.config(show='*')
            visibility.config(text='Close')
        elif visibility.cget('text') == 'Close':
            eye_open_button.place(x=320, y=2)
            eye_close_button.place_forget()
            entry.config(show='')
            visibility.config(text='Open')

    def upload_doctor_image(self, entry, size_x, size_y, label):
        file_path = filedialog.askopenfilename(initialdir="/gui/images", title="Select an Image", filetypes=(
            ("JPEG files", "*.jpg;*.jpeg"), ("PNG files", "*.png"), ("All files", "*.*")))
        if file_path:
            img_name = os.path.basename(file_path)
            if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Update the entry text
                entry.config(text=img_name, fg='#333333')
                self.doctor_image_var = file_path  # Store the file path of the uploaded image
                # Display the new image in the UI
                img = Image.open(file_path)
                img = img.resize((size_x, size_y), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                label.config(image=img)
                label.image = img
            else:
                messagebox.showerror("Error", "Invalid Image Format")


class Doctor:
    def __init__(self, main_window, user_id):
        self.root_window = main_window
        self.user_id = user_id

        self.window = tk.Toplevel(self.root_window)
        self.window.title('Call a Doctor')
        self.window.geometry('1050x600')
        icon = load_image('icon', 48, 48)
        self.window.iconphoto(False, icon)

        self.nf_icon = load_image('nf icon', 80, 70)

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('navigation.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        font=('Open Sans', 20, 'bold'))
        style.map('navigation.TButton', background=[('active', 'white')], foreground=[('active', '#77C7B5')])

        self.navigation_frame = tk.Frame(self.window, width=1050, height=90, bg='white')
        self.navigation_frame.pack()
        self.navigation_bar = tk.Frame(self.navigation_frame, height=5, bg='#166E82')

        nf_icon = tk.Label(self.navigation_frame, image=self.nf_icon, bg='white')
        nf_icon.place(x=10, y=10)
        nf_name = tk.Label(self.navigation_frame, text='CaD', font=('Open Sans', 30, 'bold'), bg='white', fg='#166E82')
        nf_name.place(x=90, y=20)
        nf_patient_button = ttk.Button(self.navigation_frame, text='Patient Appointment', style='navigation.TButton', width=18,
                                       command=lambda: self.show_activity_frame(285, 521, self.patient_frame))
        nf_patient_button.place(x=520, y=30)
        nf_timetable_button = ttk.Button(self.navigation_frame, text='Timetable', style='navigation.TButton', width=9,
                                         command=lambda: self.show_activity_frame(150, 818, self.timetable_frame))
        nf_timetable_button.place(x=817, y=30)
        nf_me_button = ttk.Button(self.navigation_frame, text='Me', style='navigation.TButton', width=3,
                                  command=lambda: self.show_activity_frame(60, 976, self.me_frame))
        nf_me_button.place(x=975, y=30)

        self.patient_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.timetable_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

    def run(self):
        self.window.deiconify()
        self.initialize_new_login()

    def initialize_new_login(self):
        self.set_up_patient_frame()
        self.set_up_timetable_frame()
        self.set_up_me_frame()

        self.show_activity_frame(285, 521, self.patient_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.patient_frame.pack_forget()
        self.timetable_frame.pack_forget()
        self.me_frame.pack_forget()

        frame.pack()
        self.window.focus_set()

    def set_up_patient_frame(self):
        for widget in self.patient_frame.winfo_children():
            widget.destroy()

    def set_up_timetable_frame(self):
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()


class Admin:
    def __init__(self, main_window, user_id):
        self.root_window = main_window
        self.user_id = user_id

        self.window = tk.Toplevel(self.root_window)
        self.window.title('Call a Doctor')
        self.window.geometry('1050x600')
        icon = load_image('icon', 48, 48)
        self.window.iconphoto(False, icon)

        self.nf_icon = load_image('nf icon', 80, 70)
        self.search_button = load_image('search button', 18, 18)
        self.clear_search = load_image('clear search', 15, 15)

        self.clinic_images = {}
        self.doctor_images = {}

        style = ttk.Style()
        style.theme_use('clam')

        style.configure('navigation.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        font=('Open Sans', 20, 'bold'))
        style.map('navigation.TButton', background=[('active', 'white')], foreground=[('active', '#77C7B5')])
        style.configure('back.TButton', border=0, relief='flat', background='white', foreground='#7EE5CE',
                        font=('Open Sans', 18, 'bold'))
        style.map('back.TButton', background=[('active', 'white')], foreground=[('active', '#77C7B5')])

        self.navigation_frame = tk.Frame(self.window, width=1050, height=90, bg='white')
        self.navigation_frame.pack()
        self.navigation_bar = tk.Frame(self.navigation_frame, height=5, bg='#166E82')

        nf_icon = tk.Label(self.navigation_frame, image=self.nf_icon, bg='white', cursor='hand2')
        nf_icon.place(x=10, y=10)
        nf_icon.bind('<Button-1>', lambda event: self.refresh())
        nf_name = tk.Label(self.navigation_frame, text='CaD', cursor='hand2', font=('Open Sans', 30, 'bold'), bg='white', fg='#166E82')
        nf_name.place(x=90, y=20)
        nf_name.bind('<Button-1>', lambda event: self.refresh())
        nf_clinic_button = ttk.Button(self.navigation_frame, text='Clinic', style='navigation.TButton', width=5,
                                      command=lambda: self.show_activity_frame(90, 660, self.clinic_frame))
        nf_clinic_button.place(x=658, y=30)
        nf_clinic_request_button = ttk.Button(self.navigation_frame, text='Clinic Request', style='navigation.TButton', width=13,
                                              command=lambda: self.show_activity_frame(210, 758, self.clinic_request_frame))
        nf_clinic_request_button.place(x=757, y=30)
        nf_me_button = ttk.Button(self.navigation_frame, text='Me', style='navigation.TButton', width=3,
                                  command=lambda: self.show_activity_frame(60, 976, self.me_frame))
        nf_me_button.place(x=975, y=30)

        self.clinic_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.all_clinic_frames = {}

        self.clinic_request_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

        self.all_scrollable_frame = {}
        self.all_scrollable_frame[self.clinic_frame] = 1
        self.all_scrollable_frame[self.clinic_request_frame] = 0
        self.all_scrollable_frame[self.me_frame] = 0

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

        self.clinic_images = {}
        self.doctor_images = {}

        self.all_clinic_frames = {}

        self.all_scrollable_frame = {}
        self.all_scrollable_frame[self.clinic_frame] = 1
        self.all_scrollable_frame[self.clinic_request_frame] = 0
        self.all_scrollable_frame[self.me_frame] = 0

    def run(self):
        self.window.deiconify()
        self.refresh()

    def refresh(self):
        self.set_up_clinic_request_frame()
        self.set_up_me_frame()
        self.set_up_clinic_frame()

        if self.all_scrollable_frame[self.clinic_frame] == 1:
            self.show_activity_frame(90, 660, self.clinic_frame)
        elif self.all_scrollable_frame[self.clinic_request_frame] == 1:
            self.show_activity_frame(210, 758, self.clinic_request_frame)
        elif self.all_scrollable_frame[self.me_frame] == 1:
            self.show_activity_frame(60, 976, self.me_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.clinic_frame.pack_forget()
        self.clinic_request_frame.pack_forget()
        self.me_frame.pack_forget()

        frame.pack()
        frame.focus_set()

        key = list(self.all_scrollable_frame.keys())
        for k in key:
            if k == frame:
                self.all_scrollable_frame[k] = 1
            else:
                self.all_scrollable_frame[k] = 0

        if frame == self.clinic_frame:
            keys = list(self.all_clinic_frames.keys())
            for k in keys:
                active = self.all_clinic_frames[k][3]
                if active:
                    self.switch(k, self.all_clinic_frames)

    def switch(self, frame, frame_list):
        frames = list(frame_list.keys())
        for f in frames:
            if f == frame:
                frame_list[f][3] = 1
                frame_list[f][0].pack()
            else:
                frame_list[f][3] = 0
                frame_list[f][0].pack_forget()
        content = frame_list[frame][2]
        canvas = frame_list[frame][1]
        content.update_idletasks()
        if len(content.winfo_children()) == 0:
            canvas.configure(scrollregion=(0, 0, 0, 0))
        else:
            canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.bind_all("<MouseWheel>", lambda event: self.on_mouse_wheel(event, canvas))

    def set_up_clinic_frame(self):

        def clear_search():
            search_entry.delete(0, tk.END)
            show_clinics()
            clinic_canvas.yview_moveto(0)

        def search():
            show_clinics()
            clinic_canvas.yview_moveto(0)

        def show_clinics():
            self.leave_focus_entry('entry', search_entry, 'Search')
            clinics_frame.focus_set()
            for w in clinic_content_frame.winfo_children():
                w.destroy()

            if search_entry.cget('fg') == '#858585':
                clear_search_button.place_forget()
                cursor.execute('''SELECT * FROM clinic ORDER BY clinic_status DESC, clinic_name ASC''')
                clinics = cursor.fetchall()
            elif search_entry.cget('fg') == '#333333':
                clear_search_button.place(x=170, y=8)
                search_query = search_entry.get().strip()
                cursor.execute('''SELECT * FROM clinic WHERE (clinic_name LIKE %s OR clinic_address LIKE %s)
                               ORDER BY clinic_status DESC, clinic_name ASC''',
                               ('%'+search_query+'%', '%'+search_query+'%', ))
                clinics = cursor.fetchall()

            x_value = 15
            count = 1
            if clinics:
                for clinic in clinics:
                    if count % 2 == 0:
                        y_value = 25
                    else:
                        y_value = 0

                    clinic_id = clinic[0]

                    image_stream = BytesIO(clinic[6])
                    img = Image.open(image_stream)
                    resized_img = img.resize((240, 200), Image.LANCZOS)
                    tk_image = ImageTk.PhotoImage(resized_img)
                    self.clinic_images[clinic_id] = tk_image

                    clinic_frame = tk.Frame(clinic_content_frame, height=200, width=1000, bg='white', highlightbackground='#166E82',
                                            highlightthickness=0.5, cursor='hand2')
                    clinic_frame.pack(padx=x_value, pady=y_value, fill='y', expand=True)
                    clinic_image = tk.Label(clinic_frame, image=self.clinic_images[clinic_id], bg='white')
                    clinic_image.grid(row=0, column=0, padx=20, pady=10, rowspan=4)
                    clinic_name = tk.Label(clinic_frame, text=clinic[1], font=('Open Sans', 20, 'bold'), bg='white', fg='#000000')
                    clinic_name.grid(row=0, column=1, sticky='w', columnspan=2, pady=(20, 10))
                    clinic_address_label = tk.Label(clinic_frame, text='Address: ', font=('Open Sans', 16), bg='white', fg='#000000')
                    clinic_address_label.grid(row=1, column=1, sticky='nw', pady=(0, 5))
                    clinic_address = tk.Label(clinic_frame, text=clinic[3].strip(), font=('Open Sans', 16), bg='white', fg='#000000',
                                              anchor='w', width=51, wraplength=620, justify='left')
                    clinic_address.grid(row=1, column=2, sticky='nw', pady=(0, 5))
                    clinic_operation_label = tk.Label(clinic_frame, text='Hours: ', font=('Open Sans', 16), bg='white',
                                                      fg='#000000')
                    clinic_operation_label.grid(row=2, column=1, sticky='w', pady=(0, 5))
                    clinic_operation = tk.Label(clinic_frame, text=clinic[2], font=('Open Sans', 16), bg='white', fg='#000000')
                    clinic_operation.grid(row=2, column=2, sticky='w', pady=(0, 5))
                    clinic_contact_label = tk.Label(clinic_frame, text='Contact: ', font=('Open Sans', 16),
                                                    bg='white', fg='#000000')
                    clinic_contact_label.grid(row=3, column=1, sticky='w', pady=(5, 20))
                    clinic_contact = tk.Label(clinic_frame, text=clinic[5], font=('Open Sans', 16), bg='white', fg='#000000')
                    clinic_contact.grid(row=3, column=2, sticky='w', pady=(5, 20))

                    clinic_frame.bind('<Button-1>', lambda event, c=clinic: show_new_detail(c))
                    for widgets in clinic_frame.winfo_children():
                        widgets.bind('<Button-1>', lambda event, c=clinic: show_new_detail(c))

                    if clinic[7] == 0:
                        clinic_frame.config(bg='#D3CCCC')
                        for widgets in clinic_frame.winfo_children():
                            widgets.config(bg='#D3CCCC')

                    count += 1

            self.switch('clinic', self.all_clinic_frames)

        def show_new_detail(c):
            show_detail(c)
            detail_canvas.yview_moveto(0)

        def show_detail(c):
            if c[7] == 0:
                inactive_label.place(x=898, y=15)
            else:
                inactive_label.place_forget()
            d_back_button.config(command=lambda: show_clinics())

            for w in detail_content_frame.winfo_children():
                w.destroy()

            clinic_id = c[0]
            clinic_frame = tk.Frame(detail_content_frame, height=200, width=1000, bg='white')
            clinic_frame.pack(padx=15, fill='y', expand=True)
            clinic_image = tk.Label(clinic_frame, image=self.clinic_images[clinic_id], bg='white')
            clinic_image.grid(row=0, column=0, padx=20, pady=10, rowspan=4)
            clinic_name = tk.Label(clinic_frame, text=c[1], font=('Open Sans', 20, 'bold'), bg='white', fg='#000000')
            clinic_name.grid(row=0, column=1, sticky='w', columnspan=2, pady=(20, 10))
            clinic_address_label = tk.Label(clinic_frame, text='Address: ', font=('Open Sans', 16), bg='white', fg='#000000')
            clinic_address_label.grid(row=1, column=1, sticky='nw', pady=(0, 5))
            clinic_address = tk.Label(clinic_frame, text=c[3].strip(), font=('Open Sans', 16), bg='white', fg='#000000',
                                      anchor='w', width=51, wraplength=620, justify='left')
            clinic_address.grid(row=1, column=2, sticky='nw', pady=(0, 5))
            clinic_operation_label = tk.Label(clinic_frame, text='Hours: ', font=('Open Sans', 16), bg='white',
                                              fg='#000000')
            clinic_operation_label.grid(row=2, column=1, sticky='w', pady=(0, 5))
            clinic_operation = tk.Label(clinic_frame, text=c[2], font=('Open Sans', 16), bg='white', fg='#000000')
            clinic_operation.grid(row=2, column=2, sticky='w', pady=(0, 5))
            clinic_contact_label = tk.Label(clinic_frame, text='Contact: ', font=('Open Sans', 16),
                                            bg='white', fg='#000000')
            clinic_contact_label.grid(row=3, column=1, sticky='w', pady=(5, 20))
            clinic_contact = tk.Label(clinic_frame, text=c[5], font=('Open Sans', 16), bg='white', fg='#000000')
            clinic_contact.grid(row=3, column=2, sticky='w', pady=(5, 20))
            clinic_describe = tk.Label(clinic_frame, text=c[4].strip(), font=('Open Sans', 12), bg='white', fg='#677294',
                                       anchor='w', wraplength=970, justify='left')
            clinic_describe.grid(row=4, column=0, columnspan=3, sticky='w', padx=20)

            doctors_frame = tk.Frame(detail_content_frame, width=1000, bg='white')
            doctors_frame.pack(pady=20, fill='y', expand=True)
            doctor_title = tk.Label(doctors_frame, text='Doctors', font=('Open Sans', 16, 'bold', 'underline'),
                                    bg='white', fg='#000000')
            doctor_title.pack(anchor='center', pady=10)
            cursor.execute('''SELECT * FROM doctor WHERE clinic_id=%s ORDER BY doctor_status DESC, doctor_name ASC''', (clinic_id, ))
            doctors = cursor.fetchall()
            count = 1
            for doctor in doctors:
                if count % 2 == 0:
                    y_value = 10
                else:
                    y_value = 0

                doctor_frame = tk.Frame(doctors_frame, width=700, bg='white')
                doctor_frame.pack(pady=y_value, fill='y', expand=True)

                doctor_id = doctor[0]

                image_stream = BytesIO(doctor[9])
                img = Image.open(image_stream)
                resized_img = img.resize((120, 120), Image.LANCZOS)
                tk_image = ImageTk.PhotoImage(resized_img)
                self.doctor_images[doctor_id] = tk_image

                doctor_image = tk.Label(doctor_frame, image=self.doctor_images[doctor_id], bg='white')
                doctor_image.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
                doctor_name = tk.Label(doctor_frame, text='Dr. '+doctor[1], font=('Open Sans', 14, 'bold'), bg='white', fg='#000000')
                doctor_name.grid(row=0, column=1, columnspan=2, sticky='w', pady=(5, 5))
                doctor_contact_label = tk.Label(doctor_frame, text='Contact: ', font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_contact_label.grid(row=1, column=1, sticky='w', pady=(0, 3))
                doctor_contact = tk.Label(doctor_frame, text=doctor[5], font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_contact.grid(row=1, column=2, sticky='w', pady=(0, 3))
                doctor_working_label = tk.Label(doctor_frame, text='Hours: ', font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_working_label.grid(row=2, column=1, sticky='w', pady=(0, 3))
                doctor_working = tk.Label(doctor_frame, text=doctor[6], font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_working.grid(row=2, column=2, sticky='w', pady=(0, 3))
                doctor_language_label = tk.Label(doctor_frame, text='Language: ', font=('Open Sans', 12), bg='white', fg='#000000')
                doctor_language_label.grid(row=3, column=1, sticky='w', pady=(0, 5))
                languages = sorted(doctor[7].split(', '))
                doctor_language = tk.Label(doctor_frame, text=', '.join(languages), font=('Open Sans', 12), bg='white', fg='#000000',
                                           width=35, anchor='w')
                doctor_language.grid(row=3, column=2, sticky='w', pady=(0, 5))
                specializations = sorted(doctor[8].split(', '))
                doctor_specialize = tk.Label(doctor_frame, text='Specialize In\n'+'\n'.join([f"•{value}" for value in specializations]),
                                             font=('Open Sans', 12), bg='white', fg='#000000', anchor='e', width=20, justify='left')
                doctor_specialize.grid(row=1, column=3, rowspan=3, sticky='nw', padx=30, pady=(0, 5))

                if doctor[10] == 0:
                    doctor_name.config(fg='red', text='Dr. '+doctor[1]+'    (INACTIVE)')

                count += 1

            self.switch('detail', self.all_clinic_frames)

        for widget in self.clinic_frame.winfo_children():
            widget.destroy()

        clinics_frame = tk.Frame(self.clinic_frame, width=1050, height=510, bg='white')
        search_frame = tk.Frame(clinics_frame, bg='#F5F5F5', width=230, height=35, highlightbackground="#C8C7C7",
                                highlightthickness=0.5)
        search_frame.place(x=785, y=15)
        search_entry = tk.Entry(search_frame, bg='#F5F5F5', font=('Roboto', 12), border=0, fg='#858585', width=16)
        search_entry.place(x=8, y=6)
        search_entry.insert(0, "Search")
        search_entry.bind('<FocusIn>', lambda event: self.focus_entry('entry', search_entry))
        search_entry.bind('<FocusOut>', lambda event: self.leave_focus_entry('entry', search_entry, 'Search'))
        search_entry.bind('<Return>', lambda event: search())
        search_button = tk.Button(search_frame, bg='#F5F5F5', image=self.search_button, border=0, cursor='hand2',
                                  command=lambda: search())
        search_button.place(x=200, y=6)
        clear_search_button = tk.Button(search_frame, bg='#F5F5F5', image=self.clear_search, border=0, command=lambda: clear_search())
        clinic_canvas = tk.Canvas(clinics_frame, width=1030, height=430, bg='white', highlightthickness=0)
        clinic_canvas.place(x=0, y=75)
        clinic_scrollbar = tk.Scrollbar(clinics_frame, orient='vertical')
        clinic_scrollbar.place(x=1033, y=75, height=430)
        clinic_canvas.configure(yscrollcommand=clinic_scrollbar.set)
        clinic_scrollbar.configure(command=clinic_canvas.yview)
        clinic_content_frame = tk.Frame(clinic_canvas, bg='white')
        clinic_canvas.create_window((0, 0), window=clinic_content_frame, anchor="nw")
        self.all_clinic_frames['clinic'] = [clinics_frame, clinic_canvas, clinic_content_frame, 0]

        detail_frame = tk.Frame(self.clinic_frame, width=1050, height=510, bg='white')
        d_back_button = ttk.Button(detail_frame, text='< Back', style='back.TButton', cursor='hand2', width=6)
        d_back_button.place(x=20, y=15)
        inactive_label = tk.Label(detail_frame, text='INACTIVE', bg='white', fg='red', font=('Roboto', 18, 'bold'))
        detail_canvas = tk.Canvas(detail_frame, width=1030, height=430, bg='white', highlightthickness=0)
        detail_canvas.place(x=0, y=75)
        detail_scrollbar = tk.Scrollbar(detail_frame, orient='vertical')
        detail_scrollbar.place(x=1033, y=75, height=430)
        detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
        detail_scrollbar.configure(command=detail_canvas.yview)
        detail_content_frame = tk.Frame(detail_canvas, bg='white')
        detail_canvas.create_window((0, 0), window=detail_content_frame, anchor="nw")
        self.all_clinic_frames['detail'] = [detail_frame, detail_canvas, detail_content_frame, 0]

        show_clinics()

    def set_up_clinic_request_frame(self):
        for widget in self.clinic_request_frame.winfo_children():
            widget.destroy()

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()

    def on_mouse_wheel(self, event, canvas):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    def focus_entry(self, entry_type, entry, visibility=None):
        if entry_type == 'entry':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
        elif entry_type == 'text':
            if entry.cget('fg') == '#858585':
                entry.delete('1.0', 'end')
                entry.config(fg='#333333')
        elif entry_type == 'password':
            if entry.cget('fg') == '#858585':
                entry.delete(0, tk.END)
                entry.config(fg='#333333')
                if visibility.cget('text') == 'Open':
                    entry.config(show='')
                elif visibility.cget('text') == 'Close':
                    entry.config(show='*')

    def leave_focus_entry(self, entry_type, entry, text):
        if entry_type == 'entry':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585')
                entry.insert(0, text)
        elif entry_type == 'text':
            value = entry.get('1.0', 'end')
            if value.strip() == '':
                entry.delete('1.0', 'end')
                entry.config(fg='#858585')
                entry.insert('1.0', text)
        elif entry_type == 'password':
            value = entry.get()
            if value.strip() == '':
                entry.delete(0, tk.END)
                entry.config(fg='#858585', show='')
                entry.insert(0, text)


root = LoginRegister()
root.run()

cursor.close()
database.close()
