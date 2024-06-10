from tkinter import *
from tkinter import ttk
import datetime
import re
import sqlite3
from contextlib import closing
import customtkinter as ctk
from tkcalendar import DateEntry
import os
import csv
from functools import partial

connection = sqlite3.connect("505_ACU_Q-Store_Database.db")

path= os.getcwd()

# Defining variables to make it easier to change the size of everything
standard_height = 30
standard_width = 250
standard_font = "", 18
standard_y_padding = 5
standard_x_padding = 5

# Defining colour mode for the program (light or dark)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("505ACU Albany Q-Store Software Version: 0.9")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"500x275")
root.resizable(False, False)

def log_in_window():

    for widget in root.winfo_children():
        widget.destroy()
    
    password_label = ctk.CTkLabel(
        root,
        text="Please Enter Your \n Username And Password",
        font=standard_font)
    password_label.pack(pady=standard_y_padding)

    username_entry = ctk.CTkEntry(
        root,
        placeholder_text="Enter Username",
        font=standard_font,
        width=standard_width,
        height=standard_height)
    username_entry.pack(pady=standard_y_padding)

    password_entry = ctk.CTkEntry(
        root,
        placeholder_text="Enter Password",
        font=standard_font,
        width=standard_width,
        height=standard_height,
        show='*')
    password_entry.pack(pady=standard_y_padding)

    button_type = ["login",username_entry,password_entry]

    login_button = ctk.CTkButton(
        root,
        text="Log In",
        font=standard_font,
        width=standard_width,
        height=standard_height,
        command=lambda: main(button_type))
    login_button.pack(pady=standard_y_padding)

    forgot_password_button = ctk.CTkButton(
        root,
        text="Forgot the Password",
        font=standard_font,
        width=standard_width,
        height=standard_height,
        command=lambda: main(button_type))
    forgot_password_button.pack(pady=standard_y_padding)

    close_button = ctk.CTkButton(
        root,
        text="Close Window",
        font=standard_font,
        width=standard_width,
        height=standard_height,
        command=root.destroy)
    close_button.pack(pady=standard_y_padding)

class ErrorWindow:
    def __init__(self,parent,message,on_close):
        self.parent = parent
        self.message = message
        self.on_close = on_close

    def create(self):
        error_window = ctk.CTkToplevel(self.parent)
        error_window.title("Error")
        error_window.resizable(False, False)

        error_label = ctk.CTkLabel(
            error_window,
            text=self.message,
            font=standard_font)
        error_label.pack(pady=standard_y_padding)

        close_button = ctk.CTkButton(
            error_window,
            text="Close",
            font=standard_font,
            width=standard_width,
            height=standard_height,
            command=lambda: [error_window.destroy(),self.on_close()])
        close_button.pack(pady=standard_y_padding)

class LogIn:
    def __init__(self, username_entry, password_entry):
        self.username_entry = username_entry
        self.password_entry = password_entry

    def username_checker(self):
        usernames = str(connection.cursor().execute("SELECT Username FROM Accounts").fetchall()).replace("(","").replace(")","").replace("'","").replace(",","").replace(" ",",")
        username = self.username_entry.get()
        if username not in usernames:
            username_in_usernames = False
            return username_in_usernames
        else:
            username_in_usernames = True
            return username_in_usernames
        
    def password_checker(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        database_password = connection.cursor().execute(f"SELECT Password FROM Accounts WHERE Username= '{username}'").fetchone()[0]
        if password != database_password:
            correct_password = False
            return correct_password
        else:
            correct_password = True
            return correct_password




def main(button_type): 
    if button_type == None:
        log_in_window()
    else:    
        button_value = button_type[0]
        username_entry = button_type[1]
        password_entry = button_type[2]

        log_in_1 = LogIn(username_entry, password_entry)
        log_in_2 = LogIn(username_entry, password_entry)
        error_window_1 = ErrorWindow(root, "Your password or username was incorect.\nPlease go back and try again.", lambda: log_in_window())
        error_window_2 = ErrorWindow(root, "We encountered a problem, please try again.", lambda: log_in_window())

        if button_value == "login":
            if log_in_1.username_checker() == True:
                if log_in_2.password_checker() == True:
                    print("yay1")
                else:
                    error_window_1.create()
            else:
                error_window_1.create()

        elif button_value == "forgot_password":
            pass
        else:
            error_window_2.create()









if __name__ == "__main__":
    main(button_type = None)

root.mainloop()