# -*- coding: utf-8 -*-

from tweepy import OAuthHandler
from tweepy import Stream
from streaming import *

l = SteamingToFileListener()
# l = SteamingToFileListener('akb48総選挙2017') # specify keyword for filename
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

stream = Stream(auth, l)
# stream.filter(languages=["ja"], track=['akb48総選挙2017'])
stream.sample(languages=["ja"]) # if random japanese sample
