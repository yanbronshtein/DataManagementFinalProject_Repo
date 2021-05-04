# Drivers for the 3 databases
import pymongo
import mysql.connector
import redis

import sys
from dotenv import dotenv_values
from datetime import timedelta
import datetime
import sys
from dotenv import dotenv_values
from tkinter import *
from crud_v2 import CRUD
import os

query_option_list = ['Search by Hashtag', 'Search by Word', 'Search by User Screen Name', 'Search by Time Range']
button_list = []


class GUI:
    def __init__(self, root):
        """
        This initializes the GUI application including the radio buttons for user query type, user entry box
        and the quit, go, and clear output buttons, and the output summary label
        :param root:
        """
        self.root = root
        self.root.title('Tweet Search Application')
        self.root.attributes("-fullscreen", True)  # Make full screen
        self.search_choice = IntVar()  # Global variable to save the radio button choice. One of {1,2,3,4}
        self.user_query = StringVar()  # Global variable to save the query typed by user in entry
        self.welcome()  # Create welcome label

        # Initialize the radio buttons
        for i in range(len(query_option_list)):
            button = Radiobutton(self.root, text=query_option_list[i], variable=self.search_choice, value=i + 1)
            button.pack(anchor=W)

        # Initialize the entry box
        self.entry = Entry(self.root)
        self.entry.pack()
        # Initialize the go button with the go() callback function
        go_button = Button(self.root, text="Go", command=self.go)
        go_button.pack()
        # Initialize the quit button with the command to destroy the frame and quit the search application
        quit_button = Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.pack()

        # Initialize the clear output button with the clear() callback function
        clear_output_button = Button(self.root, text="Clear output", command=self.clear)
        clear_output_button.pack()

    def welcome(self):
        """
        This function simply renders the welcome label. This is the first thing the user sees when opening
        the application
        :return: None
        """
        welcome_str = """
            Welcome to the Tweet Search Application! 
            Please choose a search option, the requested field and your query
            Example Choice 1: Radio button: "Search by Hashtag", Entry: "SundayVibes", Then Click "Go"
            
            Example Choice 2: Radio button: "Search by Word", Entry: "Evil", Then Click "Go"
            
            Example Choice 3: Radio button: "Search by User", Entry: "GenYtakeover", Then Click "Go"
            
            Example Choice 4: Radio button: "Search by Time Range", Entry: "2021-04-11 19:32:20,2021-04-11 19:32:50" 
            where the first value is the start date and the second value is the end date in UTC datetime. Make sure 
            to use a comma as a separator Then Click "Go" """
        welcome_label = Label(self.root, text=welcome_str, font=("Arial", 18), fg='blue')
        welcome_label.pack()

    def clear(self):
        """
        This function destroys the application and then restarts the application with a call to main()
        :return: None
        """
        self.root.destroy()
        main()

    def go(self):
        """
        This function works when the user selects a radio button and types in text into the entry
        The results are obtained from the global variables. An object of the CRUD class in instantiated to help
        with the backend of the application.
        Ultimately, the results of one of the four methods in CRUD methods is displayed in an output label
        :return: None
        """
        choice = self.search_choice.get()
        user_text = self.entry.get().strip()
        crud = CRUD()
        res = ""
        if choice == 1:
            res = crud.search_by_hashtag(user_text)
        elif choice == 2:
            res = crud.search_by_word(user_text)
        elif choice == 3:
            res = crud.search_by_user(user_text)
        elif choice == 4:
            try:
                lower_bound, upper_bound = user_text.split(',')  # Get start and end dates
                lower_bound = datetime.datetime.strptime(lower_bound.strip(), '%Y-%m-%d %H:%M:%S')

                upper_bound = datetime.datetime.strptime(upper_bound.strip(), '%Y-%m-%d %H:%M:%S')
                res = crud.search_by_time_range(lower_bound, upper_bound)

            except ValueError:
                res = """ERROR: the query by user <{}> threw an error because two comma separated values were not 
                provided Please clear the output and try again""".format(user_text)

        bg = 'red' if 'ERROR' in res else 'yellow'

        summary_label = Label(self.root, bg=bg, width=300, text=res)
        summary_label.pack()


def main():
    """
    This function is called as soon as someone executes this python file.
    The GUI is initialized and started
    :return: None
    """
    root = Tk()
    GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
