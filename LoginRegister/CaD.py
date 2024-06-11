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

database = mysql.connector.connect(host="localhost", user="root", password="xueer.1014", database="cad")
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
        nf_clinic_button = ttk.Button(self.navigation_frame, text='Clinic', style='navigation.TButton', width=5,
                                      command=lambda: self.show_activity_frame(90, 475, self.clinic_frame))
        nf_clinic_button.place(x=473, y=30)
        nf_map_button = ttk.Button(self.navigation_frame, text='Map', style='navigation.TButton', width=4,
                                   command=lambda: self.show_activity_frame(75, 576, self.map_frame))
        nf_map_button.place(x=575, y=30)
        nf_appointment_button = ttk.Button(self.navigation_frame, text='Appointment Request', style='navigation.TButton', width=20,
                                           command=lambda: self.show_activity_frame(315, 656, self.appointment_frame))
        nf_appointment_button.place(x=655, y=30)
        nf_me_button = ttk.Button(self.navigation_frame, text='Me', style='navigation.TButton', width=3,
                                  command=lambda: self.show_activity_frame(60, 976, self.me_frame))
        nf_me_button.place(x=975, y=30)

        self.clinic_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.map_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.appointment_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

    def run(self):
        self.window.deiconify()
        self.initialize_new_login()

    def initialize_new_login(self):
        self.set_up_clinic_frame()
        self.set_up_map_frame()
        self.set_up_appointment_frame()
        self.set_up_me_frame()

        self.show_activity_frame(90, 475, self.clinic_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.clinic_frame.pack_forget()
        self.map_frame.pack_forget()
        self.appointment_frame.pack_forget()
        self.me_frame.pack_forget()

        frame.pack()
        self.window.focus_set()

    def set_up_clinic_frame(self):
        for widget in self.clinic_frame.winfo_children():
            widget.destroy()

    def set_up_map_frame(self):
        for widget in self.map_frame.winfo_children():
            widget.destroy()

    def set_up_appointment_frame(self):
        for widget in self.appointment_frame.winfo_children():
            widget.destroy()

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()


class Clinic:
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
        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

    def run(self):
        self.window.deiconify()
        self.initialize_new_login()

    def initialize_new_login(self):
        self.set_up_appointment_frame()
        self.set_up_timetable_frame()
        self.set_up_doctor_list_frame()
        self.set_up_me_frame()

        self.show_activity_frame(315, 327, self.appointment_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.appointment_frame.pack_forget()
        self.timetable_frame.pack_forget()
        self.doctor_list_frame.pack_forget()
        self.me_frame.pack_forget()

        frame.pack()
        self.window.focus_set()

    def set_up_appointment_frame(self):
        for widget in self.appointment_frame.winfo_children():
            widget.destroy()

    def set_up_timetable_frame(self):
        for widget in self.timetable_frame.winfo_children():
            widget.destroy()

    def set_up_doctor_list_frame(self):
        for widget in self.doctor_list_frame.winfo_children():
            widget.destroy()

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()


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
        nf_clinic_button = ttk.Button(self.navigation_frame, text='Clinic', style='navigation.TButton', width=5,
                                      command=lambda: self.show_activity_frame(90, 575, self.clinic_frame))
        nf_clinic_button.place(x=573, y=30)
        nf_map_button = ttk.Button(self.navigation_frame, text='Map', style='navigation.TButton', width=4,
                                   command=lambda: self.show_activity_frame(75, 676, self.map_frame))
        nf_map_button.place(x=675, y=30)
        nf_clinic_request_button = ttk.Button(self.navigation_frame, text='Clinic Request', style='navigation.TButton', width=13,
                                              command=lambda: self.show_activity_frame(210, 758, self.clinic_request_frame))
        nf_clinic_request_button.place(x=757, y=30)
        nf_me_button = ttk.Button(self.navigation_frame, text='Me', style='navigation.TButton', width=3,
                                  command=lambda: self.show_activity_frame(60, 976, self.me_frame))
        nf_me_button.place(x=975, y=30)

        self.clinic_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.map_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.clinic_request_frame = tk.Frame(self.window, width=1050, height=510, bg='white')
        self.me_frame = tk.Frame(self.window, width=1050, height=510, bg='white')

    def logout(self):
        self.window.withdraw()
        self.root_window.deiconify()

    def run(self):
        self.window.deiconify()
        self.initialize_new_login()

    def initialize_new_login(self):
        self.set_up_clinic_frame()
        self.set_up_map_frame()
        self.set_up_clinic_request_frame()
        self.set_up_me_frame()

        self.show_activity_frame(90, 575, self.clinic_frame)

    def show_activity_frame(self, bar_width, bar_x, frame):
        self.navigation_bar.config(width=bar_width)
        self.navigation_bar.place(x=bar_x, y=85)

        self.clinic_frame.pack_forget()
        self.map_frame.pack_forget()
        self.clinic_request_frame.pack_forget()
        self.me_frame.pack_forget()

        frame.pack()
        self.window.focus_set()

    def set_up_clinic_frame(self):
        for widget in self.clinic_frame.winfo_children():
            widget.destroy()

    def set_up_map_frame(self):
        for widget in self.map_frame.winfo_children():
            widget.destroy()

    def set_up_clinic_request_frame(self):
        for widget in self.clinic_request_frame.winfo_children():
            widget.destroy()

    def set_up_me_frame(self):
        for widget in self.me_frame.winfo_children():
            widget.destroy()


root = LoginRegister()
root.run()

cursor.close()
database.close()
