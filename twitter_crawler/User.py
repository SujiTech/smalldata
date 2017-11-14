import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler

CONSUMER_KEY = "oaLOlFoGkAQfcjkzAxyJo4z3G"
CONSUMER_SECRET = "K2v11btonE3DhAjZeTF0s45R4dtJcuQn6CE6x9SyK8lICXRH8n"
ACCESS_KEY = "332084575-IvVdGGqc2s90KIjbsBuuYX0w0az2M7Mfk2GvUVJO"
ACCESS_SECRET = "J4PSvqyoztPZX6szAS7i4o4RRDThxeq8018cJxeJ2HUzi"

auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

class User(object):
    def __init__(self, id):
        self.user = api.get_user(id)
        # print(self.user)

    def screen_name(self):
        return self.user.screen_name
    
    def description(self):
        return self.user.description

    def followers_count(self):
        return self.user.followers_count

    def statuses_count(self):
        return self.user.statuses_count

    def url(self):
        return self.user.url
    
    def recent_statuses(self):
        return api.user_timeline(self.screen_name())