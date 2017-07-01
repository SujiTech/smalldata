#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, print_function

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import json
import datetime

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="oaLOlFoGkAQfcjkzAxyJo4z3G"
consumer_secret="K2v11btonE3DhAjZeTF0s45R4dtJcuQn6CE6x9SyK8lICXRH8n"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="332084575-IvVdGGqc2s90KIjbsBuuYX0w0az2M7Mfk2GvUVJO"
access_token_secret="J4PSvqyoztPZX6szAS7i4o4RRDThxeq8018cJxeJ2HUzi"

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        # print(data)
        # tweet = json.loads(data)

        date = str(datetime.date.today())
        with open(date+'-nokeyword.txt', "a+") as f:
            f.write(str(data))
        
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.sample(languages=["ja"])
