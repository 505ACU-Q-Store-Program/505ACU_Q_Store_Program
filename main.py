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

connection = sqlite3.connect("505_ACU_Q-Store_Database.db")

path= os.getcwd()

# Defining variables to make it easier to change the size of everything
standardHeight = 30
standardWidth = 250
standardFont = "", 18
standardYPadding = 5
standardXPadding = 5

# Defining colour mode for the program (light or dark)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
#root.resizable(False, False)
#root.attributes("-fullscreen", True)
#root.protocol("WM_DELETE_WINDOW", disable_event)
root.title("505ACU Albany Q-Store Software Version: 0.9")
#screenWidth = root.winfo_screenwidth()
#screenHeight = root.winfo_screenheight()
#root.geometry(f"{screenWidth}x{screenHeight}")
#root.state('zoomed')

# Creating the main frame
mainFrame = ctk.CTkFrame(root)
mainFrame.pack(fill="both", expand=True)

# Setting row and column weights for main frame
mainFrame.rowconfigure(0, weight=1)
mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.columnconfigure(2, weight=5)

# Creating the left frame
leftFrame = ctk.CTkFrame(mainFrame, fg_color="#1f1f1f")
leftFrame.grid(row=0, column=0, sticky="nsew", padx=standardXPadding)
leftFrame.grid_propagate(False)
leftFrame.pack_propagate(False)

# Creating the middle frame
middleFrame = ctk.CTkFrame(mainFrame, fg_color="#292929")
middleFrame.grid(row=0, column=1, sticky="nsew", pady=standardYPadding, padx=standardXPadding)
middleFrame.grid_propagate(False)
middleFrame.pack_propagate(False)

# Creating the right frame
rightFrame = ctk.CTkFrame(mainFrame, fg_color="#292929")
rightFrame.grid(row=0, column=2, sticky="nsew", pady=standardYPadding, padx=standardXPadding)
rightFrame.grid_propagate(False)
rightFrame.pack_propagate(False)

# Creating the left frame
leftFrame.columnconfigure(0, weight=3)
leftFrame.columnconfigure(2, weight=0)
leftFrame.rowconfigure(0, weight=1)
leftFrame.rowconfigure(1, weight=5)

# Creating the left top frame
leftTopFrame = ctk.CTkFrame(leftFrame, fg_color="#292929")
leftTopFrame.grid(row=0, column=0, sticky="nsew", pady=standardYPadding)
leftTopFrame.grid_propagate(False)
leftTopFrame.pack_propagate(False)

# Creating the left bottom frame
leftBottomFrame = ctk.CTkFrame(leftFrame, fg_color="#292929")
leftBottomFrame.grid(row=1, column=0, sticky="nsew", pady=standardYPadding)
leftBottomFrame.grid_propagate(False)
leftBottomFrame.pack_propagate(False)

def Date():
    date = datetime.datetime.now().strftime("%d/%m/%Y")
    return date

def Time():
    time = datetime.datetime.now().strftime("%H:%M:%S")
    return time

class ErrorWindow:
    def __init__(self, parent, message, on_close):
        self.parent = parent
        self.message = message
        self.on_close = on_close

    def create(self):
        error_window = ctk.CTkToplevel(self.parent)
        error_window.title("Error")

        error_label = ctk.CTkLabel(error_window, text=self.message, font=standardFont)
        error_label.pack(pady=standardYPadding)

        close_button = ctk.CTkButton(error_window, text="Close", command=lambda: [error_window.destroy(), self.on_close()])
        close_button.pack(pady=standardYPadding)

class ActionLogs:
    def __init__(self, loggedInAccountID, actionID, before, after, userInput, remarks):
        self.accountID = loggedInAccountID
        self.date = Date()
        self.time = Time()
        self.actionID = actionID
        self.before = before
        self.after = after
        self.userInput = userInput
        self.remarks = remarks
        
    def createLog(self):
        connection.cursor().execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{self.accountID}','{self.date}','{self.time}','{self.actionID}','{self.before}','{self.after}','{self.userInput}','{self.remarks}')").fetchall()
        connection.commit()

class LoginWindow:
    def __init__(self, root, frame, font, width, height, y_padding):
        self.root = root
        self.frame = frame
        self.font = font
        self.width = width
        self.height = height
        self.y_padding = y_padding

    def create(self):
        for widgets in self.frame.winfo_children():
            widgets.destroy()

        password_label = ctk.CTkLabel(self.frame,text="Please Enter Your \n Username And Password", font=self.font)
        password_label.pack(pady=self.y_padding)

        username_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Username", font=self.font, width=self.width, height=self.height)
        username_entry.pack(pady=self.y_padding)

        password_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Password", font=self.font, width=self.width, height=self.height, show='*')
        password_entry.pack(pady=self.y_padding)

        login_button = ctk.CTkButton(self.frame, text="Log In", font=self.font, width=self.width, height=self.height, command=lambda: Authentication.login(username_entry, password_entry))
        login_button.pack(pady=self.y_padding)

        forgot_password_button = ctk.CTkButton(self.frame, text="Forgot the Password", font=self.font, width=self.width, height=self.height, command=lambda: ForgotPassword(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create())
        forgot_password_button.pack(pady=self.y_padding)

        close_button = ctk.CTkButton(self.frame, text="Close Window", font=self.font, width=self.width, height=self.height, command=self.root.destroy)
        close_button.pack(pady=self.y_padding)

class Authentication:
    def login(username_entry, password_entry):
        usernames = str(connection.cursor().execute("SELECT Username FROM Accounts").fetchall()).replace("(","").replace(")","").replace("'","").replace(",","").replace(" ",",")
        user_username = username_entry.get()
        if user_username not in usernames:
            for widgets in leftTopFrame.winfo_children():
                widgets.destroy()
            idk = ctk.CTkLabel(leftTopFrame, text="Incorrect Username. \n Return to log in page and try again.", font = standardFont)
            idk.pack(pady = standardYPadding)

            passwordErrorButton = ctk.CTkButton(
            leftTopFrame,
            text="Return to Log In Page",
            font=standardFont,
            width=standardWidth,
            height=standardHeight,
            command=lambda: logInWindow1.create()
            )
            passwordErrorButton.pack(pady=standardYPadding)

        else:
            user_password = connection.cursor().execute(f"SELECT Password FROM Accounts WHERE Username= '{user_username}'").fetchone()[0]
            user_entered_password = password_entry.get()
            global loggedInAccountID
            loggedInAccountID = connection.cursor().execute(f"SELECT AccountID FROM Accounts WHERE Username= '{user_username}'").fetchone()[0]

            if user_entered_password != user_password:
                actionLog3 = ActionLogs(loggedInAccountID, 3, "N/A", "N/A", user_entered_password, "N/A")
                actionLog3.createLog()

                for widgets in leftTopFrame.winfo_children():
                    widgets.destroy()

                passwordErrorLabel = ctk.CTkLabel(
                leftTopFrame,
                text="Incorrect Password. Return to log in page and try again.",
                font=standardFont
                )
                passwordErrorLabel.pack(pady=standardYPadding)

                # Creates a ctk button
                passwordErrorButton = ctk.CTkButton(
                    leftTopFrame,
                    text="Return to Log In Page",
                    font=standardFont,
                    width=standardWidth,
                    height=standardHeight,
                    command=lambda: logInWindow1.create()
                )
                passwordErrorButton.pack(pady=standardYPadding)

            else:
                
                actionLog1 = ActionLogs(loggedInAccountID, 1, "N/A", "N/A", "N/A", "N/A")
                actionLog1.createLog()
                print("got to end")

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
        usernames = connection.cursor().execute("SELECT Username FROM Accounts").fetchall()
        user_username = username_entry.get()

        if user_username not in usernames:
            for widgets in leftTopFrame.winfo_children():
                widgets.destroy()
            idk = ctk.CTkLabel(leftTopFrame, text="idk", font = standardFont)
            idk.pack(pady = standardYPadding)
        else:
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

        answer_entry = ctk.CTkEntry(self.frame, placeholder_text="Enter Answer Here", font=self.font, width=self.width, height=self.height)
        answer_entry.pack(pady=self.y_padding)

        submit_button = ctk.CTkButton(self.frame, text="Submit Answer", font=self.font, width=self.width, height=self.height, command=lambda: self.check_answer(answer_entry))
        submit_button.pack(pady=self.y_padding)

        return_button = ctk.CTkButton(self.frame, text="Return to Log In Page", font=self.font, width=self.width, height=self.height, command=lambda: LoginWindow(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create())
        return_button.pack(pady=self.y_padding)

    def check_answer(self, answer_entry):
        answer = answer_entry.get()
        correct_answer = self.account_data[1]

        if answer != correct_answer:
            Authentication.log_action(self.get_account_id(), 9, answer)
            ErrorWindow(answer_entry.master, "Your answer does not match the correct answer", lambda: ForgotPassword(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create())
        else:
            password = self.account_data[2]
            PasswordDisplayWindow(self.root, self.frame, self.font, self.width, self.height, self.y_padding, password, self.username).create()
            Authentication.log_action(self.get_account_id(), 4)

    def get_account_id(self):
        return connection.cursor().execute(f"SELECT AccountID FROM Accounts WHERE Username= '{self.username}'").fetchone()[0]

class PasswordDisplayWindow:
    def __init__(self, root, frame, font, width, height, y_padding, password, username):
        self.root = root
        self.frame = frame
        self.font = font
        self.width = width
        self.height = height
        self.y_padding = y_padding
        self.password = password
        self.username = username

    def create(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        password_label = ctk.CTkLabel(self.frame, text=f"The Password is: \n{self.password}", fg_color="transparent", font=self.font)
        password_label.pack(pady=self.y_padding)

        return_button = ctk.CTkButton(self.frame, text="Return to Log In Page", font=self.font, width=self.width, height=self.height, command=lambda: LoginWindow(self.root, self.frame, self.font, self.width, self.height, self.y_padding).create())
        return_button.pack(pady=self.y_padding)


logInWindow1 = LoginWindow(root, leftTopFrame, standardFont, standardWidth, standardHeight, standardYPadding)
logInWindow1.create()

root.mainloop()