import pymongo
import mysql.connector
import pandas as pd
import sys
from dotenv import dotenv_values
from tkinter import *
from tkinter import ttk
from crud import CRUD

# config = dotenv_values('.env')  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
# user = config['USER_MONGO']
# password = config['PASSWORD_MONGO']
# conn_string = f"mongodb+srv://{user}:{password}@cluster0.6iqrn.mongodb.net"
# client = pymongo.MongoClient(conn_string)
# tweets_db_mongo = client['tweets_db_mongo']
# tweets_col = tweets_db_mongo['tweets_col']

query_option_list = ['Search by Hashtag', 'Search by Word', 'Search by User Screen Name', 'Search by Time Range']
buttonList = []

result = []


def find_hashtag(tweets_db_mongo, hashtag):
    result.append(tweets_db_mongo.tweets_col.find({}))


def sel():
    selection = 'You selected the option to ' + query_option_list[search_choice.get() - 1]
    search_choice_label.config(text=selection, bg='sky blue')


def query():
    query = 'You have entered: ' + entry.get() + ' and we shall do thingies with ' + query_option_list[
        search_choice.get() - 1]
    user_query_label.config(text=query, bg='magenta')
    mongo_query = {'hashtags': {'$elemMatch': {'$eq': entry.get()}}}
    mongo_res = str(list(tweets_db_mongo.tweets_col.find(mongo_query)))
    user_query_label.config(text=mongo_res, bg='red')
    if search_choice.get() == 1:
        #         find_hashtag(tweets_db_mongo, entry.get())
        pass


def welcome(root):
    welcome_str = """
        Welcome to the Tweet Search Application! 
        Please choose a search option, the requested field and your query
        Example Choice 1: Radio button: "Search by Hashtag", Dropdown: "username", Entry: "sundayvibes", Then Click "Go
        Example Choice 2: Radio button: "Search by Word", Dropdown: "user_name",Entry: "Evil can not spread without followers.", Then Click "Go
        Example Choice 3: Radio button: "Search by User", Dropdown: "tweet_text",Entry: "GabiShae", Then Click "Go
        Example Choice 4: Radio button: "Search by Time Range", Dropdown: "tweet_text",Entry: "GabiShae", Then Click "Go
        NOTE: If you choose by time range, specify the start date and end date:
        Ex: "
        """
    welcome_label = Label(root, text=welcome_str, font=("Arial", 25), fg='blue')
    welcome_label.pack()

def radio_search(root):
    for i in range(len(query_option_list)):
        button = Radiobutton(root, text=query_option_list[i], variable=search_choice, value=i + 1, command=sel)
        buttonList.append(button)
        button.pack(anchor=W)

    search_choice_label = Label(root)
    search_choice_label.pack()

def entry_query(root):
    entry_label = Label(root, text='Enter your query in the box below and click "Go" to see tweets')
    entry_label.pack()
    entry = Entry()
    entry.pack()
def separator(root):
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x')


def field_dropdown(root):

def create_gui():
    root = Tk()
    root.title('Tweet Search Application')
    root.geometry('1000x1000')
    # Create text widget and specify size.
    # T = Text(root, height = 5, width = 52)
    search_choice = IntVar()
    # query_string = StringVar()





user_query_label = Label(root)
user_query_label.pack()


################################################################
def show():
    label.config(text=clicked.get())


# Dropdown menu options
dropdown_options = ['tweet_id', 'user_id', 'is_retweet', 'tweet_text', 'in_reply_to_status_id',
                    'in_reply_to_user_id', 'in_reply_to_screen_name', 'coordinates', 'place', 'quote_count',
                    'reply_count', 'retweet_count', 'favorite_count', 'hashtags', 'lang', 'timestamp_ms',
                    'user_name', 'screen_name', 'followers_count', 'listed_count', 'favourites_count', 'status_count'
                    ]

# datatype of menu text
clicked = StringVar()

# initial menu text
clicked.set('Choose option')

# Create Dropdown menu
drop = OptionMenu(root, clicked, *dropdown_options)
drop.pack()

# Create button, it will change label text
# button = Button( root , text = "click Me" , command = show ).pack()
###################################################################
go_button = Button(root, text="Go", command=query)
go_button.pack()
separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')

# scrollbar = Scrollbar(root)
# scrollbar.pack(side = RIGHT, fill = Y )

# mylist = Listbox(root, yscrollcommand = scrollbar.set )

# result = tweets_db_mongo.tweets_col.find({}, {'tweet_text':1, '_id':0}).limit(10)
# for doc in result:
#     mylist.insert(END, doc['tweet_text'])

# mylist.pack( side = LEFT, fill = BOTH )
# scrollbar.config(command = mylist.yview )

scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT)

mylist = Listbox(root, yscrollcommand=scrollbar.set)

# result = tweets_db_mongo.tweets_col.find({}, {'tweet_text':1, '_id':0}).limit(10)
for doc in result:
    mylist.insert(END, doc['tweet_text'])

mylist.pack(side=LEFT)
scrollbar.config(command=mylist.yview)

separator = ttk.Separator(root, orient='horizontal')
separator.pack(fill='x')
quit_button = Button(root, text="Quit", command=root.destroy)
quit_button.pack()

root.mainloop()

