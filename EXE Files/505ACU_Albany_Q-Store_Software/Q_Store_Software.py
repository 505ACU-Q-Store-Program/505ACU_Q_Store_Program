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
import __main__

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

# Setting program main window
def disable_event():
    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "2"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

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
##################################################################################################################


def createLogInWindow():
    for widgets in leftTopFrame.winfo_children():
        widgets.destroy()

    # Creates a ctk label
    passwordLabel = ctk.CTkLabel(
        leftTopFrame,
        text="Please Enter Your \n Username And Password",
        font=standardFont
    )
    passwordLabel.pack(pady=standardYPadding)

    # Creates a ctk entry box
    usernameEntry = ctk.CTkEntry(
        leftTopFrame,
        placeholder_text="Enter Username",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
    )
    usernameEntry.pack(pady=standardYPadding)

    # Creates a ctk entry box
    passwordEntry = ctk.CTkEntry(
        leftTopFrame,
        placeholder_text="Enter Password",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
        show='*'
    )
    passwordEntry.pack(pady=standardYPadding)

    # Creates a ctk button
    logInButton = ctk.CTkButton(
        leftTopFrame,
        text="Log In",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
        command=lambda: startLogIn(usernameEntry,passwordEntry)
    )
    logInButton.pack(pady=standardYPadding)

    # Creates a ctk button
    forgotPasswordButton = ctk.CTkButton(
        leftTopFrame,
        text="Forgot the Password",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
        command=startForgotPassword
    )
    forgotPasswordButton.pack(pady=standardYPadding)

    # Creates a ctk button
    closeProgramButton = ctk.CTkButton(
        leftTopFrame,
        text="Close Window",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
        command=root.destroy
    )
    closeProgramButton.pack(pady=standardYPadding)


def startLogIn(usernameEntry,passwordEntry):
    usernames = []
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT Username FROM Accounts").fetchall()
    data = str(data).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace(" ", ',').replace("[", '').replace("]", '')
    data = data.split(',')
    for username in data:
        usernames.append(username)
    userUsernameEntry = usernameEntry.get()
    if userUsernameEntry not in usernames:

        for widgets in leftTopFrame.winfo_children():
            widgets.destroy()

        # Creates a ctk label
        passwordErrorLabel = ctk.CTkLabel(
            leftTopFrame,
            text="Incorrect Username. \n Return to log in page and try again.",
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
            command=createLogInWindow
        )
        passwordErrorButton.pack(pady=standardYPadding)

    elif userUsernameEntry in usernames:
        cursor = connection.cursor()
        userPassword = cursor.execute(f"SELECT Password FROM Accounts WHERE Username= '{userUsernameEntry}'").fetchall()
        userPassword = str(userPassword).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        userEnteredPassword = passwordEntry.get()
        if userEnteredPassword != userPassword:

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            Action= "3"
            Before= "N/A"
            After= "N/A"
            User_Input= userEnteredPassword
            Remarks= "N/A"
            cursor = connection.cursor()
            data = cursor.execute(f"SELECT AccountID FROM Accounts WHERE Username= '{userUsernameEntry}'").fetchall()
            AccountID=str(data).replace("[","").replace("]","").replace("(","").replace(")","").replace(",","")
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{AccountID}','{Date}','{Time}','{Action}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            for widgets in leftTopFrame.winfo_children():
                widgets.destroy()
            # Creates a ctk label
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
                command=createLogInWindow
            )
            passwordErrorButton.pack(pady=standardYPadding)

        elif userEnteredPassword == userPassword:
            cursor = connection.cursor()
            data = cursor.execute(f"SELECT AccountID FROM Accounts WHERE Username= '{userUsernameEntry}'").fetchall()
            accountID=str(data).replace("[","").replace("]","").replace("(","").replace(")","").replace(",","")
            global loggedInAccountID
            loggedInAccountID = accountID
            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            Action= "1"
            Before= "N/A"
            After= "N/A"
            User_Input= "N/A"
            Remarks= "N/A"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{Action}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()
            Program()


def startForgotPassword():
    for widgets in leftTopFrame.winfo_children():
        widgets.destroy()

    # Creates an entry box
    usernameEntry = ctk.CTkEntry(
        leftTopFrame,
        placeholder_text="Enter Username",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
    )
    usernameEntry.pack(pady=standardYPadding)

    # Creates a button
    usernameCheckerButton = ctk.CTkButton(
        leftTopFrame,
        text="Next",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
        command=lambda: startGetPassword(usernameEntry)
    )
    usernameCheckerButton.pack(pady=standardYPadding)

    # Creates a button
    returnToLogInButton = ctk.CTkButton(
        leftTopFrame,
        text="Return to Log In Page",
        font=standardFont,
        width=standardWidth,
        height=standardHeight,
        command=createLogInWindow,
    )
    returnToLogInButton.pack(pady=standardYPadding)


def startGetPassword(usernameEntry):
    usernames = []
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT Username FROM Accounts").fetchall()
    data = str(data).replace('(', '').replace(')', '').replace(',', '').replace("'", '').replace(" ", ',').replace(
        "[", '').replace("]", '')
    data = data.split(',')
    for username in data:
        usernames.append(username)
    userUsernameEntry = usernameEntry.get()
    if userUsernameEntry not in usernames:

        for widgets in leftTopFrame.winfo_children():
            widgets.destroy()

        # Creates a ctk label
        passwordErrorLabel = ctk.CTkLabel(
            leftTopFrame,
            text="Incorrect Username. Return to log in page and try again.",
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
            command=createLogInWindow
        )
        passwordErrorButton.pack(pady=standardYPadding)

    elif userUsernameEntry in usernames:

        cursor = connection.cursor()
        data = cursor.execute(
            f"SELECT Secret_Question,Secret_Question_Answer,Password FROM Accounts WHERE Username = '{userUsernameEntry}'").fetchall()
        formatted_data = []
        for item in data:
            accountSecretQuestion = item[0]
            accountSecretQuestionAnswer = item[1]
            accountPassword = item[2]
            formatted_data.append(
                f"{accountSecretQuestion}, {accountSecretQuestionAnswer}, {accountPassword}")

        for widgets in leftTopFrame.winfo_children():
            widgets.destroy()

        # Creates a ctk label
        label = ctk.CTkLabel(leftTopFrame, text=f"The secret question is: \n{accountSecretQuestion}", fg_color="transparent",font=standardFont)
        label.pack(pady=standardYPadding)

        # Creates an entry box
        accountQuestionAnswer = ctk.CTkEntry(
            leftTopFrame,
            placeholder_text="Enter the Answer to the Question",
            font=standardFont,
            width=400,
            height=standardHeight,
        )
        accountQuestionAnswer.pack(pady=standardYPadding)

        # Creates a button
        questionCheckerButton = ctk.CTkButton(
            leftTopFrame,
            text="Submit Answer",
            font=standardFont,
            width=400,
            height=standardHeight,
            command=lambda: startLogInQuestionChecker(accountQuestionAnswer, accountSecretQuestionAnswer, accountPassword, userUsernameEntry)
        )
        questionCheckerButton.pack(pady=standardYPadding)

        # Creates a button
        questionCheckerButton = ctk.CTkButton(
            leftTopFrame,
            text="Return to Log In Page",
            font=standardFont,
            width=400,
            height=standardHeight,
            command=createLogInWindow,
        )
        questionCheckerButton.pack(pady=standardYPadding)

        return accountQuestionAnswer, accountSecretQuestionAnswer, accountPassword


def startLogInQuestionChecker(accountQuestionAnswer, accountSecretQuestionAnswer, accountPassword, userUsernameEntry):
    questionAnswer = accountQuestionAnswer.get()

    if questionAnswer != accountSecretQuestionAnswer:
        for widgets in leftTopFrame.winfo_children():
            widgets.destroy()

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        Action= "9"
        Before= "N/A"
        After= "N/A"
        User_Input= questionAnswer
        Remarks= "N/A"
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT AccountID FROM Accounts WHERE Username= '{userUsernameEntry}'").fetchall()
        AccountID=str(data).replace("[","").replace("]","").replace("(","").replace(")","").replace(",","")
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{AccountID}','{Date}','{Time}','{Action}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()

        # Creates a label
        errorLabel = ctk.CTkLabel(
            leftTopFrame,
            text="Your answer does not match the correct answer",
            font=standardFont
        )
        errorLabel.pack(pady=standardYPadding)

        # Creates a button
        errorButton = ctk.CTkButton(
            leftTopFrame,
            text="Return to Previous Page",
            font=standardFont,
            width=standardWidth,
            height=standardHeight,
            command=startForgotPassword
        )
        errorButton.pack(pady=standardYPadding)

    else:
        for widgets in leftTopFrame.winfo_children():
            widgets.destroy()

        # Creates a ctk label
        label = ctk.CTkLabel(leftTopFrame, text=f"The Password is: \n{accountPassword}", fg_color="transparent", font=standardFont)
        label.pack(pady=standardYPadding)

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        Action= "4"
        Before= "N/A"
        After= "N/A"
        User_Input= "N/A"
        Remarks= "N/A"
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT AccountID FROM Accounts WHERE Username= '{userUsernameEntry}'").fetchall()
        AccountID=str(data).replace("[","").replace("]","").replace("(","").replace(")","").replace(",","")
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{AccountID}','{Date}','{Time}','{Action}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()
        

        # Creates a button
        returnToLoginButton = ctk.CTkButton(
            leftTopFrame,
            text="Return to Log In Page",
            font=standardFont,
            width=standardWidth,
            height=standardHeight,
            command=createLogInWindow
        )
        returnToLoginButton.pack(pady=standardYPadding)


def Program():
    for widgets in leftTopFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    startLabel = ctk.CTkLabel(leftTopFrame, text="MADE BY CDTWO2 Alec McDonald \nFOR USE ONLY BY 505ACU Albany", font = standardFont)
    startLabel.pack(pady = standardYPadding)

    #Creates a button
    global AACMemberOptionsButton
    AACMemberOptionsButton = ctk.CTkButton(
        leftTopFrame,
        text= "AAC Member Options",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=AACMemberOptions,
        )
    AACMemberOptionsButton.pack(pady = standardYPadding)

    #Creates a button
    global listOfStoresButton
    listOfStoresButton = ctk.CTkButton(
        leftTopFrame,
        text= "List Of Stores",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command= listStores,
        )
    listOfStoresButton.pack(pady = standardYPadding)

    #Creates a button
    global orderingOptionsButton
    orderingOptionsButton = ctk.CTkButton(
        leftTopFrame,
        text= "Ordering Options",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command= orderingOptions,
        )
    orderingOptionsButton.pack(pady = standardYPadding)

    #Creates a button
    global storesReturnsButton
    storesReturnsButton = ctk.CTkButton(
        leftTopFrame,
        text= "Stores Returns",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command= storesReturns,
        )
    storesReturnsButton.pack(pady = standardYPadding)

    #Creates a button 
    global adminButton
    adminButton = ctk.CTkButton(
        leftTopFrame,
        text= "Admin Options",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command= adminOptions,
        )
    adminButton.pack(pady = standardYPadding)

    #Creates a button 
    global closeWindow
    closeWindow = ctk.CTkButton(
        leftTopFrame, 
        text="Close Window", 
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command= closeProgram
        )
    closeWindow.pack(pady = standardYPadding)


##################################################################################################################


def AACMemberOptions():

        #Clears widgits in left bottom frame, middle frame and right frame
        for widgets in leftBottomFrame.winfo_children():
            widgets.destroy()
        for widgets in middleFrame.winfo_children():
            widgets.destroy()
        for widgets in rightFrame.winfo_children():
            widgets.destroy()

        #Creates a button
        addPersonOptionsButton = ctk.CTkButton(
            middleFrame,
            text= "Add An AAC Member",
            font= (standardFont),
            width= standardWidth,
            height= standardHeight,
            command= addAACMemberOptions,
            )
        addPersonOptionsButton.pack(pady = standardYPadding)

        #Creates a button
        changeRankButton = ctk.CTkButton(
            middleFrame,
            text= "Change An AAC\nMembers Rank",
            font= (standardFont),
            width= standardWidth,
            height= standardHeight,
            command= changeRankOptions,
            )
        changeRankButton.pack(pady = standardYPadding)

        #Creates a button
        listPeopleButton = ctk.CTkButton(
            middleFrame,
            text= "List Of AAC Members",
            font= (standardFont),
            width= standardWidth,
            height= standardHeight,
            command= listOfAACMembers,
            )
        listPeopleButton.pack(pady = standardYPadding)

#-----------------------------------------------------------------------------------------------------------------

def addAACMemberOptions():

    #Deletes all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creates list box and puts names into listbox using SQL
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 30, height= 23, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(row))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creates scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)        

    #User entry
    rankEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Abreviated Rank",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    rankEntry.pack(pady = standardYPadding)

    #User entry
    first_inital = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter First Name",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    first_inital.pack(pady = standardYPadding)

    #User Entry
    nameEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Last Name",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    nameEntry.pack(pady = standardYPadding)

    #Button to call 'addPerson' function
    addPersonButton = ctk.CTkButton(
        rightFrame,
        text= "Add An AAC Member\nTo The List",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command= lambda: addPerson(rankEntry,first_inital,nameEntry),
        )
    addPersonButton.pack(pady = standardYPadding)


def addPerson(rankEntry,first_inital,nameEntry):
    #Getting the entry from the entry boxes and turning them into string
    rank = str(rankEntry.get())
    first = str(first_inital.get())
    last_name = str(nameEntry.get())
    email = first+'.'+last_name+'@armycadets.gov.au'

    #Checks if the contain letters or numbers
    hasLettersRank = bool(re.search(r'[a-zA-Z]', rank))
    hasNumbersRank = bool(re.search(r'\d', rank))
    hasLettersFirst = bool(re.search(r'[a-zA-Z]', first))
    hasNumbersFirst = bool(re.search(r'\d', first))
    hasLetterslast_name = bool(re.search(r'[a-zA-Z]', last_name))
    hasNumberslast_name = bool(re.search(r'\d', last_name))

    #Checks if has no letters
    if not hasLettersRank:
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "Invalid Characters Entered For Abreviated Rank",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates button to close window
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

        #Runs function
        addAACMemberOptions()
    
    #Checking if has letters and numbers or just numbers
    elif hasLettersRank and hasNumbersRank or hasLettersRank:
        
        #Checks if only numbers
        if hasNumbersFirst:
            #Creates error window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "Invalid Characters Entered For First Name",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates button to close window
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)

            #Runs function
            addAACMemberOptions()

        #Checks if only has leters        
        elif hasLettersFirst:

            #Checks if only numbers
            if hasNumberslast_name:
                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "Invalid Characters Entered For Last Name",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates button to close window
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)

                #Runs function
                addAACMemberOptions()


            #Checks if only has leters    
            elif hasLetterslast_name:

                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO Cadets (rank,first_name,last_name,email) VALUES ('{rank}', '{first}', '{last_name}', '{email}')")
                connection.commit()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "6"
                Before= "N/A"
                After= "N/A"
                User_Input= f"{rank} {first} {last_name}"
                Remarks= "N/A"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                #Runs function
                addAACMemberOptions()

            #Checks if contians stuff other than letters or numbers  
            else:
                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "Invalid Characters Entered For Last Name",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates button to close window
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)

                #Runs function
                addAACMemberOptions()


        #Checks if contians stuff other than letters or numbers    
        else:
            #Creates error window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "Invalid Characters Entered For First Initial",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates button to close window
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)

            #Runs function
            addAACMemberOptions()

    #Checks if contians stuff other than letters or numbers   
    else:
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "Invalid Characters Entered For Abreviated Rank",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates button to close window
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

        #Runs function
        addAACMemberOptions()


def changeRankOptions():

    #Clea all widgets on right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creating a label
    label = ctk.CTkLabel(rightFrame, text="Select The Person You Wish To Modify", fg_color="transparent", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creating list box frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creating list box and inserting contents of database into it using SQL
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 30, height= 25, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creating a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)        

    #Creating an entry box
    newRankEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Abreviated Rank",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    newRankEntry.pack(pady = standardYPadding)

    #Creating a button
    changeRankButton = ctk.CTkButton(
        rightFrame,
        text= "Update Rank",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command= lambda: rankSelectionChecker(namesListListbox,formatted_data,newRankEntry),
        )
    changeRankButton.pack(pady = standardYPadding)


def rankSelectionChecker(namesListListbox,formatted_data,newRankEntry):
    #Getting user listbox selection
    rankNameSelection= namesListListbox.curselection()
    #Looking if there was no selection
    if not rankNameSelection:
        #Creating an error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creating a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creating a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)
    #Looking if there was a selection
    else:
        #Gets user selection
        rowSelectionRank = namesListListbox.curselection()

        #Checks if user selected an option
        if rowSelectionRank:
            #Gets all required information and turns it into usable variables
            rowIndexRank = rowSelectionRank[0]
            rowRank = formatted_data[rowIndexRank]
            rowRankString= str(rowRank)
            cadetID = rowRankString.split()[0]
            cadeNewRank = newRankEntry.get()

            cursor = connection.cursor()
            oldRank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID={cadetID}").fetchall()
            oldRank = str(oldRank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            firstName = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID={cadetID}").fetchall()
            firstName = str(firstName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            lastName = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID={cadetID}").fetchall()
            lastName = str(lastName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            #Updates rank in database using SQL
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Cadets SET Rank='{cadeNewRank}' WHERE CadetID={cadetID}")
            connection.commit()

            cursor = connection.cursor()
            newRank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID={cadetID}").fetchall()
            newRank = str(newRank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "13"
            Before= f"{oldRank} {firstName} {lastName}"
            After= f"{newRank} {firstName} {lastName}"
            User_Input= cadeNewRank
            Remarks= "N/A"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

        #Calls the function
        changeRankOptions()


def listOfAACMembers():
    #Clearing all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates listbox frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = 50)

    #Creates listbox and inserts contents of database into it
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 30, height=40, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creates scrollbar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)


##################################################################################################################


def listStores():

    #Clear all widgits in left bottom frame, middle frame and right frame
    for widgets in leftBottomFrame.winfo_children():
        widgets.destroy()
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a canvas
    canvas = ctk.CTkCanvas(middleFrame, bg= "#292929", highlightthickness=0, width= 450, height= 1300)
    canvas.pack(side="left")

    #Creats scroll bar
    buttonScrollbar= ctk.CTkScrollbar(middleFrame, orientation=VERTICAL, command=canvas.yview)
    buttonScrollbar.pack(side="left", fill=Y)

    #Assigns scroll bar to the canvas
    canvas.configure(yscrollcommand=buttonScrollbar.set)
    canvas.bind('<Configure>', lambda e : canvas.configure(scrollregion= canvas.bbox("all")))

    #Creates a frame
    buttonFrame= ctk.CTkFrame(canvas, fg_color= "#292929", width= 450, height= 1300)
    buttonFrame.pack()

    #Creats widnow within the canvas
    canvas.create_window((0,0), window=buttonFrame, anchor= "nw")

    cursor = connection.cursor()
    buttonDict = {}
    data = cursor.execute("SELECT CategoryID,Category FROM Categories").fetchall()
    for item in data:

        category = item[1]

        def listStoresAction(x = item): 
            return listStoresTextUpdation(x)

        buttonDict[item] = ctk.CTkButton(
        buttonFrame,
        text= category,
        font= standardFont,
        width= 300,
        height= standardHeight,
        command=listStoresAction,
        )
        buttonDict[item].pack(pady = 5)


def listStoresTextUpdation(categoryName):
           
    categoryID = categoryName[0]
    listStoresViewStores(categoryID)


def listStoresViewStores(categoryID):

    #Clear all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the item you wish to modify \n FORMAT = StoreID, Name, Size, Qty", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates a frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Create list box and writes the contents of the database into it
    storesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 35, height=25, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT StoreID,Name,Size,Qty FROM Stores WHERE CategoryID={categoryID}").fetchall()
    formatted_data = []
    for item in data:
        store_id = item[0]
        name = item[1]
        size = item[2] if item[2] is not None else 'N/A'
        qty = item[3]
        formatted_data.append(f"{store_id}, {name} {size}, {qty}")
    for row in formatted_data:
        storesListListbox.insert(END, row)
    storesListListbox.pack(side=LEFT)

    #Creates a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=storesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    storesListListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates a frame
    frameOne= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    frameOne.pack()

    #Creates an entry box
    newQuantityEntry = ctk.CTkEntry(
        frameOne, 
        placeholder_text="Enter New Quantity",
        font= standardFont,
        width= 200,
        height= standardHeight,
        )
    newQuantityEntry.pack(side= "left", padx = 10)

    #Creates a button
    changeQuantityButton = ctk.CTkButton(
        frameOne,
        text= "Update Quantity",
        font= standardFont,
        width= 150,
        height= standardHeight,
        command= lambda: listStoresUpdateQuantity(storesListListbox,formatted_data,newQuantityEntry,categoryID),
        )
    changeQuantityButton.pack(side= "right", padx = 10)
 

def listStoresUpdateQuantity(storesListListbox,formatted_data,newQuantityEntry,categoryID):

    #Gets lsit box selection
    rowSelection = storesListListbox.curselection()

    #Checks if there was a selection
    if rowSelection:
        #Getting all information required and gets quantity and ID using SQL
        rowIndex = rowSelection[0]
        row = formatted_data[rowIndex]
        newQuantity = newQuantityEntry.get()
        storeID= str(row).split(',')
        storeID = storeID[0].strip()

        cursor = connection.cursor()
        oldQtyName = cursor.execute(f"SELECT Name,Size,Qty FROM Stores WHERE StoreID={storeID}").fetchall()
        oldQtyName = str(oldQtyName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "")


        cursor = connection.cursor()
        cursor.execute(f"UPDATE Stores SET Qty='{newQuantity}' WHERE StoreID={storeID}")
        connection.commit()

        cursor = connection.cursor()
        newQtyName = cursor.execute(f"SELECT Name,Size,Qty FROM Stores WHERE StoreID={storeID}").fetchall()
        newQtyName = str(newQtyName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "")

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "18"
        Before= oldQtyName
        After= newQtyName
        User_Input= newQuantity
        Remarks= "N/A"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()

    #Call the function
    listStoresViewStores(categoryID)


##################################################################################################################


def orderingOptions():

    #Clear widgits in left bottom frame, middle frame and right frame
    for widgets in leftBottomFrame.winfo_children():
        widgets.destroy()
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a ctk label
    label = ctk.CTkLabel(leftBottomFrame, text="Select The Person Ordering", fg_color="transparent", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates a ctk frame
    listboxFrame= ctk.CTkFrame(leftBottomFrame, fg_color= "#292929")
    listboxFrame.pack()

    #Creates a listbox and inserts the contents of the file into it
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 25, height= 15, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formattedDataName = []
    for row in data:
        formattedDataName.append(' '.join(map(str, row)))
    for row in formattedDataName:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creates a ctk scrollbar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)        

    #Creates a ctk button
    global selectPersonOrderingButton
    selectPersonOrderingButton = ctk.CTkButton(
        leftBottomFrame,
        text= "Select Person Ordering",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command= lambda: selectedPersonOrdering(namesListListbox),
        )
    selectPersonOrderingButton.pack(pady = standardYPadding)


def ordering():

    storesListListbox.delete(0, END)
    for row in formatted_data:
        storesListListbox.insert(END, row)

    #Adds the command prompt the button functions
    addToOrderBotton.configure(command=addToOrder)
    removeFromOrderBotton.configure(command=removeFromOrder)
    confirmOrderBotton.configure(command=confirmedOrder)


def addToOrder():
    #Gets list box selection
    selection = storesListListbox.curselection()

    #Make sure there is a selection
    if selection:
        #Gets value that was selected in listbox, turns it into a string and cleans it up
        itemListBox = storesListListbox.get(selection[0]) 
        itemString = str(itemListBox)
        itemID = itemString.split(',')[0].strip().replace("'","").replace(")","")
        itemQuantity = itemString.split(',')[2].strip().replace("'","").replace(")","")
        itemQuantityInt = int(itemQuantity)
        item = itemString.split(',')[1].strip().replace("'","").replace(")","")
        item = itemID+', '+item
        qty_sale = "1" 

        if itemQuantityInt < int(qty_sale):
            #Creates error window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "Not enough items in stock",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)
        #If quantity required is less/same than current quantity
        else:
            #Adds item to listbox
            ordersListbox.insert(END, f"{item}")
            #Makes variable global
            global saveOrdersListbox
            #saving contents of the listbox
            saveOrdersListbox = ordersListbox.get(0, END)
            #subtracts 1 from the current quantity
            newItemQuantity = str(itemQuantityInt - 1)
            #Updates the database using SQL
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Stores SET Qty='{newItemQuantity}' WHERE StoreID={itemID}")
            connection.commit()

            cursor = connection.cursor()
            itemName = cursor.execute(f"SELECT Name FROM Stores WHERE StoreID={itemID}").fetchall()
            itemName = str(itemName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            itemSize = cursor.execute(f"SELECT Size FROM Stores WHERE StoreID={itemID}").fetchall()
            itemSize = str(itemSize).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "21"
            Before= "N/A"
            After= f"{itemName} {itemSize}"
            User_Input= "N/A"
            Remarks= "N/A"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            #Retrieves data from database to be inserted into listbox
            cursor = connection.cursor()
            data = cursor.execute(SQLCommand).fetchall()
            formatted_data = []
            for item in data:
                store_id = item[0]
                name = item[1]
                size = item[2] if item[2] is not None else 'N/A'
                qty = item[3]
                formatted_data.append(f"{store_id}, {name} {size}, {qty}")

            #Clears all information in listbox
            storesListListbox.delete(0, END)
                #Inserts database data into listbox
            for row in formatted_data:
                storesListListbox.insert(END, row)
            
            #Creates button list and calls the variable
            button_list = [AACMemberOptionsButton,listOfStoresButton,orderingOptionsButton,storesReturnsButton,selectPersonOrderingButton,adminButton,closeWindow]
            check_listbox_empty(ordersListbox, button_list)


def disable_buttons_except_one(button_list):     
    #Disables all buttons in button list 
    for button in button_list:
        button.configure(state= DISABLED)


def enable_all_buttons(button_list):
    #Enables all buttons in button list 
    for button in button_list:
        button.configure(state= NORMAL)


def check_listbox_empty(listbox, button_list):
    #Checks if listbox has more than 0 items in it and calls the function
    if listbox.size() > 0:
        disable_buttons_except_one(button_list)
    #Checks if has 0 or less items in it and calls the function
    else:
        enable_all_buttons(button_list)


def removeFromOrder():
                
    #Gets celection from the listbox
    selection = ordersListbox.curselection()
    #If there is a selection it gets selected value in the listbox and turns it into a string and splits it into useful values saved as variables
    if selection:
        itemListBox = ordersListbox.get(selection[0]) 
        itemString = str(itemListBox)
        itemID = itemString.split(',')[0].strip().replace("'","").replace(")","")
        item = itemString.split(',')[1].strip().replace("'","").replace(")","")
        item = itemID+', '+item
            
        cursor = connection.cursor()
        itemQuantity=cursor.execute(f"SELECT Qty FROM Stores WHERE StoreID={itemID}").fetchall()
        connection.commit()

        #Deletes selected item from listbox
        ordersListbox.delete(selection[0])
        #Makes variable global
        global saveOrdersListbox
        #Gets item selected in listbox
        saveOrdersListbox = ordersListbox.get(0, END)

        itemQuantity=str(itemQuantity).replace("'","").replace("[","").replace("(","").replace(",","").replace(")","").replace("]","")
        itemQuantity=int(itemQuantity)
        #Adds 1 to current value
        newItemQuantity = str(itemQuantity + 1)
        
        #Updates database using SQL
        cursor = connection.cursor()
        cursor.execute(f"UPDATE Stores SET Qty='{newItemQuantity}' WHERE StoreID={itemID}")
        connection.commit()

        cursor = connection.cursor()
        itemName = cursor.execute(f"SELECT Name FROM Stores WHERE StoreID={itemID}").fetchall()
        itemName = str(itemName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        itemSize = cursor.execute(f"SELECT Size FROM Stores WHERE StoreID={itemID}").fetchall()
        itemSize = str(itemSize).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "22"
        Before= f"{itemName} {itemSize}"
        After= "N/A"
        User_Input= "N/A"
        Remarks= "N/A"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()

        #Retrieves data from database to be inserted into listbox
        cursor = connection.cursor()
        data = cursor.execute(SQLCommand).fetchall()
        formatted_data = []
        for item in data:
            store_id = item[0]
            name = item[1]
            size = item[2] if item[2] is not None else 'N/A'
            qty = item[3]
            formatted_data.append(f"{store_id}, {name} {size}, {qty}")

        #Deletes all contents in listbox and inserts contents of database into the now empty listbox
        storesListListbox.delete(0, END)
        for row in formatted_data:
            storesListListbox.insert(END, row)
        
        #Defines variable to disable buttons
        def disable_buttons_except_one(button_list):     
            #Disables all buttons in button list 
            for button in button_list:
                button.configure(state= DISABLED)


        #Defines variable to enable buttons
        def enable_all_buttons(button_list):
            #Enables all buttons in button list 
            for button in button_list:
                button.configure(state= NORMAL)


        #Defines variable to disable buttons
        def check_listbox_empty(listbox, button_list):
            #Checks if listbox has more than 0 items in it and calls the function
            if listbox.size() > 0:
                disable_buttons_except_one(button_list)
            #Checks if has 0 or less items in it and calls the function
            else:
                enable_all_buttons(button_list)
        
        #Creates button list and calls the variable
        button_list = [AACMemberOptionsButton,listOfStoresButton,orderingOptionsButton,storesReturnsButton,selectPersonOrderingButton,adminButton,closeWindow]
        check_listbox_empty(ordersListbox, button_list)


def shortTermCheckboxEvent():

    #Gets the date and time     
    Data_Taken = datetime.datetime.now().strftime("%d/%m/%Y")
    Log_TypeID='1'
    

    #Setting a variable
    ordersListboxString = ""
    ordersListboxList = ""

    #Saves listbox to a variable
    for i in range(ordersListbox.size()):
        ordersListboxString += str(ordersListbox.get(i)) + "\n"
        ordersListboxList += ordersListbox.get(i)
    saveOrdersListbox = ordersListbox.get(0, END)

    #Sets an empty array
    wordCounts = {}

    #Iterating through lines in a file    
    for row in saveOrdersListbox:
        #Striping words and splitting words into collumns

        if row != '':
            #Checks if word is in wordcounts, if it is it adds 1 to total
            if row in wordCounts:
                wordCounts[row] += 1

            #Adds word to word count    
            else:
                wordCounts[row] = 1

    #Removes unwanted puncuation
    ItemsClean= (str(wordCounts)).replace("{", "").replace("'", "").replace(",", "|").replace(":", ",").replace("}", "").replace(",", "|")

    #Splits the variable every 3 '|'
    ItemsClean = (ItemsClean)
    ItemsClean = ItemsClean.split('|')
    ItemsClean = [ItemsClean[i:i+3] for i in range(0, len(ItemsClean), 3)]
    #Saves data to variables
    for item in ItemsClean:
        StoreID= str(item).split(',')[0].replace("[","").replace("'","").replace("]","").replace(" ","")
        Qty_Taken= str(item).split(',')[2].replace("[","").replace("'","").replace("]","").replace(" ","")

        #Inserts new data into database
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO Logs (CadetID,StoreID,Qty_Taken,Date_Taken,Log_TypeID) VALUES ('{CadetID}', '{StoreID}', '{Qty_Taken}', '{Data_Taken}', '{Log_TypeID}')")
        connection.commit()

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "23"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "20"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()
            
    #Clears all widgits in middle frame and right frame
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()


def longTermCheckboxEvent():

    #Gets the date and time     
    Data_Taken = datetime.datetime.now().strftime("%d/%m/%Y")
    Log_TypeID='1'
    

    #Setting a variable
    ordersListboxString = ""
    ordersListboxList = ""

    #Saves listbox to a variable
    for i in range(ordersListbox.size()):
        ordersListboxString += str(ordersListbox.get(i)) + "\n"
        ordersListboxList += ordersListbox.get(i)
    saveOrdersListbox = ordersListbox.get(0, END)

    #Sets an empty array
    wordCounts = {}

    #Iterating through lines in a file    
    for row in saveOrdersListbox:
        #Striping words and splitting words into collumns

        if row != '':
            #Checks if word is in wordcounts, if it is it adds 1 to total
            if row in wordCounts:
                wordCounts[row] += 1

            #Adds word to word count    
            else:
                wordCounts[row] = 1

    #Removes unwanted puncuation
    ItemsClean= (str(wordCounts)).replace("{", "").replace("'", "").replace(",", "|").replace(":", ",").replace("}", "").replace(",", "|")

    #Splits the variable every 3 '|'
    ItemsClean = (ItemsClean)
    ItemsClean = ItemsClean.split('|')
    ItemsClean = [ItemsClean[i:i+3] for i in range(0, len(ItemsClean), 3)]
    #Saves data to variables
    for item in ItemsClean:
        StoreID= str(item).split(',')[0].replace("[","").replace("'","").replace("]","").replace(" ","")
        Qty_Taken= str(item).split(',')[2].replace("[","").replace("'","").replace("]","").replace(" ","")

        #Inserts new data into database
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO Logs (CadetID,StoreID,Qty_Taken,Date_Taken,Log_TypeID) VALUES ('{CadetID}', '{StoreID}', '{Qty_Taken}', '{Data_Taken}', '{Log_TypeID}')")
        connection.commit()

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "24"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "20"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()
            
    #Clears all widgits in middle frame and right frame
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()


def confirmedOrder():
    #Gets selection from the listboxs
    resultShort= shortTermCheckbox.get()
    resultLong= longTermCheckbox.get()

    #Checks if short term checkbox was selected 
    if resultShort == 1:
        #Checks if long term checkbox was selected
        if resultLong == 1:
            #Creates a ctk window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a ctk label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "You have selected more than one box, Please try again",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a ctk button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)
                
        #Checks if long term checkbox was not selected
        elif resultLong == 0:
            #Defines the list
            button_list = [AACMemberOptionsButton,listOfStoresButton,orderingOptionsButton,storesReturnsButton,selectPersonOrderingButton,adminButton,closeWindow]
            #Goes through the list and enables the buttons
            for button in button_list:
                button.configure(state= NORMAL)
            #Calls the function
            shortTermCheckboxEvent()

        #Checks if anything else was done to checkbox
        else:
            #Creates ctk window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a ctk label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "We have encounted an error, Please try again",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates ctk button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)
            
    #Checks if long term checkbox was selected
    elif resultLong == 1:
        #Checks if short term checkbox was selected
        if resultShort == 1:
            #Creates a ctk window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a ctk label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "You have selected more than one box, Please try again",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a ctk button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)

        #Checks if short term checkbox was not selected
        elif resultShort == 0:
            #Defines a list
            button_list = [AACMemberOptionsButton,listOfStoresButton,orderingOptionsButton,storesReturnsButton,selectPersonOrderingButton,adminButton,closeWindow]
            #Enables all buttons in the list
            for button in button_list:
                button.configure(state= NORMAL)
            #Calls the function
            longTermCheckboxEvent()

        #Checks if anything else was done to checkbox
        else:
            #Creates ctk window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates ctk label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "We have encounted an error, Please try again",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates ctk button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)
    
    #Checks if short term and long term checkboxs are not selected
    elif resultShort == 0 and resultLong == 0:
        #Creates a ctk window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creates a ctk label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a box, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

    #Checks if anything else was done to checkbox
    else:
        #Creates a ctk Window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a ctk label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "We have encounted an error, Please try again",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardHeight,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)


def selectedPersonOrdering(namesListListbox):
    #Makes a global variable
    global rankNameClean
    #Gets curser selectin
    rankNameSelection= namesListListbox.curselection()
    #Checks if there was no selection
    if not rankNameSelection:
        #Creates ctk window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates ctk label    
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

    #Checks if there was a selection
    else:
        #Gets value in the selection
        rankName= namesListListbox.get(rankNameSelection[0])
        #Cleans the string up removing any unwanted character
        rankNameClean= str(rankName).replace("(", "").replace("'", "").replace(" ", "_").replace(")", "")

        #Makes global variable
        global CadetID
        CadetID= rankNameClean.split('_')[0]

        cursor = connection.cursor()
        Rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID={CadetID}").fetchall()
        Rank = str(Rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        First_Name = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID={CadetID}").fetchall()
        First_Name = str(First_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        Last_Name = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID={CadetID}").fetchall()
        Last_Name = str(Last_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "19"
        Before= "N/A"
        After= "N/A"
        User_Input= f"{Rank} {First_Name} {Last_Name}"
        Remarks= "N/A"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()

        #Calls the function
        storesList()


def storesList():

    for widgets in rightFrame.winfo_children():
        widgets.destroy()            

    #Creates a ctk canvas
    canvas = ctk.CTkCanvas(middleFrame, bg= "#292929", highlightthickness=0)
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    #Creates a scroll bar
    buttonScrollbar= ctk.CTkScrollbar(middleFrame, orientation=VERTICAL, command=canvas.yview)
    buttonScrollbar.pack(side="right", fill=Y)
    canvas.configure(yscrollcommand=buttonScrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

    #Creates a ctk frame
    buttonFrame= ctk.CTkFrame(canvas, fg_color= "#292929")
    buttonFrame.pack(pady = standardYPadding)

    #Creats canvas window?
    canvas.create_window((0,0), window=buttonFrame, anchor= "nw")

    cursor = connection.cursor()
    buttonDict = {}
    data = cursor.execute("SELECT CategoryID,Category FROM Categories").fetchall()
    for item in data:

        category = item[1]
        def ordersAction(x=item): 
            return ordersTextUpdation(x)

        buttonDict[item] = ctk.CTkButton(
        buttonFrame,
        text= category,
        font= standardFont,
        width= 300,
        height= standardHeight,
        command=ordersAction,
        )
        buttonDict[item].pack(pady = 5)
        
    #Creates a ctk label
    label = ctk.CTkLabel(rightFrame, text="Select An Item Then Click The Button Bellow \nThe Box To Add/Remove It From The Order \n\nFORMAT = StoreID, Name Size, QTY", fg_color="transparent", font= standardFont)
    label.pack(pady = 0)

    #Creates ctk frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack()

    #Makes variable global
    global storesListListbox
    #Creates a ctk list box
    storesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 40, height= 11, font= standardFont)
    storesListListbox.pack(side=LEFT)

    #Creates a ctk scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=storesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    storesListListbox.config(yscrollcommand=listboxScrollbar.set)

    #Makes the variable global
    global addToOrderBotton
    #Creates a ctk button
    addToOrderBotton = ctk.CTkButton(
        rightFrame,
        text= "Add Item To Order",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    addToOrderBotton.pack(pady = standardYPadding)

    #Creates a ctk Label
    warningLabel= ctk.CTkLabel(rightFrame, text="IF THE BOX BELLOW IS NOT EMPTY YOU WILL \n NOT BE ABLE TO LEAVE THIS PAGE", fg_color="transparent", font= standardFont)
    warningLabel.pack(pady= standardYPadding)

    #Creates a ctk frame
    listboxFrameTwo= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrameTwo.pack()

    #Makes variable global
    global ordersListbox
    #Creates a listbox
    ordersListbox = Listbox(listboxFrameTwo, bg= "#292929", fg= "Silver", width= 40, height= 11, font= standardFont)
    ordersListbox.pack(side=LEFT)

    #Creates a ctk scrollbar
    listboxScrollbarTwo= ctk.CTkScrollbar(listboxFrameTwo, command=ordersListbox.yview)
    listboxScrollbarTwo.pack(side="right", fill=Y)
    ordersListbox.config(yscrollcommand=listboxScrollbarTwo.set)        

    #Makes the variable global
    global removeFromOrderBotton
    #Creates a ctk button
    removeFromOrderBotton = ctk.CTkButton(
        rightFrame,
        text= "Remove Item From Order",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    removeFromOrderBotton.pack(pady = standardYPadding)

    #Creates a ctk frame
    checkboxFrame= ctk.CTkFrame(rightFrame, width= 20, height= 20, fg_color= "#292929")
    checkboxFrame.pack()

    #Makes the variable global
    global shortTermCheckbox
    #Creates a ctk checkbox
    shortTermCheckbox= ctk.CTkCheckBox(
        checkboxFrame, 
        text="Short Term",
        font= ("", 15),
        checkbox_width= 20,
        checkbox_height= 20,
        onvalue= 1, 
        offvalue= 0,
        )
    shortTermCheckbox.pack(side= "left",padx= 25)

    #Makes the variable global
    global longTermCheckbox
    #Creates a ctk checkbox
    longTermCheckbox= ctk.CTkCheckBox(
        checkboxFrame, 
        text="Long Term",
        font= ("", 15), 
        checkbox_width= 20,
        checkbox_height= 20,
        onvalue= 1, 
        offvalue= 0,
        )
    longTermCheckbox.pack(side= "right", padx= 25)

    #Makes the variable global
    global confirmOrderBotton
    #Creates a ctk Button
    confirmOrderBotton = ctk.CTkButton(
        rightFrame,
        text= "Confirm Order",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    confirmOrderBotton.pack(pady = standardYPadding)


def ordersTextUpdation(categoryName):
        
    categoryID = categoryName[0]
    return selcetedCategory(categoryID)


def selcetedCategory(categoryID):

    #Makes variables global
    global SQLCommand
    #Saves the command to a variable
    SQLCommand = f"SELECT StoreID,Name,Size,Qty FROM Stores WHERE CategoryID={categoryID}"
    #Makes variables global
    global formatted_data
    formatted_data=""
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT StoreID,Name,Size,Qty FROM Stores WHERE CategoryID={categoryID}").fetchall()
    formatted_data = []
    for item in data:
        store_id = item[0]
        name = item[1]
        size = item[2] if item[2] is not None else 'N/A'
        qty = item[3]
        formatted_data.append(f"{store_id}, {name} {size}, {qty}")
    ordering()


##################################################################################################################


def storesReturns():

    #Clears all widgets
    for widgets in leftBottomFrame.winfo_children():
        widgets.destroy()
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a ctk label
    label = ctk.CTkLabel(middleFrame, text="Select The Person Returning", fg_color="transparent", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creats a ctk frame
    listboxFrame= ctk.CTkFrame(middleFrame, fg_color= "#292929")
    listboxFrame.pack()

    #Creates a listbox and insert contents from file into it
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 25, height= 25, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT, pady=standardYPadding)

    #Creates a ctk scrollbar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates a ctk button 
    viewShortTermLogsButton = ctk.CTkButton(
        middleFrame,
        text= "View Short Term Logs",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: shortTermSelctionCheck(namesListListbox),
        )
    viewShortTermLogsButton.pack(pady = standardYPadding)

    #Creates a ctk button 
    viewLongTermLogsButton = ctk.CTkButton(
        middleFrame,
        text= "View Long Term Logs",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: longTermSelctionCheck(namesListListbox),
        )
    viewLongTermLogsButton.pack(pady = standardYPadding)


def shortTermSelctionCheck(namesListListbox):
    #Makes variable global
    global rankNameClean
    #Gets users selection of the listbox
    rankNameSelection= namesListListbox.curselection()
    #Checks if there was no selection
    if not rankNameSelection:
        #Creates a ctk window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creates a ctk label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

    #Runs if there was a seletion
    else:
        #Gets the name from the seelection and gets rid of unwanted charactors and turns it into a string
        rankName= namesListListbox.get(rankNameSelection[0])
        rankNameClean= str(rankName).replace("(", "").replace("'", "").replace(",", "").replace(" ", "_").replace(")", "")
        global CadetID
        CadetID = rankNameClean.split('_')[0]

        #Calls the function
        viewShortTermLogs()


def longTermSelctionCheck(namesListListbox):
    #Makes variable global
    global rankNameClean
    #Gets users selection of the listbox
    rankNameSelection= namesListListbox.curselection()
    #Checks if there was no selection
    if not rankNameSelection:
        #Creates a ctk window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creates a ctk label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

    #Runs if there was a seletion
    else:
        #Gets the name from the seelection and gets rid of unwanted charactors and turns it into a string
        rankName= namesListListbox.get(rankNameSelection[0])
        rankNameClean= str(rankName).replace("(", "").replace("'", "").replace(",", "").replace(" ", "_").replace(")", "")
        global CadetID
        CadetID = rankNameClean.split('_')[0]

        #Calls the function
        viewLongTermLogs()


def viewShortTermLogs():

    #Clears all widgits from window
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a ctk label
    shortTermLogLabel = ctk.CTkLabel(rightFrame, text="Short Term Log \nFORMAT = LogID, [StoreID] Name Size, QTY, Date", fg_color="transparent", font= standardFont)
    shortTermLogLabel.pack(pady = standardYPadding)

    #Creates a ctk frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack()

    #Makes global variable
    global formatted_dataShort 

    #Creates a listbox and insert contents from file into it
    shortTermLogListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 40, height= 28, font= standardFont)
    #Gets all required data from database using SQL and formats it into desired format
    cursor = connection.cursor()
    dataLogsShort = cursor.execute(f"SELECT Logs.LogID,Logs.StoreID,Logs.Qty_Taken,Logs.Date_Taken FROM Logs WHERE Logs.Log_TypeID = 1 AND Logs.CadetID = {CadetID};").fetchall()
    formatted_dataShort = []
    for itemLogsShort in dataLogsShort:

        LogIDShort= itemLogsShort[0]
        cursor = connection.cursor()
        dataInnerJoinShort = cursor.execute(f"SELECT Stores.Name, Logs.StoreID FROM Logs INNER JOIN Stores ON Logs.StoreID = Stores.StoreID WHERE Logs.LogID = {LogIDShort};").fetchall()
        for ItemInnerJoinShort in dataInnerJoinShort:

            StoreID = ItemInnerJoinShort[1]
            cursor = connection.cursor()
            storesDataShort= cursor.execute(f"SELECT Size FROM Stores WHERE StoreID= {StoreID}")

            for itemStoresShort in storesDataShort:
                NameShort = ItemInnerJoinShort[0]
                SizeShort = itemStoresShort[0] if itemStoresShort[0] is not None else 'N/A'
                Qty_TakenShort = itemLogsShort[2]
                Date_TakenShort = itemLogsShort[3]
                formatted_dataShort.append(f"{LogIDShort}, [{StoreID}] {NameShort} {SizeShort}, {Qty_TakenShort}, {Date_TakenShort}")

    #Inserts formated data into listbox
    for rowShort in formatted_dataShort:
        shortTermLogListbox.insert(END, rowShort)
    shortTermLogListbox.pack(side=LEFT)

    #Creates a ctk scrollbar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=shortTermLogListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    shortTermLogListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates a ctk frame
    frameTwo= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    frameTwo.pack()

    #Creates a ctk entry box
    quantityReturnEntryShort = ctk.CTkEntry(
        frameTwo, 
        placeholder_text="Enter Quantity Returned",
        font= standardFont,
        width= 210,
        height= standardHeight,
        )
    quantityReturnEntryShort.pack(side= "left", padx = 10, pady = 20)

    #Creates a ctk button 
    changeQuantityButtonShort = ctk.CTkButton(
        frameTwo,
        text= "Update Quantity",
        font= standardFont,
        width= 100,
        height= standardHeight,
        command=lambda: shortTermLogReturn(shortTermLogListbox,quantityReturnEntryShort),
        )
    changeQuantityButtonShort.pack(side= "right", padx = 10, pady = 20)


def viewLongTermLogs():
    #Clears all widgits from window
    for widgets in rightFrame.winfo_children():
        widgets.destroy()
    

    #Creates a ctk label
    longTermLoglabel = ctk.CTkLabel(rightFrame, text="Long Term Log \nFORMAT = LogID, [StoreID] Name Size, QTY, Date", fg_color="transparent", font= standardFont)
    longTermLoglabel.pack(pady = standardYPadding)

    #Creates a ctk frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack()

    #Makes global variable
    global formatted_dataLong         

    #Creates a listbox and insert contents from file into it
    longTermLogListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 40, height= 28, font= standardFont)
    #Gets all required data from database using SQL and formats it into desired format
    cursor = connection.cursor()
    dataLogsLong = cursor.execute(f"SELECT Logs.LogID,Logs.StoreID,Logs.Qty_Taken,Logs.Date_Taken FROM Logs WHERE Logs.Log_TypeID = 2 AND Logs.CadetID = {CadetID};").fetchall()
    #dataInnerJoinLong = cursor.execute(f"SELECT Stores.Name, Logs.StoreID FROM Logs INNER JOIN Stores ON Logs.StoreID = Stores.StoreID WHERE Logs.Log_TypeID = 2 AND Logs.CadetID = {CadetID};").fetchall()
    formatted_dataLong = []
    for itemLogsLong in dataLogsLong:

        LogIDLong = itemLogsLong[0]
        cursor = connection.cursor()
        dataInnerJoinLong = cursor.execute(f"SELECT Stores.Name, Logs.StoreID FROM Logs INNER JOIN Stores ON Logs.StoreID = Stores.StoreID WHERE Logs.LogID = {LogIDLong};").fetchall()
        
        for ItemInnerJoinLong in dataInnerJoinLong:

            StoreID = ItemInnerJoinLong[1]
            cursor = connection.cursor()
            storesDataLong= cursor.execute(f"SELECT Size FROM Stores WHERE StoreID= {StoreID}")

            for itemStoresLong in storesDataLong:
                NameLong = ItemInnerJoinLong[0]
                SizeLong = itemStoresLong[0] if itemStoresLong[0] is not None else 'N/A'
                Qty_TakenLong = itemLogsLong[2]
                Date_TakenLong = itemLogsLong[3]
                formatted_dataLong.append(f"{LogIDLong}, [{StoreID}] {NameLong} {SizeLong}, {Qty_TakenLong}, {Date_TakenLong}")
    
    #Inserts formated data into listbox
    for rowLong in formatted_dataLong:
        longTermLogListbox.insert(END, rowLong)
    longTermLogListbox.pack(side=LEFT)

    #Creates a ctk scrollbar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=longTermLogListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    longTermLogListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates a ctk frame
    frameOne= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    frameOne.pack()

    #Creates a ctk entry box
    quantityReturnEntryLong = ctk.CTkEntry(
        frameOne, 
        placeholder_text="Enter Quantity Returned",
        font= standardFont,
        width= 210,
        height= standardHeight,
        )
    quantityReturnEntryLong.pack(side= "left", padx = 10, pady = 20)

    #Creates a ctk button 
    changeQuantityButtonLong = ctk.CTkButton(
        frameOne,
        text= "Update Quantity",
        font= standardFont,
        width= 100,
        height= standardHeight,
        command= lambda: longTermLogReturn(longTermLogListbox,quantityReturnEntryLong),
        )
    changeQuantityButtonLong.pack(side= "right", padx = 10, pady = 20)


def shortTermLogReturn(shortTermLogListbox,quantityReturnEntryShort):
    #Gets listbox selection
    rowSelection = shortTermLogListbox.curselection()

    #Runs if there was a selection
    if rowSelection:
        #Sets all important information into the variables
        row= shortTermLogListbox.get(rowSelection[0])
        rowClean= str(row).replace('[','').replace(']',',').split(',')
        LogID= rowClean[0]
        StoreID= rowClean[1]
        rowShort = rowClean[3]
        oldValueShort= int(rowShort[1])
        quantityReturnShort = int(quantityReturnEntryShort.get())
        newQuantity= oldValueShort - quantityReturnShort

        #Checks if new quantity is equal to 0
        if newQuantity == 0:
            
            #Updates the qty in logs while deleating it from the logs on the database using SQL
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Stores SET Qty= Qty + {quantityReturnShort} WHERE StoreID= {StoreID}")
            cursor.execute(f"DELETE FROM Logs WHERE LogID= {LogID}").fetchall()
            connection.commit()

            cursor = connection.cursor()
            Rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Rank = str(Rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            First_Name = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            First_Name = str(First_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            Last_Name = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Last_Name = str(Last_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "25"
            Before= oldValueShort
            After= newQuantity
            User_Input= quantityReturnShort
            Remarks= f"{Rank} {First_Name} {Last_Name}"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            viewShortTermLogs()
            
        #Checks if new quantity is bigger than 0
        elif newQuantity > 0:

            #Updates the qty in logs while updating it from the logs on the database using SQL
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Stores SET Qty= Qty + {quantityReturnShort} WHERE StoreID= {StoreID}")
            cursor.execute(f"UPDATE Logs SET Qty_Taken= Qty_Taken - {quantityReturnShort} WHERE LogID= {LogID}").fetchall()
            connection.commit()

            cursor = connection.cursor()
            Rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Rank = str(Rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            First_Name = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            First_Name = str(First_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            Last_Name = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Last_Name = str(Last_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "25"
            Before= oldValueShort
            After= newQuantity
            User_Input= quantityReturnShort
            Remarks= f"{Rank} {First_Name} {Last_Name}"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            viewShortTermLogs()

        #Checks if new quantity is smaller than 0
        elif newQuantity < 0:

            #Creates a ctk window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a ctk label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "Trying To Return More Than They Have Taken Out",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a ctk button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)

    else:
        #Creates a ctk window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a ctk label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an item",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)


def longTermLogReturn(longTermLogListbox,quantityReturnEntryLong):
    #Gets listbox selection
    rowSelection = longTermLogListbox.curselection()

    #Runs if there was a selection
    if rowSelection:
        #Sets all important information into the variables
        row= longTermLogListbox.get(rowSelection[0])
        rowClean= str(row).replace('[','').replace(']',',').split(',')
        LogID= rowClean[0]
        StoreID= rowClean[1]
        rowLong = rowClean[3]
        oldValueLong= int(rowLong[1])
        quantityReturnLong = int(quantityReturnEntryLong.get())
        newQuantity= oldValueLong - quantityReturnLong

        #Checks if new quantity is equal to 0
        if newQuantity == 0:

            #Updates the qty in logs while deleating it from the logs on the database using SQL
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Stores SET Qty= Qty + {quantityReturnLong} WHERE StoreID= {StoreID}")
            cursor.execute(f"DELETE FROM Logs WHERE LogID= {LogID}").fetchall()
            connection.commit()

            cursor = connection.cursor()
            Rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Rank = str(Rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            First_Name = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            First_Name = str(First_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            Last_Name = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Last_Name = str(Last_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "26"
            Before= oldValueLong
            After= newQuantity
            User_Input= quantityReturnLong
            Remarks= f"{Rank} {First_Name} {Last_Name}"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            viewLongTermLogs()

        #Checks if new quantity is bigger than 0
        elif newQuantity > 0:

            #Updates the qty in logs while updating it from the logs on the database using SQL
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Stores SET Qty= Qty + {quantityReturnLong} WHERE StoreID= {StoreID}")
            cursor.execute(f"UPDATE Logs SET Qty_Taken= Qty_Taken - {quantityReturnLong} WHERE LogID= {LogID}").fetchall()
            connection.commit()

            cursor = connection.cursor()
            Rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Rank = str(Rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            First_Name = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            First_Name = str(First_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
            Last_Name = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID = {CadetID}").fetchall()
            Last_Name = str(Last_Name).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "26"
            Before= oldValueLong
            After= newQuantity
            User_Input= quantityReturnLong
            Remarks= f"{Rank} {First_Name} {Last_Name}"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            viewLongTermLogs()

        #Checks if new quantity is smaller than 0
        elif newQuantity < 0:

            #Creates a ctk window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a ctk label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "Trying To Return More Than They Have Taken Out",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a ctk button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)

    else:
        #Creates a ctk window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a ctk label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an item",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)


################################### ADMIN OPTIONS ###################################################


def adminOptions():

    for widgets in leftBottomFrame.winfo_children():
        widgets.destroy()
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a ctk window
    global passwordWindow
    passwordWindow= ctk.CTkToplevel(root)
    passwordWindow.title("Log In Window")
    passwordWindow.geometry("500x300")
    passwordWindow.transient(root)
    passwordWindow.lift()

    for widgets in passwordWindow.winfo_children():
        widgets.destroy()

    #Creates a ctk label
    passwordLabel= ctk.CTkLabel(
        passwordWindow,
        text= "Please Enter the Admin Pasword",
        font= standardFont
        )
    passwordLabel.pack(pady= standardYPadding)

    #Creates a ctk entry box
    global passwordEntry
    passwordEntry= ctk.CTkEntry(
        passwordWindow,
        placeholder_text="Enter Pasword",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        show= '*'
        )
    passwordEntry.pack(pady= standardYPadding)

    #Creates a ctk button
    passwordButton= ctk.CTkButton(
        passwordWindow,
        text= "Log In",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: logIn(passwordWindow,passwordEntry)
        )
    passwordButton.pack(pady= standardYPadding)

    #Creates a ctk button
    passwordButton= ctk.CTkButton(
        passwordWindow,
        text= "Forgot the Password",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: forgotPassword(passwordWindow)
        )
    passwordButton.pack(pady= standardYPadding)

    #Creates a ctk button
    passwordButton= ctk.CTkButton(
        passwordWindow,
        text= "Close Window",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command= passwordWindow.destroy
        )
    passwordButton.pack(pady= standardYPadding)


def forgotPassword(passwordWindow):

    for widgets in passwordWindow.winfo_children():
        widgets.destroy()

    cursor = connection.cursor()
    data = cursor.execute("SELECT Secret_Question,Secret_Question_Answer,Password FROM Accounts WHERE Account_TypeID = 1").fetchall()
    formatted_data = []
    for item in data:
        adminAccountSecretQuestion = item[0]
        adminAccountSecretQuestionAnswer = item[1]
        adminAccountPassword = item[2]
        formatted_data.append(f"{adminAccountSecretQuestion}, {adminAccountSecretQuestionAnswer}, {adminAccountPassword}")

    #Creates a ctk label
    label = ctk.CTkLabel(passwordWindow, text=f"The secret question is: \n{adminAccountSecretQuestion}", fg_color="transparent", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates an entry box
    adminAccountQuestionAnswer = ctk.CTkEntry(
        passwordWindow, 
        placeholder_text="Enter the Answer to the Question",
        font= standardFont,
        width= 400,
        height= standardHeight,
        show= '*'
        )
    adminAccountQuestionAnswer.pack(pady = standardYPadding)

    #Creates a button
    questionCheckerButton = ctk.CTkButton(
        passwordWindow,
        text= "Submit Answer",
        font= standardFont,
        width= 400,
        height= standardHeight,
        command=lambda: adminLogInQuestionChecker(passwordWindow,adminAccountQuestionAnswer,adminAccountSecretQuestionAnswer,adminAccountPassword),
        )
    questionCheckerButton.pack(pady = standardYPadding)

    #Creates a button
    questionCheckerButton = ctk.CTkButton(
        passwordWindow,
        text= "Return to Log In Page",
        font= standardFont,
        width= 400,
        height= standardHeight,
        command=lambda: returnToLogin(passwordWindow),
        )
    questionCheckerButton.pack(pady = standardYPadding)

    
    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "4"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "Admin"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()


def returnToLogin(passwordWindow):
    passwordWindow.destroy()
    adminOptions()


def adminLogInQuestionChecker(passwordWindow,adminAccountQuestionAnswer,adminAccountSecretQuestionAnswer,adminAccountPassword):

    adminQuestionAnswer= adminAccountQuestionAnswer.get()

    if adminQuestionAnswer != adminAccountSecretQuestionAnswer:
        for widgets in passwordWindow.winfo_children():
            widgets.destroy()

        #Creates a label
        errorLabel= ctk.CTkLabel(
            passwordWindow,
            text= "Your answer does not match the correct answer",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            passwordWindow,
            text= "Return to Previous Page",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= lambda: forgotPassword(passwordWindow)
            )
        errorButton.pack(pady= standardYPadding)

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "9"
        Before= "N/A"
        After= "N/A"
        User_Input= adminQuestionAnswer
        Remarks= "Admin"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()

    else:
        for widgets in passwordWindow.winfo_children():
            widgets.destroy()

        #Creates a ctk label
        label = ctk.CTkLabel(passwordWindow, text=f"The Password is: \n{adminAccountPassword}", fg_color="transparent", font= standardFont)
        label.pack(pady = standardYPadding)

        #Creates a button
        returnToLoginButton= ctk.CTkButton(
            passwordWindow,
            text= "Return to Log In Page",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command=lambda: returnToLogin(passwordWindow)
            )
        returnToLoginButton.pack(pady= standardYPadding)


def logIn(passwordWindow,passwordEntry):

    passwords= []
    cursor = connection.cursor()
    data= cursor.execute(f"SELECT Password FROM Accounts WHERE Account_TypeID = 1").fetchall()
    data= str(data).replace('(','').replace(')','').replace(',','').replace("'",'').replace(" ",',').replace("[",'').replace("]",'')
    data=data.split(',')
    for password in data:
        passwords.append(password)
    userEntry= passwordEntry.get()

    if userEntry not in passwords:

        for widgets in passwordWindow.winfo_children():
            widgets.destroy()

        #Creates a ctk label
        passwordErrorLabel= ctk.CTkLabel(
            passwordWindow,
            text= "Incorect password. Return to log in page and try again.",
            font= standardFont
            )
        passwordErrorLabel.pack(pady= standardYPadding)

        #Creates a ctk button
        passwordErrorButton= ctk.CTkButton(
            passwordWindow,
            text= "Return to Log In Page",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= lambda: returnToLogin(passwordWindow)
            )
        passwordErrorButton.pack(pady= standardYPadding)

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "3"
        Before= "N/A"
        After= "N/A"
        User_Input= userEntry
        Remarks= "Admin"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()


    elif userEntry in passwords:
        passwordWindow.destroy()

        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "1"
        Before= "N/A"
        After= "N/A"
        User_Input= userEntry
        Remarks= "Admin"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()



        succesfulLogIn()


def succesfulLogIn():

    #Creats a ctk button
    removePersonButton = ctk.CTkButton(
        leftBottomFrame,
        text= "Remove An AAC Member",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=removeAACMemberOptions,
        )
    removePersonButton.pack(pady = standardYPadding)

    #Creats a ctk button
    changeIDButton = ctk.CTkButton(
        leftBottomFrame,
        text= "Change AAC Member ID",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=changeIDOptions,
        )
    changeIDButton.pack(pady = standardYPadding)

    #Creats a ctk button
    removeStoresButton = ctk.CTkButton(
        leftBottomFrame,
        text= "Remove Stores",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=removeStoreOptions,
        )
    removeStoresButton.pack(pady = standardYPadding)

    #Creats a ctk button
    addStoresButton = ctk.CTkButton(
        leftBottomFrame,
        text= "Add Stores",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=addStoresOptions,
        )
    addStoresButton.pack(pady = standardYPadding)

    #Creats a ctk button
    adminAcountButton = ctk.CTkButton(
        leftBottomFrame,
        text= "Admin Account Options",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=adminAccountOptions,
        )
    adminAcountButton.pack(pady = standardYPadding)

    #Creats a ctk button
    userAcountButton = ctk.CTkButton(
        leftBottomFrame,
        text= "User Account Options",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=userAccountOptions,
        )
    userAcountButton.pack(pady = standardYPadding)

    #Creats a ctk button
    viewLogsButton = ctk.CTkButton(
        leftBottomFrame,
        text= "View Logs",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=viewLogsOptions,
        )
    viewLogsButton.pack(pady = standardYPadding)

#--------------------------------- REMOVE MEMBER OPTIONS -------------------------------------------------------------

def removeAACMemberOptions():

    #Deletes all widgits
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(middleFrame, text="Select the person you wish to remove", font= standardFont)
    label.pack(pady = standardYPadding)

    #Create frame
    listboxFrame= ctk.CTkFrame(middleFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creates list box and fills it with members names using SQL
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 30, height= 30, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creates scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)        

    #Creates button to call a function
    removeAACMemberButton = ctk.CTkButton(
        middleFrame,
        text= "Remove AAC Member From List",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: removeMemberSelectionChecker(namesListListbox),
        )
    removeAACMemberButton.pack(pady = standardYPadding)


def removeMemberSelectionChecker(namesListListbox):
    #Gets user selection
    rankNameSelection= namesListListbox.curselection()
    #Checks if there is not a selection
    if not rankNameSelection:
        #Creates error widnow
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

        #Runs if the user did select a name and calls a function
    else:
        AACMember(namesListListbox)


def AACMember(namesListListbox):

    #Gets userse selection
    selection = namesListListbox.curselection()

    #Gets members name and folder location
    AACMember= namesListListbox.get(selection)
    stringAACMember= str(AACMember)
    cleanStringAACMember= stringAACMember.replace("(", "").replace("'", "").replace(",", "").replace(" ", "_").replace(")", "")
    cadetID = stringAACMember.split()[0]

    #Creates new window
    areYouSureWindow= ctk.CTkToplevel(root, fg_color= "#1f1f1f")
    areYouSureWindow.title("Are You Sure")
    areYouSureWindow.geometry("1200x500")
    areYouSureWindow.transient(root)
    areYouSureWindow.lift()
    
    #Creates label
    areYouSureLabel= ctk.CTkLabel(
        areYouSureWindow,
        text= f"Are You Sure You Want To Remove {cleanStringAACMember}\n\n This Will Permanently Remove All Information For This Person",
        font= standardFont
        )
    areYouSureLabel.pack(pady= standardYPadding)

    #Creates a frame
    buttonFrame= ctk.CTkFrame(areYouSureWindow, fg_color= "#1f1f1f")
    buttonFrame.pack()

    #Creates a buttonto call a function
    yesButton= ctk.CTkButton(
        buttonFrame,
        text= "Yes",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command= lambda: removeMemberYes(cadetID,areYouSureWindow)
        )
    yesButton.pack(pady= standardYPadding, padx= 10, side='left')

    #Creates a buttonto call a function
    noButton= ctk.CTkButton(
        buttonFrame,
        text= "No",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: areYouSureWindow.destroy()
        )
    noButton.pack(pady= standardYPadding, padx= 10, side='left')


def removeMemberYes(cadetID,areYouSureWindow):

    cursor = connection.cursor()
    rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID={cadetID}").fetchall()
    rank = str(rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
    firstName = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID={cadetID}").fetchall()
    firstName = str(firstName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
    lastName = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID={cadetID}").fetchall()
    lastName = str(lastName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")

    #Deletes data from the database
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Cadets WHERE CadetID={cadetID}')
    connection.commit()
    
    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "14"
    Before= f"{rank} {firstName} {lastName}"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "Admin"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()


    #Closes window  
    areYouSureWindow.destroy()

    removeAACMemberOptions()


#--------------------------------- CHANGE ID OPTIONS -----------------------------------------------------------

def changeIDOptions():

    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creating a label
    label = ctk.CTkLabel(middleFrame, text="Select The Person You Wish To Modify", fg_color="transparent", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creating list box frame
    listboxFrame= ctk.CTkFrame(middleFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creating list box and inserting contents of database into it using SQL
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 25, height= 30, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creating a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)        

    #Creating an entry box
    newIDEntry = ctk.CTkEntry(
        middleFrame, 
        placeholder_text="Enter New Cadet ID",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    newIDEntry.pack(pady = standardYPadding)

    #Creating a button
    changeRankButton = ctk.CTkButton(
        middleFrame,
        text= "Update Rank",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: changeIDSelectionChecker(namesListListbox,newIDEntry,formatted_data),
        )
    changeRankButton.pack(pady = standardYPadding)


def changeIDSelectionChecker(namesListListbox,newIDEntry,formatted_data):
    #Getting user listbox selection
    rankNameSelection= namesListListbox.curselection()
    #Looking if there was no selection
    if not rankNameSelection:
        #Creating an error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creating a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creating a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)
    #Looking if there was a selection
    else:
        #Calling the function
        updateID(namesListListbox,newIDEntry,formatted_data)


def updateID(namesListListbox,newIDEntry,formatted_data):

    #Gets user selection
    rowSelectionRank = namesListListbox.curselection()

    #Checks if user selected an option
    if rowSelectionRank:
        #Gets all required information and turns it into usable variables
        rowIndexRank = rowSelectionRank[0]
        rowRank = formatted_data[rowIndexRank]
        rowRankString= str(rowRank)
        cadetID = rowRankString.split()[0]
        cadeNewID = newIDEntry.get()

        cursor = connection.cursor()
        rank = cursor.execute(f"SELECT Rank FROM Cadets WHERE CadetID={cadetID}").fetchall()
        rank = str(rank).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        firstName = cursor.execute(f"SELECT First_Name FROM Cadets WHERE CadetID={cadetID}").fetchall()
        firstName = str(firstName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")
        lastName = cursor.execute(f"SELECT Last_Name FROM Cadets WHERE CadetID={cadetID}").fetchall()
        lastName = str(lastName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace(" ", "").replace("[", "").replace("]", "")


        Date= datetime.datetime.now().strftime("%d/%m/%Y")
        Time= datetime.datetime.now().strftime("%H:%M:%S")
        ActionID= "15"
        Before= f"{cadetID} {rank} {firstName} {lastName}"
        After= f"{cadeNewID} {rank} {firstName} {lastName}"
        User_Input= cadeNewID
        Remarks= "Admin"
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
        connection.commit()

        #Updates rank in database using SQL
        cursor = connection.cursor()
        cursor.execute(f"UPDATE Cadets SET CadetID='{cadeNewID}' WHERE CadetID={cadetID}")
        connection.commit()

    #Calls the function
    changeIDOptions()

#-----------------------------------------------------------------------------------------------------------------

def removeStoreOptions():

    #Clear all widgits in a frame
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a ctk canvas
    canvas = ctk.CTkCanvas(middleFrame, bg= "#292929", highlightthickness=0)
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    #Creates a scroll bar
    buttonScrollbar= ctk.CTkScrollbar(middleFrame, orientation=VERTICAL, width=10, command=canvas.yview)
    buttonScrollbar.pack(side="left", fill=Y)
    canvas.configure(yscrollcommand=buttonScrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

    #Creates a ctk frame
    buttonFrame= ctk.CTkFrame(canvas, fg_color= "#292929")
    buttonFrame.pack(pady = standardYPadding)

    #Creats canvas window?
    canvas.create_window((0,0), window=buttonFrame, anchor= "nw")

    cursor = connection.cursor()
    buttonDict = {}
    data = cursor.execute("SELECT CategoryID,Category FROM Categories").fetchall()
    for item in data:

        category = item[1]

        def removeStoresAction(x=item): 
            return removeStoreTextUpdation(x)

        buttonDict[item] = ctk.CTkButton(
        buttonFrame,
        text= category,
        font= standardFont,
        width= 300,
        height= standardHeight,
        command=removeStoresAction,
        )
        buttonDict[item].pack(pady = 5)


def removeStoreTextUpdation(categoryName):
    global removeStoreCategoryID
    removeStoreCategoryID= categoryName[0]
    return removeStoreViewStores(removeStoreCategoryID)


def removeStoreViewStores(removeStoreCategoryID):
               
    #Makes variables global
    global SQLCommand
    #Saves the command to a variable
    SQLCommand = f"SELECT StoreID,Name,Size,Qty FROM Stores WHERE CategoryID={removeStoreCategoryID}"
    #Makes variables global
    global formatted_data
    #Selects data from database using SQL
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT StoreID,Name,Size,Qty FROM Stores WHERE CategoryID={removeStoreCategoryID}").fetchall()
    formatted_data = []
    for item in data:
        store_id = item[0]
        name = item[1]
        size = item[2] if item[2] is not None else 'N/A'
        qty = item[3]
        formatted_data.append(f"{store_id}, {name} {size}, {qty}")

    #Calls the function
    rightFrameWidgits()


def rightFrameWidgits():
                               
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the person you wish to remove", font= standardFont)
    label.pack(pady = standardYPadding)

    #Create frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creates list box and fills it with members names using SQL
    storesListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 30, height= 25, font= standardFont)
    for row in formatted_data:
        storesListbox.insert(END, row)
    storesListbox.pack(side=LEFT)

    #Creates scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=storesListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    storesListbox.config(yscrollcommand=listboxScrollbar.set)        

    #Creates button to call a function
    removeAACMemberButton = ctk.CTkButton(
        rightFrame,
        text= "Remove item from stores",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: removeStoreSelectionChecker(storesListbox),
        )
    removeAACMemberButton.pack(pady = standardYPadding)


def removeStoreSelectionChecker(storesListbox):
                                
    #Gets user selection
    itemSelection= storesListbox.curselection()
    #Checks if there is not a selection
    if not itemSelection:
        #Creates error widnow
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an item, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

    #Runs if the user did select a name and calls a function
    else:
        removeItem(storesListbox,itemSelection)


def removeItem(storesListbox,itemSelection):

    item= storesListbox.get(itemSelection)
    stringItem= str(item)
    cleanStringItem= stringItem.replace("(", "").replace("'", "").replace(",", "").replace(" ", "_").replace(")", "")
    StoreID = stringItem.split()[0].replace(",", "")

    #Creates new window
    areYouSureWindow= ctk.CTkToplevel(root, fg_color= "#1f1f1f")
    areYouSureWindow.title("Are You Sure")
    areYouSureWindow.geometry("1200x500")
    areYouSureWindow.transient(root)
    areYouSureWindow.lift()
    
    #Creates label
    areYouSureLabel= ctk.CTkLabel(
        areYouSureWindow,
        text= f"Are You Sure You Want To Remove {cleanStringItem}\n\n This Will Permanently Remove All Information For This Item",
        font= standardFont
        )
    areYouSureLabel.pack(pady= standardYPadding)

    #Creates a frame
    buttonFrame= ctk.CTkFrame(areYouSureWindow, fg_color= "#1f1f1f")
    buttonFrame.pack()

    #Creates a buttonto call a function
    yesButton= ctk.CTkButton(
        buttonFrame,
        text= "Yes",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: removeStoreYes(StoreID,areYouSureWindow)
        )
    yesButton.pack(pady= standardYPadding, padx= 10, side='left')

    #Creates a buttonto call a function
    noButton= ctk.CTkButton(
        buttonFrame,
        text= "No",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: areYouSureWindow.destroy()
        )
    noButton.pack(pady= standardYPadding, padx= 10, side='left')


def removeStoreYes(StoreID,areYouSureWindow):

    cursor = connection.cursor()
    oldQtyName = cursor.execute(f"SELECT Name,Size,Qty FROM Stores WHERE StoreID={StoreID}").fetchall()
    oldQtyName = str(oldQtyName).replace("(", "").replace(")", "").replace(",", "").replace("'", "").replace("[", "").replace("]", "")
    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "16"
    Before= oldQtyName
    After= "N/A"
    User_Input= "N/A"
    Remarks= "Admin"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()


    #Deletes data from the database
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Stores WHERE StoreID={StoreID}')
    connection.commit()

    areYouSureWindow.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()
    removeStoreViewStores(removeStoreCategoryID)

#-----------------------------------------------------------------------------------------------------------------

def addStoresOptions():

    #Clear all widgits in left bottom frame, middle frame and right frame
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a canvas
    canvas = ctk.CTkCanvas(middleFrame, bg= "#292929", highlightthickness=0)
    canvas.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

    #Creats scroll bar
    buttonScrollbar= ctk.CTkScrollbar(middleFrame, orientation=VERTICAL, command=canvas.yview)
    buttonScrollbar.pack(side="right", fill=Y)

    #Assigns scroll bar to the canvas
    canvas.configure(yscrollcommand=buttonScrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion= canvas.bbox("all")))

    #Creates a frame
    buttonFrame= ctk.CTkFrame(canvas, fg_color= "#292929")
    buttonFrame.pack(pady = standardYPadding)

    #Creats widnow within the canvas
    canvas.create_window((0,0), window=buttonFrame, anchor= "nw")

    cursor = connection.cursor()
    buttonDict = {}
    data = cursor.execute("SELECT CategoryID,Category FROM Categories").fetchall()
    for item in data:
                
        def action(x = item): 
            return addStoreTextUpdation(x)

        category = item[1]

        buttonDict[item] = ctk.CTkButton(
        buttonFrame,
        text= category,
        font= standardFont,
        width= 300,
        height= standardHeight,
        command=action,
        )
        buttonDict[item].pack(pady = 5)


def addStoreTextUpdation(categoryName):
                        
    categoryID = categoryName[0]
    return addStoreViewStores(categoryID)


def addStoreViewStores(categoryID):

    #Clear all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the item you wish to modify \n FORMAT = StoreID, Name, Size, Qty", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates a frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Create list box and writes the contents of the database into it
    storesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 40, height=25, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT StoreID,Name,Size,Qty FROM Stores WHERE CategoryID={categoryID}").fetchall()
    formatted_data = []
    for item in data:
        store_id = item[0]
        name = item[1]
        size = item[2] if item[2] is not None else 'N/A'
        qty = item[3]
        formatted_data.append(f"{store_id}, {name} {size}, {qty}")
    for row in formatted_data:
        storesListListbox.insert(END, row)
    storesListListbox.pack(side=LEFT)

    #Creates a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=storesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    storesListListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates an entry box
    itemNameEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Item Name",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    itemNameEntry.pack(pady = standardYPadding)

    #Creates an entry box
    itemSizeEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Item Size",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    itemSizeEntry.pack(pady = standardYPadding)

    #Creates an entry box
    itemQuantityEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Item Quantity",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        )
    itemQuantityEntry.pack(pady = standardYPadding)

    #Creates a button
    addItemButton = ctk.CTkButton(
        rightFrame,
        text= "Add Item",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: addItem(itemNameEntry,itemSizeEntry,itemQuantityEntry,categoryID),
        )
    addItemButton.pack(pady = standardYPadding)
                        

def addItem(itemNameEntry,itemSizeEntry,itemQuantityEntry,categoryID):
    itemName = itemNameEntry.get()
    itemName = itemName.replace(' ','_')
    itemSize = itemSizeEntry.get()
    itemQuantity = itemQuantityEntry.get()
    
    if itemName == '':
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("500x100")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not entered an item name",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)
    
    else:
        if itemSize != '':
            itemSize = itemSize
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO Stores (Name, CategoryID, Size, Qty) VALUES ('{itemName}','{categoryID}','{itemSize}','{itemQuantity}')")
            connection.commit()

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "17"
            Before= "N/A"
            After= f"{itemName} {itemSize} {itemQuantity}"
            User_Input= "N/A"
            Remarks= "Admin"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()


        else:
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO Stores (Name, CategoryID, Qty) VALUES ('{itemName}','{categoryID}','{itemQuantity}')")
            connection.commit()

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "17"
            Before= "N/A"
            After= f"{itemName} {itemQuantity}"
            User_Input= "N/A"
            Remarks= "Admin"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

    #Call the function
    addStoreViewStores(categoryID)

#-----------------------------------------------------------------------------------------------------------------

def adminAccountOptions():
                    
    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    changeSecretQuestion = ctk.CTkButton(
        middleFrame,
        text= "Change Secret Question",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=changeSecretQuestionOptions,
    )
    changeSecretQuestion.pack(pady = standardYPadding) 

    changePassword = ctk.CTkButton(
        middleFrame,
        text= "Change Password",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=changePasswordOptions,
    )
    changePassword.pack(pady = standardYPadding)


def changeSecretQuestionOptions():

    #Clear all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the account you wish to modify \n FORMAT = Admin Account ID, Secret Question, Secret Question Answer", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates a frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Create list box and writes the contents of the database into it
    adminAccountsListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 40, height=10, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT AccountID,Secret_Question,Secret_Question_Answer FROM Accounts WHERE Account_TypeID = 1").fetchall()
    formatted_data = []
    for item in data:
        AccountID = item[0]
        secret_Question = item[1]
        secret_Question_Answer = item[2]
        formatted_data.append(f"{AccountID}, {secret_Question}, {secret_Question_Answer}")
    for row in formatted_data:
        adminAccountsListbox.insert(END, row)
    adminAccountsListbox.pack(side=LEFT)

    #Creates a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=adminAccountsListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    adminAccountsListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates an entry box
    questionEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Replacement Question",
        font= standardFont,
        width= 500,
        height= standardHeight,
        )
    questionEntry.pack(pady = standardYPadding)

    #Creates an entry box
    questionAnswerEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Replacement Question Answer",
        font= standardFont,
        width= 500,
        height= standardHeight,
        )
    questionAnswerEntry.pack(pady = standardYPadding)

    #Creates a button
    changeQuantityButton = ctk.CTkButton(
        rightFrame,
        text= "Update Quantity",
        font= standardFont,
        width= 500,
        height= standardHeight,
        command=lambda: adminAccountUpdateQuestion(questionEntry,questionAnswerEntry,adminAccountsListbox,secret_Question_Answer,secret_Question),
        )
    changeQuantityButton.pack(pady = standardYPadding)


def adminAccountUpdateQuestion(questionEntry,questionAnswerEntry,adminAccountsListbox,secret_Question_Answer,secret_Question):
                            
    replacementQuestion= questionEntry.get()
    replacementAnswer= questionAnswerEntry.get()
    adminAccountSelection= adminAccountsListbox.curselection()
    if adminAccountSelection:

        AccountID= adminAccountsListbox.get(adminAccountSelection[0])
        AccountID= str(AccountID).split(',')[0]

        if replacementQuestion == '':

            if replacementAnswer == '':

                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates a label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "You have not entered the question or the answer",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates a button
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)
            
            else:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE Accounts SET Secret_Question_Answer='{replacementAnswer}' WHERE AccountID={AccountID}")
                connection.commit()
                changeSecretQuestionOptions()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "11"
                Before= secret_Question_Answer
                After= replacementAnswer
                User_Input= "N/A"
                Remarks= "Admin"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

        else:

            if replacementAnswer == '':
                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates a label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "You have not entered the answer",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates a button
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)

            else:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE Accounts SET Secret_Question='{replacementQuestion}' WHERE AccountID={AccountID}")
                cursor.execute(f"UPDATE Accounts SET Secret_Question_Answer='{replacementAnswer}' WHERE AccountID={AccountID}")
                connection.commit()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "10"
                Before= secret_Question
                After= replacementQuestion
                User_Input= "N/A"
                Remarks= "Admin"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                ActionID= "11"
                Before= secret_Question_Answer
                After= replacementAnswer
                User_Input= "N/A"
                Remarks= "Admin"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                changeSecretQuestionOptions()

    else:
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an account",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)


def changePasswordOptions():
                                      
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Follow the prompts to change the password", font= standardFont)
    label.pack(pady = standardYPadding)

    cursor = connection.cursor()
    data = cursor.execute(f"SELECT AccountID, Password FROM Accounts WHERE Account_TypeID = 1").fetchall()
    formatted_data = []
    for item in data:
        AccountID = item[0]
        adminAccountPassword = item[1]
        formatted_data.append(f"{AccountID}, {adminAccountPassword}")

    #Creates an entry box
    adminAccountOldPassword = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Old Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*'
        )
    adminAccountOldPassword.pack(pady = standardYPadding)

    #Creates an entry box
    adminAccountNewPassword = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter New Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*'
        )
    adminAccountNewPassword.pack(pady = standardYPadding)

    #Creates an entry box
    adminAccountNewPasswordConfirm = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter New Password Again",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*'
        )
    adminAccountNewPasswordConfirm.pack(pady = standardYPadding)

    #Creates a button
    changeQuantityButton = ctk.CTkButton(
        rightFrame,
        text= "Update Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        command=lambda: adminAccountPasswordChecker(adminAccountOldPassword,adminAccountNewPassword,adminAccountNewPasswordConfirm,adminAccountPassword,AccountID),
        )
    changeQuantityButton.pack(pady = standardYPadding)


def adminAccountPasswordChecker(adminAccountOldPassword,adminAccountNewPassword,adminAccountNewPasswordConfirm,adminAccountPassword,AccountID):

    adminOldPassword= adminAccountOldPassword.get()
    adminNewPassword= adminAccountNewPassword.get()
    adminNewPasswordConfirm= adminAccountNewPasswordConfirm.get()

    if adminOldPassword != adminAccountPassword:
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "The old account password does not much currant password",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)
        changePasswordOptions

    else:
        if adminNewPassword != adminNewPasswordConfirm:
            #Creates error window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "The new passwords do not match",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)
            changePasswordOptions

        else:
            cursor = connection.cursor()
            cursor.execute(f"UPDATE Accounts SET Password='{adminNewPasswordConfirm}' WHERE AccountID={AccountID}")
            connection.commit()

            Date= datetime.datetime.now().strftime("%d/%m/%Y")
            Time= datetime.datetime.now().strftime("%H:%M:%S")
            ActionID= "5"
            Before= adminOldPassword
            After= adminNewPasswordConfirm
            User_Input= "N/A"
            Remarks= "Admin"
            cursor = connection.cursor()
            cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
            connection.commit()

            changePasswordOptions()

#-----------------------------------------------------------------------------------------------------------------

def userAccountOptions():

    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    addUserAccountButton = ctk.CTkButton(
        middleFrame,
        text= "Add User Account",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=addUserAccount,
        )
    addUserAccountButton.pack(pady = standardYPadding)

    removeUserAccountButton = ctk.CTkButton(
        middleFrame,
        text= "Remove User Account",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=deleteUserAccountOption,
        )
    removeUserAccountButton.pack(pady = standardYPadding)

    changeSecretQuestionButton = ctk.CTkButton(
        middleFrame,
        text= "Change Secret Question",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=changeSecretQuestion,
        )
    changeSecretQuestionButton.pack(pady = standardYPadding)

    changePasswordButton = ctk.CTkButton(
        middleFrame,
        text= "Change Password",
        font= (standardFont),
        width= standardWidth,
        height= standardHeight,
        command=changeUserPassword,
        )
    changePasswordButton.pack(pady = standardYPadding)


def addUserAccount():

    for widgits in rightFrame.winfo_children():
        widgits.destroy()

    #Create frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creates list box and fills it with members names using SQL
    namesListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 30, height= 25, font= standardFont)
    cursor = connection.cursor()
    data = cursor.execute("SELECT CadetID,rank,first_name,last_name FROM Cadets").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        namesListListbox.insert(END, row)
    namesListListbox.pack(side=LEFT)

    #Creates scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=namesListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    namesListListbox.config(yscrollcommand=listboxScrollbar.set)   

    #Creates an entry box
    passwordEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Please Enter a Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*',
        )
    passwordEntry.pack(pady = standardYPadding)

    #Creates an entry box
    confirmedPasswordEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Please Enter the Password Again",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*',
        )
    confirmedPasswordEntry.pack(pady = standardYPadding)

    #Creates an entry box
    secretQuestionEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter A Secret Question",
        font= standardFont,
        width= 500,
        height= standardHeight,
        )
    secretQuestionEntry.pack(pady = standardYPadding)

    #Creates an entry box
    secretQuestionAnswerEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Secret Question Answer",
        font= standardFont,
        width= 500,
        height= standardHeight,
        )
    secretQuestionAnswerEntry.pack(pady = standardYPadding)

    #Creates a button
    addAccountButton = ctk.CTkButton(
        rightFrame,
        text= "Add Account",
        font= standardFont,
        width= 500,
        height= standardHeight,
        command=lambda: addAccount(namesListListbox,passwordEntry,confirmedPasswordEntry,secretQuestionEntry,secretQuestionAnswerEntry,formatted_data),
        )
    addAccountButton.pack(pady = standardYPadding)


def addAccount(namesListListbox,passwordEntry,confirmedPasswordEntry,secretQuestionEntry,secretQuestionAnswerEntry,formatted_data):

    rowSelection = namesListListbox.curselection()
    if rowSelection:
        rowIndex = rowSelection[0]
        row = formatted_data[rowIndex]
        cadetID= str(row).split(" ")[0]
        firstName= str(row).split(" ")[2]
        lastName= str(row).split(" ")[3]
        username= firstName+'.'+lastName
        accountType= "2"
        password= passwordEntry.get()
        confirmedPassword= confirmedPasswordEntry.get()
        secretQuestion= secretQuestionEntry.get()
        secretQuestionAnswer= secretQuestionAnswerEntry.get()

        if confirmedPassword != password:

            #Creating an error window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()
            
            #Creating a label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "Passwords do not match",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creating a button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)

        else:
            if password == "" or confirmedPassword == "" or secretQuestion == "" or secretQuestionAnswer == "":

                #Creating an error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()
                
                #Creating a label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "You have left a field empty",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creating a button
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)

            else:
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO Accounts (CadetID, Username, Password, Account_TypeID, Secret_Question, Secret_Question_Answer) VALUES ('{cadetID}','{username}','{password}','{accountType}','{secretQuestion}','{secretQuestionAnswer}')")
                connection.commit()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "6"
                Before= "N/A"
                After= f"{username} {password} {secretQuestion} {secretQuestionAnswer}"
                User_Input= "N/A"
                Remarks= "Standard_Account"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()


                addUserAccount()

    else:
        #Creating an error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creating a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected a person, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creating a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

#----------------------------------------------------------------------------------------------------------------

def deleteUserAccountOption():

    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the person you wish to remove \n FORMAT = AcountID, Rank, Name", font= standardFont)
    label.pack(pady = standardYPadding)

    #Create frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Creates list box and fills it with members names using SQL
    accountsListListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 40, height= 25, font= ("", 15))
    cursor = connection.cursor()
    data = cursor.execute("""
        SELECT Accounts.AccountID,Cadets.Rank||' '||Cadets.First_Name||' '||Cadets.Last_Name
        FROM Accounts
        INNER JOIN Cadets
        ON Accounts.CadetID = Cadets.CadetID
        WHERE Accounts.Account_TypeID=2""").fetchall()
    formatted_data = []
    for row in data:
        formatted_data.append(' '.join(map(str, row)))
    for row in formatted_data:
        accountsListListbox.insert(END, row)
    accountsListListbox.pack(side=LEFT)

    #Creates scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=accountsListListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    accountsListListbox.config(yscrollcommand=listboxScrollbar.set)        

    #Creates button to call a function
    removeAccountButton = ctk.CTkButton(
        rightFrame,
        text= "Remove Account From List",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: userSelectionChecker(accountsListListbox),
        )
    removeAccountButton.pack(pady = standardYPadding)


def userSelectionChecker(accountsListListbox):
    #Gets user selection
    accountSelection= accountsListListbox.curselection()
    #Checks if there is not a selection
    if not accountSelection:
        #Creates error widnow
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()
        
        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an account, Please try again.",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

        #Runs if the user did select a name and calls a function
    else:
        deleteAccount(accountsListListbox)


def deleteAccount(accountsListListbox):

    #Gets userse selection
    selection = accountsListListbox.curselection()

    #Gets members name and folder location
    account= accountsListListbox.get(selection)
    accountString= str(account)
    cleanStringAccount= accountString.replace("(", "").replace("'", "").replace(",", "").replace(" ", "_").replace(")", "")
    accountID = accountString.split()[0]

    #Creates new window
    areYouSureWindow= ctk.CTkToplevel(root, fg_color= "#1f1f1f")
    areYouSureWindow.title("Are You Sure")
    areYouSureWindow.geometry("1200x500")
    areYouSureWindow.transient(root)
    areYouSureWindow.lift()
    
    #Creates label
    areYouSureLabel= ctk.CTkLabel(
        areYouSureWindow,
        text= f"Are You Sure You Want To Remove {cleanStringAccount}\n\n This Will Permanently Remove The Account",
        font= standardFont
        )
    areYouSureLabel.pack(pady= standardYPadding)

    #Creates a frame
    buttonFrame= ctk.CTkFrame(areYouSureWindow, fg_color= "#1f1f1f")
    buttonFrame.pack()

    #Creates a buttonto call a function
    yesButton= ctk.CTkButton(
        buttonFrame,
        text= "Yes",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: deleteUserAccountYes(accountID,areYouSureWindow,cleanStringAccount)
        )
    yesButton.pack(pady= standardYPadding, padx= 10, side='left')

    #Creates a buttonto call a function
    noButton= ctk.CTkButton(
        buttonFrame,
        text= "No",
        font= standardFont,
        width= standardWidth,
        height= standardHeight,
        command=lambda: areYouSureWindow.destroy()
        )
    noButton.pack(pady= standardYPadding, padx= 10, side='left')


def deleteUserAccountYes(accountID,areYouSureWindow,cleanStringAccount):

    #Deletes data from the database
    cursor = connection.cursor()
    cursor.execute(f'DELETE FROM Accounts WHERE AccountID={accountID}')
    connection.commit()
    
    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "7"
    Before= cleanStringAccount
    After= "N/A"
    User_Input= "N/A"
    Remarks= "Admin"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

    #Closes window  
    areYouSureWindow.destroy()

    deleteUserAccountOption()

#-----------------------------------------------------------------------------------------------------------------

def changeSecretQuestion():

    #Clear all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the account you wish to modify \n FORMAT = Account ID, Username, Secret Question, Secret Question Answer", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates a frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Create list box and writes the contents of the database into it
    userAccountsListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 45, height=10, font=("",15))
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT AccountID,Username,Secret_Question,Secret_Question_Answer FROM Accounts WHERE Account_TypeID = 2").fetchall()
    formatted_data = []
    for item in data:
        AccountID = item[0]
        Username = item[1]
        secret_Question = item[2]
        secret_Question_Answer = item[3]
        formatted_data.append(f"{AccountID}, {Username}, {secret_Question}, {secret_Question_Answer}")
    for row in formatted_data:
        userAccountsListbox.insert(END, row)
    userAccountsListbox.pack(side=LEFT)

    #Creates a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=userAccountsListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    userAccountsListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates an entry box
    questionEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Replacement Question",
        font= standardFont,
        width= 500,
        height= standardHeight,
        )
    questionEntry.pack(pady = standardYPadding)

    #Creates an entry box
    questionAnswerEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Replacement Question Answer",
        font= standardFont,
        width= 500,
        height= standardHeight,
        )
    questionAnswerEntry.pack(pady = standardYPadding)

    #Creates a button
    changeQuantityButton = ctk.CTkButton(
        rightFrame,
        text= "Update Quantity",
        font= standardFont,
        width= 500,
        height= standardHeight,
        command=lambda: updateQuestion(questionEntry,questionAnswerEntry,userAccountsListbox,secret_Question_Answer,secret_Question),
        )
    changeQuantityButton.pack(pady = standardYPadding)


def updateQuestion(questionEntry,questionAnswerEntry,userAccountsListbox,secret_Question_Answer,secret_Question):
    replacementQuestion= questionEntry.get()
    replacementAnswer= questionAnswerEntry.get()
    userAccountSelection= userAccountsListbox.curselection()
    if userAccountSelection:

        AccountID= userAccountsListbox.get(userAccountSelection[0])
        AccountID= str(AccountID).split(',')[0]

        if replacementQuestion == '':

            if replacementAnswer == '':

                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates a label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "You have not entered the question or the answer",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates a button
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)
            
            else:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE Accounts SET Secret_Question_Answer='{replacementAnswer}' WHERE Admin_AccountID={AccountID}")
                connection.commit()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "11"
                Before= secret_Question_Answer
                After= replacementAnswer
                User_Input= "N/A"
                Remarks= "Standard_Account"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                changeSecretQuestion()

        else:

            if replacementAnswer == '':
                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates a label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "You have not entered the answer",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates a button
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)

            else:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE Accounts SET Secret_Question='{replacementQuestion}' WHERE AccountID={AccountID}")
                cursor.execute(f"UPDATE Accounts SET Secret_Question_Answer='{replacementAnswer}' WHERE AccountID={AccountID}")
                connection.commit()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "10"
                Before= secret_Question
                After= replacementQuestion
                User_Input= "N/A"
                Remarks= "Standard_Account"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                ActionID= "11"
                Before= secret_Question_Answer
                After= replacementAnswer
                User_Input= "N/A"
                Remarks= "Standard_Account"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                changeSecretQuestion()

    else:
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an account",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)

#-----------------------------------------------------------------------------------------------------------------

def changeUserPassword():

    #Clear all widgits in right frame
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    #Creates a label
    label= ctk.CTkLabel(rightFrame, text="Select the account you wish to modify \n FORMAT = Account ID, Username", font= standardFont)
    label.pack(pady = standardYPadding)

    #Creates a frame
    listboxFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    listboxFrame.pack(pady = standardYPadding)

    #Create list box and writes the contents of the database into it
    userAccountsListbox = Listbox(listboxFrame, bg= "#292929", fg= "Silver", width= 45, height=10, font=("",15))
    cursor = connection.cursor()
    data = cursor.execute(f"SELECT AccountID,Username FROM Accounts WHERE Account_TypeID = 2").fetchall()
    formatted_data = []
    for item in data:
        AccountID = item[0]
        Username = item[1]
        formatted_data.append(f"{AccountID}, {Username}")
    for row in formatted_data:
        userAccountsListbox.insert(END, row)
    userAccountsListbox.pack(side=LEFT)

    #Creates a scroll bar
    listboxScrollbar= ctk.CTkScrollbar(listboxFrame, command=userAccountsListbox.yview)
    listboxScrollbar.pack(side="right", fill=Y)
    userAccountsListbox.config(yscrollcommand=listboxScrollbar.set)

    #Creates an entry box
    userOldPasswordEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter Old Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*',
        )
    userOldPasswordEntry.pack(pady = standardYPadding)

    #Creates an entry box
    userNewPasswordEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter New Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*',
        )
    userNewPasswordEntry.pack(pady = standardYPadding)

    #Creates an entry box
    userConfirmNewPasswordEntry = ctk.CTkEntry(
        rightFrame, 
        placeholder_text="Enter New Password Again",
        font= standardFont,
        width= 500,
        height= standardHeight,
        show= '*',
        )
    userConfirmNewPasswordEntry.pack(pady = standardYPadding)

    #Creates a button
    userUpdatePasswordButton = ctk.CTkButton(
        rightFrame,
        text= "Update Password",
        font= standardFont,
        width= 500,
        height= standardHeight,
        command=lambda: userPasswordChecker(userOldPasswordEntry,userNewPasswordEntry,userConfirmNewPasswordEntry,userAccountsListbox),
        )
    userUpdatePasswordButton.pack(pady = standardYPadding)


def userPasswordChecker(userOldPasswordEntry,userNewPasswordEntry,userConfirmNewPasswordEntry,userAccountsListbox):
    userOldPassword= userOldPasswordEntry.get()
    userNewPassword= userNewPasswordEntry.get()
    userNewPasswordConfirm= userConfirmNewPasswordEntry.get()
    userAccountSelection= userAccountsListbox.curselection()

    if userAccountSelection:

        AccountID= userAccountsListbox.get(userAccountSelection[0])
        AccountID= str(AccountID).split(',')[0]
        cursor = connection.cursor()
        userAccountPassword = cursor.execute(f"SELECT Password FROM Accounts WHERE AccountID = {AccountID}").fetchall()
        userAccountPassword = str(userAccountPassword).replace("[","").replace("(","").replace("'","").replace(",","").replace(")","").replace("]","")

        if userOldPassword != userAccountPassword:
            #Creates error window
            errorWindow= ctk.CTkToplevel(root)
            errorWindow.title("Error Window")
            errorWindow.geometry("1200x500")
            errorWindow.transient(root)
            errorWindow.lift()

            #Creates a label
            errorLabel= ctk.CTkLabel(
                errorWindow,
                text= "The old account password does not match the currant password",
                font= standardFont
                )
            errorLabel.pack(pady= standardYPadding)

            #Creates a button
            errorButton= ctk.CTkButton(
                errorWindow,
                text= "Close Window",
                font= standardFont,
                width= standardWidth,
                height= standardHeight,
                command= errorWindow.destroy
                )
            errorButton.pack(pady= standardYPadding)
            changeUserPassword

        else:
            if userNewPassword != userNewPasswordConfirm:
                #Creates error window
                errorWindow= ctk.CTkToplevel(root)
                errorWindow.title("Error Window")
                errorWindow.geometry("1200x500")
                errorWindow.transient(root)
                errorWindow.lift()

                #Creates a label
                errorLabel= ctk.CTkLabel(
                    errorWindow,
                    text= "The new passwords do not match",
                    font= standardFont
                    )
                errorLabel.pack(pady= standardYPadding)

                #Creates a button
                errorButton= ctk.CTkButton(
                    errorWindow,
                    text= "Close Window",
                    font= standardFont,
                    width= standardWidth,
                    height= standardHeight,
                    command= errorWindow.destroy
                    )
                errorButton.pack(pady= standardYPadding)
                changeUserPassword

            else:
                cursor = connection.cursor()
                cursor.execute(f"UPDATE Accounts SET Password='{userNewPassword}' WHERE AccountID={AccountID}")
                connection.commit()

                Date= datetime.datetime.now().strftime("%d/%m/%Y")
                Time= datetime.datetime.now().strftime("%H:%M:%S")
                ActionID= "5"
                Before= userOldPassword
                After= userNewPassword
                User_Input= "N/A"
                Remarks= "Standard_Account"
                cursor = connection.cursor()
                cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
                connection.commit()

                changeUserPassword()
    
    else:
        #Creates error window
        errorWindow= ctk.CTkToplevel(root)
        errorWindow.title("Error Window")
        errorWindow.geometry("1200x500")
        errorWindow.transient(root)
        errorWindow.lift()

        #Creates a label
        errorLabel= ctk.CTkLabel(
            errorWindow,
            text= "You have not selected an account",
            font= standardFont
            )
        errorLabel.pack(pady= standardYPadding)

        #Creates a button
        errorButton= ctk.CTkButton(
            errorWindow,
            text= "Close Window",
            font= standardFont,
            width= standardWidth,
            height= standardHeight,
            command= errorWindow.destroy
            )
        errorButton.pack(pady= standardYPadding)


#-----------------------------------------------------------------------------------------------------------------


def viewLogsOptions():

    for widgets in middleFrame.winfo_children():
        widgets.destroy()
    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    Day= datetime.datetime.now().strftime("%d")
    Month= datetime.datetime.now().strftime("%m")
    Year= datetime.datetime.now().strftime("%Y")
    Day= int(Day)
    Month= int(Month)
    Year= int(Year)

    #Creates a label
    label= ctk.CTkLabel(middleFrame, text="Select start date", font= standardFont)
    label.pack(pady = standardYPadding)

    calOne = DateEntry(middleFrame, 
        width=20, 
        year=Year, 
        month=Month,
        background='darkblue', 
        foreground='white', 
        borderwidth=5,
        date_pattern='dd/mm/yyyy',
        font=standardFont)
    calOne.pack(padx=10, pady=10)

    #Creates a label
    label= ctk.CTkLabel(middleFrame, text="Select end date", font= standardFont)
    label.pack(pady = standardYPadding)

    calTwo = DateEntry(middleFrame, 
        width=20, 
        year=Year, 
        month=Month, 
        background='darkblue', 
        foreground='white', 
        borderwidth=5,
        date_pattern='dd/mm/yyyy',
        font=standardFont)
    calTwo.pack(padx=10, pady=10)

    #Creates a button
    getLogsButton = ctk.CTkButton(
        middleFrame,
        text= "Get Logs",
        font= standardFont,
        width= 300,
        height= standardHeight,
        command=lambda: getLogs(calOne,calTwo),
        )
    getLogsButton.pack(pady = standardYPadding)


def getLogs(calOne,calTwo):

    for widgets in rightFrame.winfo_children():
        widgets.destroy()

    calOneDate = calOne.get_date()
    calOneDate= str(calOneDate)
    year, month, day = calOneDate.split('-')
    calOneDate = f"{day}/{month}/{year}"

    calTwoDate = calTwo.get_date()
    calTwoDate= str(calTwoDate)
    year, month, day = calTwoDate.split('-')
    calTwoDate = f"{day}/{month}/{year}"

    data=[]
    cursor = connection.cursor()
    data = cursor.execute(f"""
        SELECT ActionsLogs.LogID,Accounts.Username,ActionsLogs.Date,ActionsLogs.Time,Actions.Action,ActionsLogs.Before,ActionsLogs.After,ActionsLogs.User_Input,ActionsLogs.Remarks
        FROM ActionsLogs
        LEFT JOIN Actions
        ON ActionsLogs.ActionID = Actions.ActionID
        LEFT JOIN Accounts
        ON ActionsLogs.AccountID = Accounts.AccountID
        WHERE Date BETWEEN '{calOneDate}' AND '{calTwoDate}'""").fetchall()
    
    #Create frame
    treeviewFrame= ctk.CTkFrame(rightFrame, fg_color= "#292929")
    treeviewFrame.pack()

    ttk.Style().theme_use("clam")
    ttk.Style().configure("Treeview", background="#292929",foreground="White", fieldbackground="#292929")
    ttk.Style().configure('Treeview.Heading', background='#292929', foreground='White')

    columns = ("LogID", "Username", "Date", "Time", "Action", "Before", "After", "UserInput", "Remarks")
    actionLogsTreeview = ttk.Treeview(treeviewFrame, columns=columns, show="headings", height= 40)

    actionLogsTreeview.column("# 1",anchor=W, stretch=False, width=100)
    actionLogsTreeview.heading("# 1", text="LogID")
    actionLogsTreeview.column("# 2", anchor=W, stretch=False, width=180)
    actionLogsTreeview.heading("# 2", text="Username")
    actionLogsTreeview.column("# 3", anchor=W, stretch=False, width=80)
    actionLogsTreeview.heading("# 3", text="Date")
    actionLogsTreeview.column("# 4", anchor=W, stretch=False, width=80)
    actionLogsTreeview.heading("# 4", text="Time")
    actionLogsTreeview.column("# 5", anchor=W, stretch=False, width=200)
    actionLogsTreeview.heading("# 5", text="Action")
    actionLogsTreeview.column("# 6", anchor=W, stretch=False, width=200)
    actionLogsTreeview.heading("# 6", text="Before")
    actionLogsTreeview.column("# 7", anchor=W, stretch=False, width=200)
    actionLogsTreeview.heading("# 7", text="After")
    actionLogsTreeview.column("# 8", anchor=W, stretch=False, width=200)
    actionLogsTreeview.heading("# 8", text="UserInput")
    actionLogsTreeview.column("# 9", anchor=W, stretch=False, width=200)
    actionLogsTreeview.heading("# 9", text="Remarks")
        
    for row in data:
        actionLogsTreeview.insert("", "end", values=row)

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "27"
    Before= calOneDate
    After= calTwoDate
    User_Input= "N/A"
    Remarks= "Admin"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

    #Creates scroll bar
    treeviewScrollbarY= ttk.Scrollbar(treeviewFrame, command=actionLogsTreeview.yview)
    treeviewScrollbarY.pack(side=LEFT, fill=Y)
    actionLogsTreeview.config(yscrollcommand=treeviewScrollbarY.set)
    
    actionLogsTreeview.pack(side=RIGHT)

    horizontal_scrollbar = ttk.Scrollbar(rightFrame, orient=HORIZONTAL, command=actionLogsTreeview.xview)
    horizontal_scrollbar.pack(fill="x")
    horizontal_scrollbar.configure(command=actionLogsTreeview.xview)
    actionLogsTreeview.configure(xscrollcommand=horizontal_scrollbar.set)
    
    #Creates a button
    getLogsButton = ctk.CTkButton(
        rightFrame,
        text= "Download Logs",
        font= standardFont,
        width= 300,
        height= standardHeight,
        command=lambda: downloadLogs(calOneDate,calTwoDate),
        )
    getLogsButton.pack(pady = 10)

    
def downloadLogs(calOneDate,calTwoDate):

    data=[]
    cursor = connection.cursor()
    data = cursor.execute(f"""
        SELECT ActionsLogs.LogID,Accounts.Username,ActionsLogs.Date,ActionsLogs.Time,Actions.Action,ActionsLogs.Before,ActionsLogs.After,ActionsLogs.User_Input,ActionsLogs.Remarks
        FROM ActionsLogs
        LEFT JOIN Actions
        ON ActionsLogs.ActionID = Actions.ActionID
        LEFT JOIN Accounts
        ON ActionsLogs.AccountID = Accounts.AccountID
        WHERE Date BETWEEN '{calOneDate}' AND '{calTwoDate}'""").fetchall()
    
    with open(path+"/namesList.csv", 'w', newline='') as file:
        writer = csv.writer(file)

    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Define the file name and content
    file_name = f'Action_Logs_({calOneDate}_to_{calTwoDate}).csv'

    # Create the file path
    file_path = os.path.join(downloads_folder, file_name)

    file_path=file_path.replace("/","-")

    # Write the content to the file
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

    # Get the path to the Downloads folder based on the user's operating system
    downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

    # Open the Downloads folder using the default file explorer
    os.startfile(downloads_folder)

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "28"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

    viewLogsOptions()


##################################################################################################################


def closeProgram():

    Date= datetime.datetime.now().strftime("%d/%m/%Y")
    Time= datetime.datetime.now().strftime("%H:%M:%S")
    ActionID= "2"
    Before= "N/A"
    After= "N/A"
    User_Input= "N/A"
    Remarks= "N/A"
    cursor = connection.cursor()
    cursor.execute(f"INSERT INTO ActionsLogs (AccountID,Date,Time,ActionID,Before,After,User_Input,Remarks) VALUES ('{loggedInAccountID}','{Date}','{Time}','{ActionID}','{Before}','{After}','{User_Input}','{Remarks}')").fetchall()
    connection.commit()

    #Closes database connection and the program
    with closing(sqlite3.connect("505_ACU_Q-Store_Database.db")):
        root.destroy()


##################################################################################################################


createLogInWindow()
root.mainloop()