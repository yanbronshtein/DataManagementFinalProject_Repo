import pymongo
import mysql.connector
import pandas as pd
import sys
from dotenv import dotenv_values
from tkinter import *
from tkinter import ttk
from crud import CRUD

##VIP global variables


# config = dotenv_values('.env')  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
# user = config['USER_MONGO']
# password = config['PASSWORD_MONGO']
# conn_string = f"mongodb+srv://{user}:{password}@cluster0.6iqrn.mongodb.net"
# client = pymongo.MongoClient(conn_string)
# tweets_db_mongo = client['tweets_db_mongo']
# tweets_col = tweets_db_mongo['tweets_col']

query_option_list = ['Search by Hashtag', 'Search by Word', 'Search by User Screen Name', 'Search by Time Range']
button_list = []

result = []


# def find_hashtag(tweets_db_mongo, hashtag):
#     result.append(tweets_db_mongo.tweets_col.find({}))


def query():

    # query = 'You have entered: ' + entry.get() + ' and we shall do thingies with ' + query_option_list[
    #     search_choice.get() - 1]
    # user_query_label.config(text=query, bg='magenta')
    # print(entry.get())
    crud = CRUD()
    # mongo_query = {'hashtags': {'$elemMatch': {'$eq': entry.get()}}}
    mongo_query = {'hashtags': {'$elemMatch': {'$eq': 'sundayvibes'}}}

    res = crud.get_mongo(query=mongo_query)

    # text = tkinter.scrolledtext.ScrolledText(root)
    # text.pack()
    # mongo_res = str(list(tweets_db_mongo.tweets_col.find(mongo_query)))
    # user_query_label.config(text=mongo_res, bg='red')
    # return res
    # if search_choice.get() == 1:
    #     #         find_hashtag(tweets_db_mongo, entry.get())
    #     pass


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
    welcome_label = Label(root, text=welcome_str, font=("Arial", 18), fg='blue')
    welcome_label.pack()








def separator(root):
    separator = ttk.Separator(root, orient='horizontal')
    separator.pack(fill='x')


def field_dropdown(root):
    # Dropdown menu options
    dropdown_options = ['tweet_id', 'user_id', 'is_retweet', 'tweet_text', 'in_reply_to_status_id',
                        'in_reply_to_user_id', 'in_reply_to_screen_name', 'coordinates', 'place', 'quote_count',
                        'reply_count', 'retweet_count', 'favorite_count', 'hashtags', 'lang', 'timestamp_ms',
                        'user_name', 'screen_name', 'followers_count', 'listed_count', 'favourites_count',
                        'status_count'
                        ]

    # datatype of menu text

    # initial menu text
    clicked.set('Choose field to display')

    # Create Dropdown menu
    drop = OptionMenu(root, clicked, *dropdown_options)
    drop.pack()


def go():
    print("User search choice", search_choice.get())
    choice = search_choice.get()
    user_text = entry.get().strip()
    print("User text was", user_text)
    crud = CRUD()

    res = None
    mongo_query = None
    if choice == 1:
        print("choice was to search by hashtag")
        mongo_query = {'hashtags': {'$elemMatch': {'$eq': user_text}}}
    elif choice == 2:
        print("choice was to search by word")

        mongo_query = {'tweet_text': {'$regex': user_text.lower()}}
    elif choice == 3:
        print("choice was to search by user")
        sql_query = "SELECT * FROM users WHERE screen_name=user_text;"
        crud.get_mysql(sql_query)

    else:
        pass


    res = crud.get_mongo(query=mongo_query)




def scrollbar(root):
    sb = Scrollbar(root)
    sb.pack(side=RIGHT, fill=Y)
    crud = CRUD()
    mongo_query = {'hashtags': {'$elemMatch': {'$eq': 'sundayvibes'}}}
    # res = list(crud.get_mongo(query=mongo_query))
    res = crud.get_mongo(mongo_query)
    mylist = Listbox(root, yscrollcommand=sb.set, width=300)
    # print(res)
    for doc in res:
        mylist.insert(END, str(dict(doc)))

    mylist.pack(side=LEFT)
    sb.config(command=mylist.yview)


def quit(root):
    quit_button = Button(root, text="Quit", command=root.destroy)
    quit_button.pack()


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


# radio(root)
# entry(root)
print()
# field_dropdown(root)
# go(root)
go_button = Button(root, text="Go", command=go)
go_button.pack()

entry = Entry(root)
entry.pack()
quit(root)

# scrollbar(root)
# Create text widget and specify size.
# T = Text(root, height = 5, width = 52)
# search_choice = IntVar()
# query_string = StringVar()

# user_query_label = Label(root)
# user_query_label.pack()

root.mainloop()
