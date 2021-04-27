import pymongo
import mysql.connector
import sys
from dotenv import dotenv_values
import pandas as pd


class CRUD:

    def __init__(self):
        ##MongoDB
        config = dotenv_values('.env')  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
        user = config['USER_MONGO']
        password = config['PASSWORD_MONGO']
        conn_string = f"mongodb+srv://{user}:{password}@cluster0.6iqrn.mongodb.net"
        client = pymongo.MongoClient(conn_string)
        tweets_db_mongo = client['tweets_db_mongo']
        tweets_col = tweets_db_mongo['tweets_col']
        self.tweets_db_mongo = tweets_db_mongo
        ##MySQL

        properties = {
            'user': config['USER_SQL'],
            'password': config['PASSWORD_SQL'],
            'host': 'localhost',
            'database': 'tweets_db_sql',
            'raise_on_warnings': True,
        }
        self.mysql_conn = mysql.connector.connect(**properties)
        self.mysql_conn.autocommit = True
        self.mysql_cursor = self.mysql_conn.cursor(dictionary=True)

    def get_mysql(self, query):
        self.mysql_cursor.execute(query)
        result = self.mysql_cursor.fetchall()

        return result
        # for record in result:
        #     print(record)

        # self.mysql_cursor.close()
        # self.mysql_conn.close()

        # sys.exit(0)

    def get_mongo(self, query):
        return self.tweets_db_mongo.tweets_col.find(query)
        # print(self.tweets_db_mongo.tweets_col.find_one())
        # temp = self.tweets_db_mongo.tweets_col.find(query)

        # new_temp = self.tweets_db_mongo.tweets_col.find(
        #     { 'hashtags': {'$elemMatch':{ '$eq':'sundayvibes'} } }
        # )


        # return pd.DataFrame(self.tweets_db_mongo.tweets_col.find_one()).to_string()
    def make_timestamp(self, date_str):
        """:arg date_str Date String formatted as MM/DD/YYYY"""
        # date_string = "11/22/2019"
        date = datetime.datetime.strptime(date_str, "%m/%d/%Y")
        time_tuple = date.timetuple()
        timestamp = time.mktime(time_tuple)
        return timestamp




