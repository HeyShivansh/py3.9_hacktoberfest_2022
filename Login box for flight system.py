import mysql.connector as ms
from tkinter import *

DB = ms.connect(host='localhost', user='root', password='admin')
cursor = DB.cursor()

# Creating Database
cursor.execute("create database if not exists bookings")
cursor.execute("use bookings")

# Creating Table in Database
sql_command_1 = '''
               create table if not exists users(
               email char(64),
               username varchar(64),
               password varchar(30)
               )
               '''     
cursor.execute(sql_command_1)

# Creating GUI window 
window = Tk()
window.geometry('500x300+500+250')
window.title("SignUp Box")

# variable declaration to store values from tkinter input/entry
username = StringVar()
email_ = StringVar()
password_ = StringVar()
confirm_password = StringVar()

def enter_into_db(email, name, password):
    sql_command = f"insert into users values ('{email}', '{name}', '{password}');"
    cursor.execute(sql_command)
    DB.commit()

def check_entries(*entries):
    for entry in entries:
        if len(entry) == 0:
            return True

def print_values():
    email = email_.get()
    name = username.get()
    password = password_.get()
    c_pass = confirm_password.get()

    if check_entries(email, name, password, c_pass):
        print("Invalid Credentials")
    else:
        enter_into_db(email, name, password)

def signUp_window():
    
    window.geometry('500x300')

    def login_window():

        # Resizing the window
        window.geometry('500x225')
        
        # Destroying email row
        email.destroy()
        email_entry.destroy()
        
        # Destroying confirm password row
        c_pass.destroy()
        c_pass_entry.destroy()
        
        # Destroying signUp button
        sign.destroy()

        # Destroying login button
        if_login.destroy()

        # Button
        login = Button(window, text='Log In', font=('',15))
        login.grid(row=4, column=0, padx=15, pady=10, columnspan=2)

        # Ask if already have account
        ask_text['text'] = "Don't have an account?"
        
        if_sign = Button(window, text="SignUp", font=('',10), width=8, command=signUp_window)
        if_sign.grid(row=5, column=1, padx=15, pady=10)
    
    # Email text and entry
    email = Label(window, text='Email', font=('',15))
    email.grid(row=0, column=0, padx=15, pady=10)

    email_entry = Entry(window, font=('',15),textvariable=email_, width=25)
    email_entry.grid(row=0, column=1, padx=15, pady=10)

    # Username text and Entry
    user = Label(window, text='Username', font=('',15))
    user.grid(row=1, column=0, padx=15, pady=10)

    user_entry = Entry(window, font=('',15),textvariable=username, width=25)
    user_entry.grid(row=1, column=1, padx=15, pady=10)

    # password text and entry
    password = Label(window, text='Password', font=('',15))
    password.grid(row=2, column=0, padx=15, pady=10)

    pass_entry = Entry(window, font=('',15),textvariable=password_ , width=25)
    pass_entry.grid(row=2, column=1, padx=15, pady=10)

    # Confirm password text and entry
    c_pass = Label(window, text='Password(again)', font=('',15))
    c_pass.grid(row=3, column=0, padx=15, pady=10)

    c_pass_entry = Entry(window, font=('',15),textvariable=confirm_password, width=25)
    c_pass_entry.grid(row=3, column=1, padx=15, pady=10)

    # Button
    sign = Button(window, text='SignUp', font=('',15), width=10, command=print_values)
    sign.grid(row=4, column=0, padx=15, pady=10, columnspan=2)

    # Ask if already have account
    ask_text = Label(window, text="Already have an account?", font=('',10))
    ask_text.grid(row=5, column=0, padx=15, pady=10)

    if_login = Button(window, text="LogIn", font=('',10), width=10, command=login_window)
    if_login.grid(row=5, column=1, padx=15, pady=10)



#__main__
signUp_window()

















    
