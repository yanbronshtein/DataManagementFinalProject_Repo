import pymongo
import mysql.connector
import sys
from dotenv import dotenv_values
import pandas as pd
import datetime
import fontstyle
import time
import redis
from datetime import timedelta


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

    def hashtag(self, user_text):

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

            percent_retweets = str(round((float(num_retweets / count_docs) * 100), 2)) + '%'

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

    def time_range(self, lower_bound, upper_bound):
        try:
            lower_bound = str(lower_bound)
            upper_bound = str(upper_bound)
            upper_bound = "2021-04-26 14:12:19"
            my_query = {"time": {"$gte": lower_bound, "$lt": upper_bound}}
            my_doc = self.tweets_db_mongo.tweets_col.find(my_query).sort("followers", -1)

            tweets_cnt = self.tweets_db_mongo.tweets_col.count_documents(my_query)
            dist_users = len(tweets_col.distinct('user_id', my_query))

            # num_tweeters = 0
            num_retweeters = 0

            # ave_query =([{"$group": {"_id":'null', "average": {"$avg":"$followers"} } }])

            p = 1
            avg = 0
            for i in my_doc:
                avg = avg + i['followers']
                p += 1

            avg_follow = round(avg / p, 0)
            my_doc = tweets_col.find(my_query).sort("followers", -1)

            text = fontstyle.apply('SUMMARY STATISTICS:', 'bold/white/black_BG')

            summary = """
            Number of tweets: {}
    
            Number of users who posted within the time range : {}
    
            Average no. of followers for the users who tweeted: {}
    
            """.format(tweets_cnt, dist_users, avg_follow)

            twt_head = fontstyle.apply('2 Tweets from the most followed people ', 'bold/white/black_BG')

            tweet = """"
    
            1.{}
    
            2.{}""".format(my_doc[0]['text'], my_doc[1]['text'])

            print(text, summary, twt_head, tweet)
        except:
            error = fontstyle.apply('Use alternate search criteria', 'bold/white/black_BG')
            print(error)

    def word(self, user_text):
        try:
            myquery = {"$or": [{"text": {"$regex": user_text}}, {"rtwt_text": {"$regex": user_text}}]}
            mydoc = tweets_col.find(myquery).sort("followers", -1)

            tweets_cnt = tweets_col.count_documents(myquery)
            dist_users = len(tweets_col.distinct('user_id', myquery))

            ########################avg query########################################
            num_tweets
            num_retweets

            # ave_query =([{"$group": {"_id":'null', "average": {"$avg":"$followers"} } }])

            p = 1
            avg = 0
            for i in mydoc:
                avg = avg + i['followers']
                p += 1

            avg_follow = round(avg / p, 0)
            mydoc = tweets_col.find(myquery).sort("followers", -1)

            text = fontstyle.apply('SUMMARY STATISTICS:', 'bold/white/black_BG')

            summary = """
            Number of tweets: {}
    
            Number of users who tweeted the selected word : {}
    
            Average no. of followers for the users who tweeted: {}
    
            """.format(tweets_cnt, dist_users, avg_follow)

            twt_head = fontstyle.apply('2 Tweets from the most followed people ', 'bold/white/black_BG')

            tweet = """"
    
            1.{}
    
            2.{}""".format(mydoc[0]['text'], mydoc[1]['text'])

            print(text, summary, twt_head, tweet)

            ####################################################################
        except:
            error = fontstyle.apply('Use alternate search criteria', 'bold/white/black_BG')
            print(error)
