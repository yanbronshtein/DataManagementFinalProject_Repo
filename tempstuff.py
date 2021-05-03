for row in json_data:
    user = row['user']
    input = [user['id_str'], user['name'], user['screen_name'], user['followers_count'], user['friends_count'],
             user['listed_count'], user['favourites_count'], user['statuses_count']]

    # Cleaning commas from User name and Description
    input[1] = re.sub("'", "", inp[1])
    # if inp[3] is not None:
    #     inp[3] = re.sub("'", "", inp[3])

    ############mongoshit
    entities = []
    if row['truncated'] == False:
        text = row['text']
        for i in row['entities']['hashtags']:
            entities.append(i['text'])
    else:
        text = row['extended_tweet']['full_text']
        for i in row['extended_tweet']['entities']['hashtags']:
            entities.append(i['text'])

    try:  # If the first 2 words of the tweet is RT but it is not actually retweet
        if row['text'][0:2] == 'RT':
            retweet = "Y"
            # Getting hashtags and hashtags from the retweeted object
            rt_entities = []
            if row['retweeted_status']['truncated'] == False:
                rt_text = row['retweeted_status']['text']

                for i in row['retweeted_status']['entities']['hashtags']:
                    rt_entities.append(i['text'])
            else:
                rt_text = row['retweeted_status']['extended_tweet']['full_text']

                for i in row['retweeted_status']['extended_tweet']['entities']['hashtags']:
                    rt_entities.append(i['text'])
        else:
            retweet = "N"
            rt_text = None
            rt_entities = None
    except:
        retweet = "N"
        rt_text = None
        rt_entities = None

    time = datetime.strftime(datetime.strptime(row['created_at'], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')

    document_dict = {"tweet_id": row['id_str'],
                     "time": time,
                     "user_id": row['user']['id_str'],
                     "screen_name": row['user']['screen_name'],
                     "followers_count": row['user']['followers_count'],
                     "favorite_count": row['favorite_count'],
                     "hash_orig": entities,
                     "hash_rtwt": rt_entities,
                     "retweet": retweet,
                     "tweet_text": text,
                     "rtwt_text": rt_text}
    insert_mongo(document_dict, tweets_db_mongo)
    insert_mysql(input, sql_cursor)

