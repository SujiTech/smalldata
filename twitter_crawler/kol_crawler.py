from tweepy import OAuthHandler
from tweepy import Stream
from streaming import *

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

keys = open('./keyword_list.txt').readlines()
keys = [x[:-1] for x in keys]

l = KOLtoFileListener()
stream = Stream(auth, l)
stream.filter(languages=["ja"], track=keys)