import redis
from time import sleep
from datetime import timedelta
r = redis.Redis()
print(r.mset({'hashtag': 'sundayvibes','mongo_info':'info_m', 'sql_info': 'info_s'}))
print(r.expire('hashtag', timedelta(seconds=10)))
print(r.ttl('hashtag'))
sleep(5)
print(r.ttl('hashtag'))
sleep(5)
print(r.ttl('hashtag'))

# r.hset()
# r.lrange()