# # import redis
# import pymongo
# import mysql.connector
# import pandas as pd
# import json
# import tweepy
# import sys
# from dotenv import dotenv_values
#
# config = dotenv_values(".env")  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
#
#
# user = config['USER_MONGO']
# password = config['PASSWORD_MONGO']
# conn_string = f"mongodb+srv://{user}:{password}@cluster0.6iqrn.mongodb.net"
# client = pymongo.MongoClient(conn_string)
# dbnames = client.list_database_names()
# if "tweets_db_mongo" in dbnames:
#     print("db exists. Will be deleted...")
#     client.drop_database("tweets_db_mongo")
# tweets_db_mongo = client["tweets_db_mongo"]
# col_names = tweets_db_mongo.list_collection_names()
# if "tweets_col" in col_names:
#     print("Tweets Collection exists. Will be deleted...")
#     tweets_db_mongo.tweets_col.drop()
# tweets_col = tweets_db_mongo["tweets_col"]
#
#
# print(pd.DataFrame(tweets_db_mongo.tweets_col.index_information()))

unfiltered_hash_tags = [{"text": "BTSARMY", "indices": [42, 50]},
                        {"text": "BestFanArmy", "indices": [55, 67]},
                        {"text": "iHeartAwards", "indices": [80, 93]}]
filtered_hash_tags = list(map(lambda x: x["text"],unfiltered_hash_tags))

print(filtered_hash_tags)