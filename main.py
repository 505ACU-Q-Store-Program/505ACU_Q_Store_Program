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


import startLogin


root.mainloop()