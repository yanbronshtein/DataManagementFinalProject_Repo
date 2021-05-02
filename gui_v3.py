import pymongo
import mysql.connector
import pandas as pd
import sys
from dotenv import dotenv_values
from tkinter import *
from tkinter import ttk
from crud import CRUD
import os

##VIP global variables


query_option_list = ['Search by Hashtag', 'Search by Word', 'Search by User Screen Name', 'Search by Time Range']
button_list = []


class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Tweet Search Application')
        # self.root.geometry('1000x1000')
        self.root.attributes("-fullscreen", True)
        self.search_choice = IntVar()
        self.user_query = StringVar()
        self.welcome()
        for i in range(len(query_option_list)):
            # button = Radiobutton(root, text=query_option_list[i], variable=search_choice, value=i+1, command=sel)
            button = Radiobutton(self.root, text=query_option_list[i], variable=self.search_choice, value=i + 1)

            # button_list.append(button)
            button.pack(anchor=W)

        self.entry = Entry(self.root)
        self.entry.pack()
        go_button = Button(self.root, text="Go", command=self.go)
        go_button.pack()

        quit_button = Button(self.root, text="Quit", command=self.root.destroy)
        quit_button.pack()
        clear_output_button = Button(self.root, text="Clear output", command=self.clear)
        clear_output_button.pack()

        #Labels
        # userinfo_label = Label(self.root, text="User Info\n")
        # userinfo_label.pack(side=LEFT)
        # tweetinfo_label = Label(self.root, text="Tweet Info\n")
        # tweetinfo_label.pack(side=LEFT)
        # tweetinfo_label.pack(side=RIGHT)

        #Tweet Info

        self.sb1 = Scrollbar(self.root)
        # self.sb1.pack(side=RIGHT, fill=Y)
        # self.tweetinfo_guiList = Listbox(self.root, yscrollcommand=self.sb1.set, width=150)
        self.tweetinfo_guiList = Listbox(self.root, yscrollcommand=self.sb1.set, bg="yellow")
        # self.tweetinfo_guiList.pack(side=LEFT)
        self.sb1.config(command=self.tweetinfo_guiList.yview)

        #User info
        self.sb2 = Scrollbar(self.root)
        # self.sb2.pack(side=RIGHT, fill=Y)
        # self.userinfo_gui_list = Listbox(self.root, yscrollcommand=self.sb2.set, width=150)
        self.userinfo_gui_list = Listbox(self.root, yscrollcommand=self.sb2.set)

        # self.userinfo_gui_list.pack(side=LEFT)
        self.sb2.config(command=self.userinfo_gui_list.yview)


    def welcome(self):
        welcome_str = """
            Welcome to the Tweet Search Application! 
            Please choose a search option, the requested field and your query
            Example Choice 1: Radio button: "Search by Hashtag", Entry: "sundayvibes", Then Click "Go"
            
            Example Choice 2: Radio button: "Search by Word", Entry: "Evil can not spread without followers.", Then Click "Go"
            
            Example Choice 3: Radio button: "Search by User", Entry: "SistaAkos", Then Click "Go"
            
            Example Choice 4: Radio button: "Search by Time Range", 
            Entry: "2018-06-29 17:08:00,2020-06-29 17:08:00" where the first value is the start date
            and the second value is the end date in UTC datetime. Make sure to use a comma as a separator Then Click "Go"
            """
        welcome_label = Label(self.root, text=welcome_str, font=("Arial", 18), fg='blue')
        welcome_label.pack()

    def clear(self):
        self.root.destroy()
        main()

    # def separator(self):
    #     separator = ttk.Separator(root, orient='horizontal')
    #     separator.pack(fill='x')

    # def merge_dicts(self, dict1, dict2):
    #     new_dict = {**dict1, **dict2}
    #     return new_dict

    def go(self):

        print("User search choice", self.search_choice.get())
        choice = self.search_choice.get()
        user_text = self.entry.get().strip()
        print("User text was", user_text)
        crud = CRUD()

        mongo_query = sql_query = sql_res = mongo_res = None
        # by hashtag
        # Find user and tweet_id. Find all matches in SQL
        global user_info_list
        global tweet_info_list
        user_info_list = []  # Store SQL user information
        tweet_info_list = [] # Store MongoDB tweet information

        if choice == 1:

            print("choice was to search by hashtag")
            mongo_query = {'hashtags': {'$elemMatch': {'$eq': user_text}}}
            doc_count = crud.get_mongo_doc_count(mongo_query)
            # print("doc_count", doc_count)
            mongo_res = crud.get_mongo(mongo_query)

            for doc in mongo_res:
                doc_dict = dict(doc)  # Get the dictionary version of this
                tweet_info_list.append(str(doc_dict) + '\n')
                sql_query = """
                SELECT * FROM user WHERE sql_tweet_id = '{}' and sql_user_id = '{}';
                """.format(doc_dict['mongo_tweet_id'], doc_dict['mongo_user_id'])
                sql_res = crud.get_mysql(sql_query)
                # the composite key of user_id and tweet_id is unique in SQL so merge_dicts() will work
                for record in sql_res:
                    user_info_list.append(str(record) + '\n')

        # by word
        elif choice == 2:
            print("choice was to search by word")

            # mongo_query = {'tweet_text': {'$regex': user_text.lower()}}
            mongo_query = {'tweet_text': {'$elemMatch': {'$eq': user_text}}}

            mongo_res = crud.get_mongo(mongo_query)
            for doc in mongo_res:
                doc_dict = dict(doc)  # Get the dictionary version of this
                tweet_info_list.append(str(doc_dict))
                sql_query = """
                        SELECT * FROM user WHERE sql_tweet_id = '{}' and sql_user_id = '{}';
                        """.format(doc_dict['mongo_tweet_id'], doc_dict['mongo_user_id'])
                sql_res = crud.get_mysql(sql_query)
                # the composite key of user_id and tweet_id is unique in SQL so merge_dicts() will work
                for record in sql_res:
                    user_info_list.append(str(record) + '\n')

        # by user
        elif choice == 3:
            print("choice was to search by user")
            sql_query = """
            SELECT * FROM user WHERE screen_name='{}';
            """.format(user_text)
            sql_res = crud.get_mysql(sql_query)
            # if len(sql_res) == 0:
            #     print("The screen_name", user_text, "does not exist")

            for record in sql_res:
                user_info_list.append(str(record) + '\n')
                mongo_query = {'mongo_tweet_id': record['sql_tweet_id'], 'mongo_user_id': record['sql_user_id']}
                mongo_res = crud.get_mongo(mongo_query)
                for doc in mongo_res:
                    doc_dict = dict(doc)  # Get the dictionary version of this

                    tweet_info_list.append(str(doc_dict) + '\n')

        # by time range
        elif choice == 4:
            start_date, end_date = user_text.split(',')  # Get start and end dates
            start_timestamp = crud.make_timestamp(start_date)
            end_timestamp = crud.make_timestamp(start_date)
            mongo_query = {"created_date": {"$gte": start_timestamp, "$lt": end_timestamp}}
            mongo_res = crud.get_mongo(mongo_query)
            for doc in mongo_res:
                doc_dict = dict(doc)  # Get the dictionary version of this
                tweet_info_list.append(str(doc_dict))
                sql_query = """
                        SELECT * FROM user WHERE sql_tweet_id = '{}' and sql_user_id = '{}';
                        """.format(doc_dict['mongo_tweet_id'], doc_dict['mongo_user_id'])
                sql_res = crud.get_mysql(sql_query)
                # the composite key of user_id and tweet_id is unique in SQL so merge_dicts() will work
                for record in sql_res:
                    user_info_list.append(str(record) + '\n')


        # sql_res = crud.get_mysql(sql_query)
        #
        #
        # print("Type SQLres", type(sql_res))
        # print("Type mongores", type(mongo_res))

        # # print(res)
####################################################################
        self.tweetinfo_guiList = Listbox(self.root, yscrollcommand=self.sb1.set, bg="yellow", width=75)
        self.sb1.config(command=self.tweetinfo_guiList.yview)
        for row in tweet_info_list:
            self.tweetinfo_guiList.insert(END, str(row))

        self.tweetinfo_guiList.pack(side=LEFT)
        self.sb1.pack(side=LEFT, fill=Y)
        self.sb1.config(command=self.tweetinfo_guiList.yview)


        # User info
        self.sb2 = Scrollbar(self.root)
        self.userinfo_gui_list = Listbox(self.root, yscrollcommand=self.sb2.set, bg="light blue", width=75)

        # self.userinfo_gui_list.pack(side=LEFT)
        self.sb2.config(command=self.userinfo_gui_list.yview)
        for row in user_info_list:
            self.userinfo_gui_list.insert(END, str(row))

        self.userinfo_gui_list.pack(side=LEFT)
        self.sb2.pack(side=LEFT, fill=Y)

        self.sb2.config(command=self.userinfo_gui_list.yview)
#####################################################################





    # root.update_idletasks()
    #


# def scrollbar(root):
#     sb = Scrollbar(root)
#     sb.pack(side=RIGHT, fill=Y)
#     crud = CRUD()
#     mongo_query = {'hashtags': {'$elemMatch': {'$eq': 'sundayvibes'}}}
#     # res = list(crud.get_mongo(query=mongo_query))
#     res = crud.get_mongo(mongo_query)
#
#     mylist = Listbox(root, yscrollcommand=sb.set, width=300)
#     # print(res)
#     for doc in res:
#         mylist.insert(END, str(dict(doc)))
#
#     mylist.pack(side=LEFT)
#     sb.config(command=mylist.yview)


# # print(res)


# mylist.pack(side=LEFT)
# sb.config(command=mylist.yview)
def main():
    root = Tk()
    app = GUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
