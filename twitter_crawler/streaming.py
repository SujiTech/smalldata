# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener

import datetime
import pytz
import json
import csv

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key = "oaLOlFoGkAQfcjkzAxyJo4z3G"
consumer_secret = "K2v11btonE3DhAjZeTF0s45R4dtJcuQn6CE6x9SyK8lICXRH8n"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token = "332084575-IvVdGGqc2s90KIjbsBuuYX0w0az2M7Mfk2GvUVJO"
access_token_secret = "J4PSvqyoztPZX6szAS7i4o4RRDThxeq8018cJxeJ2HUzi"


class SteamingToFileListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def __init__(self, keyword=None, timezone='Japan'):
        super().__init__()
        if keyword is None:
            self.keyword = 'random'
        else:
            self.keyword = str(keyword)
        self.timezone = timezone
        self.date = datetime.datetime.now(pytz.timezone(self.timezone)).date().strftime("%Y-%m-%d")
        self.f = open('data/' + self.date + '-' + self.keyword + '.txt', "a+")

    def on_data(self, data):
        # print(data)
        # tweet = json.loads(data)
        today = datetime.datetime.now(pytz.timezone(self.timezone)).date().strftime("%Y-%m-%d")
        if self.date is not today:
            self.f.close()
            self.date = today
            self.f = open('data/' + self.date + '-' + self.keyword + '.txt', "a+")
        print(data)
        self.f.write(str(data))
        return True

    def on_error(self, status):
        print(status)

class KOLtoFileListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """

    def __init__(self, keyword=None):
        super().__init__()
        if keyword is None:
            self.keyword = 'all'
        else:
            self.keyword = str(keyword)
        self.f = open('data/' + self.keyword + '-kol.csv', "a+", encoding='utf-8') 
        self.writer = csv.writer(self.f, delimiter=',')
        # self.writer.writerow(['昵称', '用户名', '简介', '粉丝', '关注', '推文数', '喜欢'])

    def on_data(self, data):
        # print(data)
        tweet = json.loads(data)
        try:
            des = tweet['user']['description']
            if u'画家' in des or u'アニメーター' in des or u'脚本' in des or u'ライター' in des or u'イラストレーター' in des:
                print(tweet['user']['name'])
                self.writer.writerow([tweet['user']['name'], tweet['user']['screen_name'], tweet['user']['description'], tweet['user']['followers_count'], tweet['user']['friends_count'], tweet['user']['statuses_count'], tweet['user']['favourites_count']])
        except Exception:
            pass
        
        return True


    def on_error(self, status):
        print(status)

