import pymongo
import mysql.connector
import pandas as pd
import sys
from dotenv import dotenv_values
from tkinter import *
from tkinter import ttk
from crud import CRUD

##VIP global variables


query_option_list = ['Search by Hashtag', 'Search by Word', 'Search by User Screen Name', 'Search by Time Range']
button_list = []

def welcome(root):
    welcome_str = """
        Welcome to the Tweet Search Application! 
        Please choose a search option, the requested field and your query
        Example Choice 1: Radio button: "Search by Hashtag", Dropdown: "username", Entry: "sundayvibes", Then Click "Go
        Example Choice 2: Radio button: "Search by Word", Dropdown: "user_name",Entry: "Evil can not spread without followers.", Then Click "Go
        Example Choice 3: Radio button: "Search by User", Dropdown: "tweet_text",Entry: "SistaAkos", Then Click "Go
        REDO:::Example Choice 4: Radio button: "Search by Time Range", Dropdown: "tweet_text",Entry: "GabiShae", Then Click "Go
        NOTE: If you choose by time range, specify the start date and end date:
        Ex: "
        """
    welcome_label = Label(root, text=welcome_str, font=("Arial", 18), fg='blue')
    welcome_label.pack()








def separator(root):
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x')



def merge_dicts(dict1, dict2):
    new_dict = {**dict1, **dict2}
    return new_dict
def go():

    print("User search choice", search_choice.get())
    choice = search_choice.get()
    user_text = entry.get().strip()
    print("User text was", user_text)
    crud = CRUD()

    mongo_query = sql_query = sql_res = mongo_res = None
    #by hashtag
    #Find user and tweet_id. Find all matches in SQL
    global display_list
    display_list = []  # list of dictionaries

    if choice == 1:

        print("choice was to search by hashtag")
        mongo_query = {'hashtags': {'$elemMatch': {'$eq': user_text}}}
        mongo_res = crud.get_mongo(mongo_query)
        for doc in mongo_res:
            doc_dict = dict(doc) #Get the dictionary version of this
            sql_query = """
            SELECT * FROM user WHERE tweet_id = '{}' and user_id = '{}';
            """.format(doc_dict['tweet_id'], doc_dict['user_id'])
            sql_res = crud.get_mysql(sql_query)
            #the composite key of user_id and tweet_id is unique in SQL so merge_dicts() will work
            for record in sql_res:
                display_list.append(merge_dicts(doc_dict, record))

    #by word
    elif choice == 2:
        print("choice was to search by word")

        mongo_query = {'tweet_text': {'$regex': user_text.lower()}}
        mongo_res = crud.get_mongo(mongo_query)
        for doc in mongo_res:
            doc_dict = dict(doc)  # Get the dictionary version of this
            sql_query = """
                    SELECT * FROM user WHERE tweet_id = '{}' and user_id = '{}';
                    """.format(doc_dict['tweet_id'], doc_dict['user_id'])
            sql_res = crud.get_mysql(sql_query)
            # the composite key of user_id and tweet_id is unique in SQL so merge_dicts() will work
            for record in sql_res:
                display_list.append(merge_dicts(doc_dict, record))

    #by user
    elif choice == 3:
        print("choice was to search by user")
        sql_query = """
        SELECT * FROM user WHERE screen_name='{}';
        """.format(user_text)
        sql_res = crud.get_mysql(sql_query)
        if len(sql_res) == 0:
            # print(f"The screen_name {} does not exist".format(user_text))
            print("The screen_name", user_text, "does not exist")

        for record in sql_res:
            mongo_query = {'tweet_id': record['tweet_id'], 'user_id': record['user_id']}
            mongo_res = crud.get_mongo(mongo_query)
            for doc in mongo_res:
                display_list.append(merge_dicts(dict(doc), record))


    #by time range
    else:
        print("YO we in da outskirts")

    # mongo_res = crud.get_mongo(mongo_query)
    # print(mongo_res)
    # sql_res = crud.get_mysql(sql_query)
    #
    #
    # print("Type SQLres", type(sql_res))
    # print("Type mongores", type(mongo_res))

    sb = Scrollbar(root)
    sb.pack(side=RIGHT, fill=Y)
    global mylist
    mylist = Listbox(root, yscrollcommand=sb.set, width=300)
    # # print(res)
    

    for row in display_list:
        mylist.insert(END, str(row))

    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)
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


def quit(root):
    quit_button = Button(root, text="Quit", command=root.destroy)
    quit_button.pack()
def clear():
    print("Whats my search choice", search_choice.get())
    mylist.delete(0, END)


root = Tk()
root.title('Tweet Search Application')
root.geometry('1000x1000')
welcome(root)
search_choice = IntVar()
user_query = StringVar()
for i in range(len(query_option_list)):
    # button = Radiobutton(root, text=query_option_list[i], variable=search_choice, value=i+1, command=sel)
    button = Radiobutton(root, text=query_option_list[i], variable=search_choice, value=i+1)

    button_list.append(button)
    button.pack(anchor=W)



go_button = Button(root, text="Go", command=go)
go_button.pack()


entry = Entry(root)
entry.pack()
clear_output_button = Button(root, text="Clear output", command=clear)
clear_output_button.pack()
quit(root)

# # print(res)




# mylist.pack(side=LEFT)
# sb.config(command=mylist.yview)

root.mainloop()
