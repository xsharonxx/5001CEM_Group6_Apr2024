import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import ImageTk, Image
import mysql.connector
from io import BytesIO

database = mysql.connector.connect(host="localhost", user="root", password="xueer.1014", database="cad")
cursor = database.cursor()


def load_image(description, width, height):
    cursor.execute('''SELECT app_image_data FROM app_image WHERE app_image_description=%s''', (description,))
    image_data = cursor.fetchone()
    image_stream = BytesIO(image_data[0])
    img = Image.open(image_stream)
    resized_img = img.resize((width, height), Image.LANCZOS)
    tk_image = ImageTk.PhotoImage(resized_img)
    return tk_image


class LoginRegister:
    def __init__(self, main_window):
        self.frame = tk.Frame(main_window, width=1050, height=600, bg='white')

        self.get_started_background = load_image('bg get started', 1050, 600)
        self.icon = load_image('icon', 100, 90)
        self.lfr_background = load_image('bg login_register as', 1050, 600)
        self.eye_closed_image = load_image('eye closed', 24, 24)
        self.eye_opened_image = load_image('eye opened', 24, 24)

        self.email_var = StringVar()
        self.password_var = StringVar()
        self.confirmed_password_var = StringVar()
        self.name_var = StringVar()
        self.ic_passport_var = StringVar()
        self.gender_var = StringVar()
        self.address_var = StringVar()
        self.contact_var = StringVar()
        self.operation_var = StringVar()
        self.description_var = StringVar()
        self.image_var = None

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
        style.map('eye_closed_grey.TButton', background=[('active', '#F5F5F5')])
        style.configure('eye_closed_green.TButton', border=0, relief='flat', background='#D0F9EF', image=self.eye_closed_image)
        style.map('eye_closed_green.TButton', background=[('active', '#D0F9EF')])
        style.configure('eye_opened_green.TButton', border=0, relief='flat', background='#D0F9EF', image=self.eye_opened_image)
        style.map('eye_closed_green.TButton', background=[('active', '#D0F9EF')])
        style.configure('selection.TButton', border=0, relief='flat', background='#D0F9EF', foreground='#858585',
                        font=('Rubik', 12, 'bold'))
        style.map('selection.TButton', background=[('active', '#D0F9EF')], foreground=[('active', '#4F5871')])

    def hide_frame(self):
        self.frame.pack_forget()

    def show_frame(self):
        self.frame.pack()

    def show_get_started(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
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
        for widget in self.frame.winfo_children():
            widget.destroy()
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
        for widget in self.frame.winfo_children():
            widget.destroy()
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

        l_password_label = tk.Label(self.frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        l_password_label.place(x=620, y=295)
        l_password_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        l_password_entry_frame.place(x=625, y=325)
        l_password_entry = tk.Entry(l_password_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35)
        l_password_entry.place(x=10, y=12)
        l_password_entry.insert(0, 'Enter Your Password')
        l_password_eye_closed_button = ttk.Button(l_password_entry_frame, style='eye_closed_grey.TButton', cursor='hand2')
        l_password_eye_closed_button.place(x=270, y=2)
        l_password_eye_opened_button = ttk.Button(l_password_entry_frame, style='eye_opened_grey.TButton', cursor='hand2')

        l_login_button = ttk.Button(self.frame, text='Login', style='small_green.TButton', cursor='hand2', width=20, padding=5)
        l_login_button.place(x=690, y=410)

        l_forgot_password_grey_button = ttk.Button(self.frame, text='Forgot Password', style='grey_word.TButton', cursor='hand2',
                                                   width=15, command=lambda: self.show_forgot_password())
        l_forgot_password_grey_button.place(x=725, y=445)

        l_text3 = tk.Label(self.frame, text='Don\'t have an account?', bg='#08D5A7', fg='#333333', font=('Rubik', 8, 'bold'))
        l_text3.place(x=810, y=570)
        l_register_as_black_button = ttk.Button(self.frame, text='Register', style='black_word.TButton', cursor='hand2', width=8,
                                                command=lambda: self.show_register_as())
        l_register_as_black_button.place(x=940, y=565)

    def show_forgot_password(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
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

        fp_password_label = tk.Label(self.frame, text='New Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        fp_password_label.place(x=620, y=230)
        fp_password_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        fp_password_entry_frame.place(x=625, y=260)
        fp_password_entry = tk.Entry(fp_password_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35)
        fp_password_entry.place(x=10, y=12)
        fp_password_entry.insert(0, 'Enter New Password')
        fp_password_eye_closed_button = ttk.Button(fp_password_entry_frame, style='eye_closed_grey.TButton', cursor='hand2')
        fp_password_eye_closed_button.place(x=270, y=2)
        fp_password_eye_opened_button = ttk.Button(fp_password_entry_frame, style='eye_opened_grey.TButton', cursor='hand2')

        fp_confirmed_label = tk.Label(self.frame, text='Re-enter New Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        fp_confirmed_label.place(x=620, y=325)
        fp_confirmed_entry_frame = tk.Frame(self.frame, bg='#F5F5F5', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        fp_confirmed_entry_frame.place(x=625, y=355)
        fp_confirmed_entry = tk.Entry(fp_confirmed_entry_frame, font=('Open Sans', 10), bg='#F5F5F5', fg='#858585', border=0, width=35)
        fp_confirmed_entry.place(x=10, y=12)
        fp_confirmed_entry.insert(0, 'Re-enter New Password')
        fp_confirmed_eye_closed_button = ttk.Button(fp_confirmed_entry_frame, style='eye_closed_grey.TButton', cursor='hand2')
        fp_confirmed_eye_closed_button.place(x=270, y=2)
        fp_confirmed_eye_opened_button = ttk.Button(fp_confirmed_entry_frame, style='eye_opened_grey.TButton', cursor='hand2')

        fp_back_button = ttk.Button(self.frame, text='Back', style='small_green.TButton', cursor='hand2', width=20, padding=5,
                                    command=lambda: self.show_login())
        fp_back_button.place(x=690, y=440)
        fp_update_pass_button = ttk.Button(self.frame, text='Update Password', style='small_green.TButton', cursor='hand2', width=20,
                                           padding=5)
        fp_update_pass_button.place(x=690, y=490)

        fp_text3 = tk.Label(self.frame, text='Don\'t have an account?', bg='#08D5A7', fg='#333333', font=('Rubik', 8, 'bold'))
        fp_text3.place(x=810, y=570)
        fp_register_as_black_button = ttk.Button(self.frame, text='Register', style='black_word.TButton', cursor='hand2', width=8,
                                                 command=lambda: self.show_register_as())
        fp_register_as_black_button.place(x=940, y=565)

    def show_registering_user(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

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

        ru_ic_passport_label = tk.Label(self.frame, text='IC or Passport Number', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_ic_passport_label.place(x=120, y=190)
        ru_ic_passport_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                              highlightthickness=0.5)
        ru_ic_passport_entry_frame.place(x=125, y=220)
        ru_ic_passport_entry = tk.Entry(ru_ic_passport_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0,
                                        width=35)
        ru_ic_passport_entry.place(x=10, y=12)
        ru_ic_passport_entry.insert(0, 'Enter Your IC or Passport Number')

        ru_gender_label = tk.Label(self.frame, text='Gender', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_gender_label.place(x=120, y=280)
        ru_gender_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                         highlightthickness=0.5)
        ru_gender_entry_frame.place(x=125, y=310)
        ru_gender_entry = tk.Label(ru_gender_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
        ru_gender_entry.place(x=8, y=10)
        ru_gender_entry.config(text='Select Your Gender')
        ru_gender_button = ttk.Button(ru_gender_entry_frame, text='▼', style='selection.TButton', width=4,
                                      command=lambda: self.display_menu(ru_gender_entry_frame, 1, 40, ru_gender_menu))
        ru_gender_button.place(x=265, y=5)
        ru_gender_menu = tk.Menu(self.frame, tearoff=0, bg='#D0F9EF', fg='#333333', font=('Open Sans', 10))
        ru_gender_menu.add_command(label="Male")
        ru_gender_menu.add_command(label="Female")
        ru_gender_menu.add_separator()
        ru_gender_menu.add_command(label="Cancel\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ", command=ru_gender_menu.unpost)

        ru_address_label = tk.Label(self.frame, text='Address', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_address_label.place(x=120, y=370)
        ru_address_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        ru_address_entry_frame.place(x=125, y=400)
        ru_address_entry = tk.Entry(ru_address_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_address_entry.place(x=10, y=12)
        ru_address_entry.insert(0, 'Enter Your Address')

        ru_contact_label = tk.Label(self.frame, text='Contact Number', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_contact_label.place(x=590, y=100)
        ru_contact_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        ru_contact_entry_frame.place(x=595, y=130)
        ru_contact_entry = tk.Entry(ru_contact_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_contact_entry.place(x=10, y=12)
        ru_contact_entry.insert(0, 'Enter Your Contact Number')

        ru_email_label = tk.Label(self.frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_email_label.place(x=590, y=190)
        ru_email_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        ru_email_entry_frame.place(x=595, y=220)
        ru_email_entry = tk.Entry(ru_email_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_email_entry.place(x=10, y=12)
        ru_email_entry.insert(0, 'Enter Your Email')

        ru_password_label = tk.Label(self.frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_password_label.place(x=590, y=280)
        ru_password_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        ru_password_entry_frame.place(x=595, y=310)
        ru_password_entry = tk.Entry(ru_password_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_password_entry.place(x=10, y=12)
        ru_password_entry.insert(0, 'Enter Your Password')
        ru_password_eye_closed_button = ttk.Button(ru_password_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        ru_password_eye_closed_button.place(x=270, y=2)
        ru_password_eye_opened_button = ttk.Button(ru_password_entry_frame, style='eye_opened_green.TButton', cursor='hand2')

        ru_confirmed_label = tk.Label(self.frame, text='Confirm Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        ru_confirmed_label.place(x=590, y=370)
        ru_confirmed_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        ru_confirmed_entry_frame.place(x=595, y=400)
        ru_confirmed_entry = tk.Entry(ru_confirmed_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        ru_confirmed_entry.place(x=10, y=12)
        ru_confirmed_entry.insert(0, 'Re-enter Your Password')
        ru_confirmed_eye_closed_button = ttk.Button(ru_confirmed_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        ru_confirmed_eye_closed_button.place(x=270, y=2)
        ru_confirmed_eye_opened_button = ttk.Button(ru_confirmed_entry_frame, style='eye_opened_green.TButton', cursor='hand2')

        ru_back_button = ttk.Button(self.frame, text='Back', style='small_green.TButton', cursor='hand2', width=15, padding=8,
                                    command=lambda: self.show_register_as())
        ru_back_button.place(x=40, y=530)
        ru_register_button = ttk.Button(self.frame, text='Register', style='small_green.TButton', cursor='hand2', width=15, padding=8)
        ru_register_button.place(x=850, y=530)

    def show_registering_clinic(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        rc_text1 = tk.Label(self.frame, text='Register Clinic Account', font=('Open Sans', 30, 'bold'), bg='white', fg='#333333')
        rc_text1.place(x=30, y=20)

        rc_name_label = tk.Label(self.frame, text='Clinic Name', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_name_label.place(x=120, y=100)
        rc_name_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                       highlightthickness=0.5)
        rc_name_entry_frame.place(x=125, y=130)
        rc_name_entry = tk.Entry(rc_name_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_name_entry.place(x=10, y=12)
        rc_name_entry.insert(0, 'Enter Clinic Name')

        rc_operation_label = tk.Label(self.frame, text='Operation Hours', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_operation_label.place(x=120, y=190)
        rc_operation_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        rc_operation_entry_frame.place(x=125, y=220)
        rc_operation_entry = tk.Entry(rc_operation_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0,
                                      width=35)
        rc_operation_entry.place(x=10, y=12)
        rc_operation_entry.insert(0, 'Enter Operation Hours')

        rc_address_label = tk.Label(self.frame, text='Address', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_address_label.place(x=120, y=280)
        rc_address_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        rc_address_entry_frame.place(x=125, y=310)
        rc_address_entry = tk.Entry(rc_address_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_address_entry.place(x=10, y=12)
        rc_address_entry.insert(0, 'Enter Clinic Address')

        rc_describe_label = tk.Label(self.frame, text='Short Description', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_describe_label.place(x=120, y=370)
        rc_describe_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        rc_describe_entry_frame.place(x=125, y=400)
        rc_describe_entry = tk.Entry(rc_describe_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_describe_entry.place(x=10, y=12)
        rc_describe_entry.insert(0, 'Enter Short Description')

        rc_contact_label = tk.Label(self.frame, text='Contact Number', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_contact_label.place(x=590, y=100)
        rc_contact_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                          highlightthickness=0.5)
        rc_contact_entry_frame.place(x=595, y=130)
        rc_contact_entry = tk.Entry(rc_contact_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_contact_entry.place(x=10, y=12)
        rc_contact_entry.insert(0, 'Enter Contact Number')

        rc_image_label = tk.Label(self.frame, text='Image', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_image_label.place(x=590, y=190)
        rc_image_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        rc_image_entry_frame.place(x=595, y=220)
        rc_image_entry = tk.Label(rc_image_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585')
        rc_image_entry.place(x=8, y=10)
        rc_image_entry.config(text='Upload Clinic Image')
        ru_image_button = ttk.Button(rc_image_entry_frame, text='⇫', style='selection.TButton', width=4)
        ru_image_button.place(x=265, y=4)

        rc_email_label = tk.Label(self.frame, text='Email', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_email_label.place(x=590, y=280)
        rc_email_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                        highlightthickness=0.5)
        rc_email_entry_frame.place(x=595, y=310)
        rc_email_entry = tk.Entry(rc_email_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_email_entry.place(x=10, y=12)
        rc_email_entry.insert(0, 'Enter Your Email')

        rc_password_label = tk.Label(self.frame, text='Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_password_label.place(x=590, y=370)
        rc_password_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                           highlightthickness=0.5)
        rc_password_entry_frame.place(x=595, y=400)
        rc_password_entry = tk.Entry(rc_password_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_password_entry.place(x=10, y=12)
        rc_password_entry.insert(0, 'Enter Your Password')
        rc_password_eye_closed_button = ttk.Button(rc_password_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        rc_password_eye_closed_button.place(x=270, y=2)
        rc_password_eye_opened_button = ttk.Button(rc_password_entry_frame, style='eye_opened_green.TButton', cursor='hand2')

        rc_confirmed_label = tk.Label(self.frame, text='Confirm Password', font=('Open Sans', 12, 'bold'), bg='white', fg='#000000')
        rc_confirmed_label.place(x=590, y=460)
        rc_confirmed_entry_frame = tk.Frame(self.frame, bg='#D0F9EF', width=320, height=45, highlightbackground="#C8C7C7",
                                            highlightthickness=0.5)
        rc_confirmed_entry_frame.place(x=595, y=490)
        rc_confirmed_entry = tk.Entry(rc_confirmed_entry_frame, font=('Open Sans', 10), bg='#D0F9EF', fg='#858585', border=0, width=35)
        rc_confirmed_entry.place(x=10, y=12)
        rc_confirmed_entry.insert(0, 'Re-enter Your Password')
        rc_confirmed_eye_closed_button = ttk.Button(rc_confirmed_entry_frame, style='eye_closed_green.TButton', cursor='hand2')
        rc_confirmed_eye_closed_button.place(x=270, y=2)
        rc_confirmed_eye_opened_button = ttk.Button(rc_confirmed_entry_frame, style='eye_opened_green.TButton', cursor='hand2')

        rc_back_button = ttk.Button(self.frame, text='Back', style='small_green.TButton', cursor='hand2', width=15, padding=8,
                                    command=lambda: self.show_register_as())
        rc_back_button.place(x=40, y=530)
        rc_register_button = ttk.Button(self.frame, text='Register', style='small_green.TButton', cursor='hand2', width=15, padding=8)
        rc_register_button.place(x=850, y=530)

    def display_menu(self, frame, x, y, menu):
        root_x = frame.winfo_rootx()
        root_y = frame.winfo_rooty()
        adjusted_x = root_x + x
        adjusted_y = root_y + y

        menu.post(adjusted_x, adjusted_y)


window = tk.Tk()
window.title('Call a Doctor')
window.geometry('1050x600')
icon = load_image('icon', 48, 48)
window.iconphoto(False, icon)

root = LoginRegister(window)
root.show_get_started()
root.show_frame()

window.mainloop()

cursor.close()
database.close()
