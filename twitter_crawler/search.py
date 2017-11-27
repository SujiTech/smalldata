# -*- coding: utf-8 -*-
import tweepy
from tweepy import OAuthHandler
from streaming import *
import json
from collections import defaultdict
import subprocess

l = SteamingToFileListener()
l = SteamingToFileListener(u'tongren') # specify keyword for filename
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

keys = open('./keyword_list.txt').readlines()
keys = [x[:-1] for x in keys]


for key in keys:
    subprocess.call(['mkdir', './tweets/%s'%key])
    results = tweepy.Cursor(api.search, q=key).items(1000)
    users = defaultdict(list)
    for result in results:
        a = result._json
        uname = a['user']['id_str']
        if uname not in users:
            subprocess.call(['mkdir', './tweets/%s/%s'%(key,uname)])
        with open('./tweets/%s/%s/%d' % (key, uname, len(users[uname])), 'w') as out_f:
            json.dump(a, out_f)
