import json
import tweepy
import sys
consumer_key = "ivnYtcjufwJxcPsOSIbgjcqRW"
consumer_secret = "pmhfQrFyQ5j1YJHKI0J2s07te6HFaeD0r0F4Pt4ErFfhBVQoyt"
access_token = "1377717932030111748-TzVAliHIh3rGUx0KGcJ9tfkQpoOki0"
access_token_secret = "ZGm22tqdlj8BKGEHdwX4kPY1ibY2VpODZFhjjYoMHpQEq"

tweet_counter = 0
TWEET_MAX = 10500 #At least 10000
class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api, write_file):
        self.api = api
        self.me = api.me()
        self.f = f

    def on_status(self, tweet):
        """
        1.extract the username
        """
        global tweet_counter
        tweet_counter += 1
        print("tweet_counter", tweet_counter)
        if tweet_counter < 3:
            json.dump(tweet._json, f)
            f.write(',')

        else:
            f.write(']')
            self.f.close()
            sys.exit(0)



    def on_error(self, status):
        print("Error detected")



auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

f = open("out.json", "w")
f.write('[')
tweets_listener = MyStreamListener(api, f)
stream = tweepy.Stream(api.auth, tweets_listener)


stream.filter(track=['#iHeartAwards'], languages=['en'])
print("Hi")

