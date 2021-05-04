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
        ##MongoDB
        config = dotenv_values('.env')  # config = {"USER": "foo", "EMAIL": "foo@example.org"}
        user = config['USER_MONGO']
        password = config['PASSWORD_MONGO']
        conn_string = f"mongodb+srv://{user}:{password}@cluster0.6iqrn.mongodb.net"
        # client = pymongo.MongoClient("mongodb://localhost:27017/")
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

        ##REDIS

        self.redis_client = redis.Redis(host='localhost', port='6379', decode_responses=True)
        self.redis_client.flushdb()


    def search_by_hashtag(self, user_text):

        mongo_query = {"$or": [{'original_hash': {'$elemMatch': {'$eq': user_text}}},
                               {'retweet_hash': {'$elemMatch': {'$eq': user_text}}}]}

        redis_key = """{}:{}""".format(1, user_text)
        summary = ""
        start_time = time.time()
        elapsed_time_ms = ''
        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:

            summary += "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
        else:
            summary += "Not found in redis cache. Generating summary from DB and updating cache"
            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query).sort("followers_count", -1)  #
            # count_docs = self.tweets_db_mongo.tweets_col.count_documents(mongo_query)
            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            tweet_sample = ""
            count_docs = 0
            for doc in my_doc:
                count_docs += 1
                if doc['is_retweet']:
                    num_retweets += 1
                else:
                    tweet_sample = doc['tweet_text']
            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return ("""ERROR: the query by hashtag {} threw an error. 
                            "Please clear the output and try again""".format(user_text), "")

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            summary = """
            Total tweets: {}
    
            Number of unique users with hashtag: {}
    
            Percent Retweets: {}
            
            Tweet Of the Day: {}           
            """.format(count_docs, num_unique_users, percent_retweets, tweet_sample)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)

        return (summary, elapsed_time_ms)

    def search_by_word(self, user_text):

        mongo_query = {"$or": [{"tweet_text": {"$regex": user_text}}, {"retweet_text": {"$regex": user_text}}]}

        redis_key = """{}:{}""".format(2, user_text)
        summary = ""
        start_time = time.time()
        elapsed_time_ms = ''
        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:

            summary += "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
        else:
            summary += "Not found in redis cache. Generating summary from DB and updating cache"
            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query).sort("followers_count", -1)  #
            # count_docs = self.tweets_db_mongo.tweets_col.count_documents(mongo_query)
            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            tweet_sample = ""
            count_docs = 0
            for doc in my_doc:
                count_docs += 1
                if doc['is_retweet']:
                    num_retweets += 1
                else:
                    tweet_sample = doc['tweet_text']
            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return ("""ERROR: the query by word {} threw an error. 
                            "Please clear the output and try again""".format(user_text), "")

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            summary = """
            Total tweets: {}

            Number of unique users with hashtag: {}

            Percent Retweets: {}

            Tweet Of the Day: {}           
            """.format(count_docs, num_unique_users, percent_retweets, tweet_sample)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)

        return (summary, elapsed_time_ms)

    def search_by_user(self, user_text):
        # Sql query first

        sql_query = """SELECT sql_user_id FROM user WHERE screen_name = '{}';""".format(user_text)
        self.mysql_cursor.execute(sql_query)
        sql_user_id = self.mysql_cursor.fetchone()

        mongo_query = {'user_id': sql_user_id['sql_user_id']}
        redis_key = """{}:{}""".format(3, user_text)
        summary = ""
        start_time = time.time()
        elapsed_time_ms = ''
        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:

            summary += "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
        else:
            summary += "Not found in redis cache. Generating summary from DB and updating cache"
            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query).sort("followers_count", -1)  #
            # count_docs = self.tweets_db_mongo.tweets_col.count_documents(mongo_query)
            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            tweet_sample = ""
            count_docs = 0
            for doc in my_doc:
                count_docs += 1
                if doc['is_retweet']:
                    num_retweets += 1
                else:
                    tweet_sample = doc['tweet_text']
            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return ("""ERROR: the query by user {} threw an error.
                            "Please clear the output and try again""".format(user_text), "")

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            summary = """
            Total tweets: {}

            Number of unique users with hashtag: {}

            Percent Retweets: {}

            Tweet Of the Day: {}
            """.format(count_docs, num_unique_users, percent_retweets, tweet_sample)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)

        return (summary, elapsed_time_ms)

    def search_by_time_range(self, lower_bound, upper_bound):

        # upper_bound = datetime.datetime.now()
        mongo_query = {"created_date": {"$gte": lower_bound, "$lt": upper_bound}}
        print(mongo_query)
        redis_key = """{}:{}""".format(4, str(lower_bound) + ',' + str(upper_bound))
        summary = ""
        start_time = time.time()
        elapsed_time_ms = ''
        if self.redis_client.exists(redis_key) > 0 and self.redis_client.ttl(redis_key) > 0:
            summary += "Found in redis cache. Generating summary write away"
            summary += self.redis_client.get(redis_key)
            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
        else:

            summary += "Not found in redis cache. Generating summary from DB and updating cache"
            # my_doc = self.tweets_db_mongo.tweets_col.find_one(mongo_query).sort("followers_count", -1)
            # my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query)
            # my_doc = self.tweets_db_mongo.tweets_col.find_one(mongo_query) #works wtf
            my_doc = self.tweets_db_mongo.tweets_col.find(mongo_query)

            # for doc in my_doc:
            #     print(dict(my_doc))
            # # count_docs = self.tweets_db_mongo.tweets_col.count_documents(mongo_query)
            num_unique_users = len(self.tweets_db_mongo.tweets_col.distinct('user_id', mongo_query))

            num_retweets = 0
            tweet_sample = ""
            count_docs = 0
            for doc in my_doc:
                count_docs += 1
                if doc['is_retweet']:
                    num_retweets += 1
                    tweet_sample = doc['retweet_text']

                else:
                    tweet_sample = doc['retweet_text']
            print("sample yo", tweet_sample)

            try:
                percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'
            except ZeroDivisionError:
                return ("""ERROR: the time query with lower bound {} and upper bound {} threw an error.
                            Please clear the output and try again""".format(lower_bound, upper_bound), "")

            end_time = time.time()
            elapsed_time = end_time - start_time

            elapsed_time_ms = str(round(elapsed_time * 1000)) + 'ms'
            summary = """
            Total tweets: {}

            Number of unique users with hashtag: {}

            Percent Retweets: {}

            Tweet Of the Day: {}           
            """.format(count_docs, num_unique_users, percent_retweets, tweet_sample)
            self.redis_client.setex(redis_key, time=timedelta(minutes=15), value=summary)

        return (summary, elapsed_time_ms)
