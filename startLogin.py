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
from main import leftTopFrame, standardFont, standardYPadding

connection = sqlite3.connect("505_ACU_Q-Store_Database.db")

class LoginWindow:
    def __init__(self, root, frame, font, width, height, y_padding):
        self.root = root
        self.frame = frame
        self.font = font
        self.width = width
        self.height = height
        self.y_padding = y_padding

    def create(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        password_label = ctk.CTkLabel(self.frame, text="Please Enter Your \n Username And Password", font=self.font)
        password_label.pack(pady=self.y_padding)

        username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Username", font=self.font, width=self.width, height=self.height)
        username_entry.pack(pady=self.y_padding)

        password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Password", font=self.font, width=self.width, height=self.height, show='*')
        password_entry.pack(pady=self.y_padding)

        login_button = ctk.CTkButton(self.frame, text="Log In", font=self.font, width=self.width, height=self.height, command=lambda: Authentication.login(username_entry, password_entry))
        login_button.pack(pady=self.y_padding)

        forgot_password_button = ctk.CTkButton(self.frame, text="Forgot the Password", font=self.font, width=self.width, height=self.height, command=ForgotPassword(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create)
        forgot_password_button.pack(pady=self.y_padding)

        close_button = ctk.CTkButton(self.frame, text="Close Window", font=self.font, width=self.width, height=self.height, command=self.root.destroy)
        close_button.pack(pady=self.y_padding)

class Authentication:
    @staticmethod
    def login(username_entry, password_entry):
        usernames = [row[0] for row in connection.cursor().execute("SELECT Username FROM Accounts").fetchall()]
        user_username = username_entry.get()

        if user_username not in usernames:
            for widget in leftTopFrame.winfo_children():
                widget.destroy()
            idk = ctk.CTkLabel(leftTopFrame, text="idk", font = standardFont)
            idk.pack(pady = standardYPadding)
        else:
            user_password = connection.cursor().execute(f"SELECT Password FROM Accounts WHERE Username= '{user_username}'").fetchone()[0]
            user_entered_password = password_entry.get()

            if user_entered_password != user_password:
                Authentication.log_action(user_username, 3, user_entered_password)
                for widget in leftTopFrame.winfo_children():
                    widget.destroy()
                idk = ctk.CTkLabel(leftTopFrame, text="idk", font = standardFont)
                idk.pack(pady = standardYPadding)
            else:
                account_id = connection.cursor().execute(f"SELECT AccountID FROM Accounts WHERE Username= '{user_username}'").fetchone()[0]
                Authentication.log_action(account_id, 1)
                print("got to end")

    @staticmethod
    def log_action(account_id, action_id, user_input=None):
        date = datetime.datetime.now().strftime("%d/%m/%Y")
        time = datetime.datetime.now().strftime("%H:%M:%S")
        before = after = remarks = "N/A"

        connection.cursor().execute(f"INSERT INTO ActionsLogs (AccountID, Date, Time, ActionID, Before, After, User_Input, Remarks) VALUES ('{account_id}', '{date}', '{time}', '{action_id}', '{before}', '{after}', '{user_input}', '{remarks}')")
        connection.commit()

class ForgotPassword:
    def __init__(self, root, frame, font, width, height, y_padding):
        self.root = root
        self.frame = frame
        self.font = font
        self.width = width
        self.height = height
        self.y_padding = y_padding

    def create(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Username", font=self.font, width=self.width, height=self.height)
        username_entry.pack(pady=self.y_padding)

        next_button = ctk.CTkButton(self.frame, text="Next", font=self.font, width=self.width, height=self.height, command=lambda: self.get_password(username_entry))
        next_button.pack(pady=self.y_padding)

        return_button = ctk.CTkButton(self.frame, text="Return to Log In Page", font=self.font, width=self.width, height=self.height, command=lambda: LoginWindow(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create())
        return_button.pack(pady=self.y_padding)

    def get_password(self, username_entry):
        usernames = [row[0] for row in connection.cursor().execute("SELECT Username FROM Accounts").fetchall()]
        user_username = username_entry.get()

        if user_username not in usernames:
            for widget in leftTopFrame.winfo_children():
                widget.destroy()
            idk = ctk.CTkLabel(leftTopFrame, text="idk", font = standardFont)
            idk.pack(pady = standardYPadding)
            account_data = connection.cursor().execute(f"SELECT Secret_Question, Secret_Question_Answer, Password FROM Accounts WHERE Username = '{user_username}'").fetchone()
            PasswordRetrievalWindow(self.root, self.frame, self.font, self.width, self.height, self.y_padding, account_data, user_username).create()

class PasswordRetrievalWindow:
    def __init__(self, root, frame, font, width, height, y_padding, account_data, username):
        self.root = root
        self.frame = frame
        self.font = font
        self.width = width
        self.height = height
        self.y_padding = y_padding
        self.account_data = account_data
        self.username = username

    def create(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        question_label = ctk.CTkLabel(self.frame, text=f"The secret question is: \n{self.account_data[0]}", fg_color="transparent", font=self.font)
        question_label.pack(pady=self.y_padding)

        answer_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter the Answer to the Question", font=self.font, width=self.width, height=self.height)
        answer_entry.pack(pady=self.y_padding)

        submit_button = ctk.CTkButton(self.frame, text="Submit Answer", font=self.font, width=self.width, height=self.height, command=lambda: self.check_answer(answer_entry))
        submit_button.pack(pady=self.y_padding)

        return_button = ctk.CTkButton(self.frame, text="Return to Log In Page", font=self.font, width=self.width, height=self.height, command=lambda: LoginWindow(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create())
        return_button.pack(pady=self.y_padding)


LoginWindow.create()