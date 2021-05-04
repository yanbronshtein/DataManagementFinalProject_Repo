import pymongo
import mysql.connector
import sys
from dotenv import dotenv_values
import pandas as pd
# import datetime
import fontstyle
import time
import redis
from datetime import timedelta
import datetime


class CRUD:

    def __init__(self):
        """
        This constructor creates an object that will be used to perform all read operations by the Tkinter GUI
        on three databases: MongoDB, MySQL, and Redis
        """
        config = dotenv_values('.env')  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
        # MongoDB connection
        user = config['USER_MONGO']
        password = config['PASSWORD_MONGO']
        conn_string = f"mongodb+srv://{user}:{password}@cluster0.6iqrn.mongodb.net"
        client = pymongo.MongoClient(conn_string)
        tweets_db_mongo = client['tweets_db_mongo']
        tweets_col = tweets_db_mongo['tweets_col']
        self.tweets_db_mongo = tweets_db_mongo

        # MySQL connection
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

        # REDIS connection
        self.redis_client = redis.Redis(host='localhost', port='6379', decode_responses=True)

    def search_helper(self, user_text: str, redis_key: str, mongo_query: dict) -> str:
        """
        This helper method is used for the Search By Hashtag and Search by Word methods
        to process the combination of search choice and text entered by the user to produce a string output.
        If the combination exists in the cache, that result is outputed. Else the required databases are
        queried and the summary is saved in the redis cache for the next time an identical combination is provided
        :param user_text: Text entered by user in the GUI
        :param redis_key: Key of the format choice:user_text where choice belongs to {1,2} and user_text is anything
        :param mongo_query: Dictionary format query to be executed by MongoDB
        :return: Output text to be displayed by Tkinter GUI
        """
        summary = ""
        start_time = time.time()

        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:

            msg1 = "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            msg2 = "Summary generation time:" + elapsed_time_ms
        else:
            msg1 = "Not found in redis cache. Generating summary from DB and updating cache"
            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query).sort("followers_count", -1)  #
            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            top_3_tweets = ""
            count_docs = 0
            i = 0
            for doc in my_doc:
                count_docs += 1

                if doc['is_retweet']:
                    num_retweets += 1
                if i < 3:
                    top_3_tweets += str(doc) + '\n'
                i += 1

            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return """ERROR: the query by word/hashtag <{}> threw an error. 
                                    Please clear the output and try again""".format(user_text)

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'

            msg2 = "Summary generation time:" + elapsed_time_ms

            summary += """
                    Total tweets: {}

                    Number of unique users with hashtag: {}

                    Percent Retweets: {}

                    Top 3 Tweets of the Day : {}           
                    """.format(count_docs, num_unique_users, percent_retweets, top_3_tweets)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)
        return msg1 + summary + msg2

    def search_by_hashtag(self, user_text: str) -> str:
        """
        This method is called when the user chooses to search by hashtag.
        The method creates a query to search in two lists of hashtags(retweet and tweet tags)
        It then calls the search_helper() to complete the rest of the steps
        :param user_text: Text entered by user in the GUI
        :return: Output text to be displayed by Tkinter GUI
        """
        mongo_query = {"$or": [{'original_hash': {'$elemMatch': {'$eq': user_text}}},
                               {'retweet_hash': {'$elemMatch': {'$eq': user_text}}}]}

        redis_key = """{}:{}""".format(1, user_text)
        return self.search_helper(user_text, redis_key, mongo_query)

    def search_by_word(self, user_text: str) -> str:
        """
        This method is called when the user chooses to search by word.
        The method creates a query to search in both tweet and retweet text for a match using regex
        It then calls the search_helper() to complete the rest of the steps
        :param user_text: Text entered by user in the GUI
        :return: Output text to be displayed by Tkinter GUI
        """
        mongo_query = {'$or': [{'tweet_text': {'$regex': user_text}}, {'retweet_text': {'$regex': user_text}}]}

        redis_key = """{}:{}""".format(2, user_text)
        return self.search_helper(user_text, redis_key, mongo_query)

    def search_by_user(self, user_text: str) -> str:
        """
        This method is used for the Search By User to process the combination of search choice and text entered by the
        user to produce a string output.
        If the combination exists in the cache, that result is outputed. Else the required databases are
        queried and the summary is saved in the redis cache for the next time an identical combination is provided
        :param user_text: Text entered by user in the GUI.
        This is the only method that requires a MySQL query to extract the matching screen_name to get the user_id
        to search MongoDB with
        :return: Output text to be displayed by Tkinter GUI
        """
        try:
            sql_query = """SELECT sql_user_id FROM user WHERE screen_name = '{}';""".format(user_text)
            self.mysql_cursor.execute(sql_query)
            sql_user_id = self.mysql_cursor.fetchone()

            mongo_query = {'user_id': sql_user_id['sql_user_id']}
            redis_key = """{}:{}""".format(3, user_text)
        except TypeError:
            return """ERROR: the query by user <{}> threw an error.
                                        Please clear the output and try again""".format(user_text)
        summary = ""
        start_time = time.time()

        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:

            msg1 = "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            msg2 = "Summary generation time:" + elapsed_time_ms
        else:
            msg1 = "Not found in redis cache. Generating summary from DB and updating cache"
            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query).sort("followers_count", -1)  #
            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            top_3_tweets = ""
            count_docs = 0
            i = 0
            for doc in my_doc:
                count_docs += 1
                if i < 3:
                    top_3_tweets += str(doc) + '\n'
                if doc['is_retweet']:
                    num_retweets += 1
                i += 1
            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return """ERROR: the query by user <{}> threw an error.
                            Please clear the output and try again""".format(user_text)

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            msg2 = "Summary generation time:" + elapsed_time_ms
            summary = """
            Total tweets: {}

            Number of unique users with hashtag: {}

            Percent Retweets: {}

            Top 3 Tweets of the Day : {}
            
                       
            """.format(count_docs, num_unique_users, percent_retweets, top_3_tweets)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)

        return msg1 + summary + msg2

    def search_by_time_range(self, lower_bound: datetime.datetime, upper_bound: datetime.datetime) -> str:


        # upper_bound = datetime.datetime.now()
        mongo_query = {"created_date": {"$gte": lower_bound, "$lt": upper_bound}}
        redis_key = """{}:{}""".format(4, str(lower_bound) + ',' + str(upper_bound))
        summary = ""
        start_time = time.time()
        # elapsed_time_ms = ''
        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:
            msg1 = "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            msg2 = "Summary generation time:" + elapsed_time_ms
        else:

            msg1 = "Not found in redis cache. Generating summary from DB and updating cache"

            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query).sort("followers_count", -1)

            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            top_3_tweets = ""
            count_docs = 0
            i = 0
            for doc in my_doc:
                count_docs += 1
                if i < 3:
                    top_3_tweets += str(doc) + '\n'
                if doc['is_retweet']:
                    num_retweets += 1
                i += 1

            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return """ERROR: The query by time range with lower bound <{}> and upper bound <{}> threw an error.
                            Please clear the output and try again""".format(lower_bound, upper_bound)

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            msg2 = "Summary generation time:" + elapsed_time_ms
            summary = """
            Total tweets: {}

            Number of unique users with hashtag: {}

            Percent Retweets: {}

            Top 3 Tweets of the Day : {}           
            """.format(count_docs, num_unique_users, percent_retweets, top_3_tweets)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)

        return msg1 + summary + msg2
