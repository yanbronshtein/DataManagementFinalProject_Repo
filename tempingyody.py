import time
import re


def store_data_mongo_mysql(json_data, sql_conn, sql_cursor, tweets_db_mongo):
    for row in json_data:
        user = row['user']
        input = [user['id_str'], user['name'], user['screen_name'], user['followers_count'], user['friends_count'],
                 user['listed_count'], user['favourites_count'], user['statuses_count']]

        input[1] = re.sub("'", "", input[1])

        hashtags = []

        # if row['truncated'] == False:
        #     text = row['text']
        #     for i in row['entities']['hashtags']:
        #         hashtags.append(i['text'])
        # else:
        #     text = row['extended_tweet']['full_text']
        #     for i in row['extended_tweet']['entities']['hashtags']:
        #         hashtags.append(i['text'])

        is_retweet = False
        text = row['text']
        for i in row['entities']['hashtags']:
            hashtags.append(i['text'])

        try:
            #try to get retweet text
            if row['text'][0:2] == 'RT':
                is_retweet = True
                retweet_hashtags = []
                retweet_text = row['retweeted_status']['text']

                for i in row['retweeted_status']['entities']['hashtags']:
                    retweet_hashtags.append(i['text'])

            else:
                # is_retweet = False
                retweet_text = None
                retweet_hashtags = None
        except:
            # is_retweet = False
            retweet_text = None
            retweet_hashtags = None

        time = datetime.strftime(datetime.strptime(row['created_at'], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

        document_dict = {"tweet_id": row['id_str'],
                         "created_date": time,
                         "user_id": row['user']['id_str'],
                         "screen_name": row['user']['screen_name'],
                         "followers_count": row['user']['followers_count'],
                         "favorite_count": row['favorite_count'],
                         "original_hash": hashtags,
                         "retweet_hash": retweet_hashtags,
                         "is_retweet": is_retweet,
                         "tweet_text": text,
                         "retweet_text": retweet_text}
        insert_mongo(document_dict, tweets_db_mongo)
        insert_mysql(input, sql_cursor)



