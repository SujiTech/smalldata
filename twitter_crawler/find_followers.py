# -*- coding: utf-8 -*-

import json
import time

import tweepy
from selenium import webdriver

from pyvirtualdisplay import Display

# tweepy setup
consumer_key = "oaLOlFoGkAQfcjkzAxyJo4z3G"
consumer_secret = "K2v11btonE3DhAjZeTF0s45R4dtJcuQn6CE6x9SyK8lICXRH8n"
access_token = "332084575-IvVdGGqc2s90KIjbsBuuYX0w0az2M7Mfk2GvUVJO"
access_token_secret = "J4PSvqyoztPZX6szAS7i4o4RRDThxeq8018cJxeJ2HUzi"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# selenium setup
display = Display(visible=0, size=(1366, 768))
display.start()
capabilities = webdriver.DesiredCapabilities().FIREFOX
capabilities["marionette"] = False
driver = webdriver.Firefox(capabilities=capabilities)
driver.get('https://twitter.com/login')
time.sleep(2)
username = driver.find_element_by_class_name("js-username-field")
password = driver.find_element_by_class_name("js-password-field")
username.clear()
password.clear()
username.send_keys("tika.summer@gmail.com")
password.send_keys("Kami8989sama.")
time.sleep(2)
driver.find_element_by_xpath('//button[@type="submit"]').click()
print(driver.get_cookies())

driver.get('https://twitter.com/')
driver.maximize_window()
time.sleep(1)
if '1mEther' not in driver.page_source:
    exit()

with open('data/2017-07-18-random.txt') as f:
    for line in f:
        data = json.loads(line)
        follower_list = []
        try:
            user = api.get_user(data['user']['screen_name'])
            print(user.screen_name)
            print(user.followers_count)
            if user.followers_count < 800:
                driver.get('https://twitter.com/' + user.screen_name + '/followers')
                time.sleep(2)

                lastHeight = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(5)
                    newHeight = driver.execute_script("return document.body.scrollHeight")
                    if newHeight == lastHeight:
                        break
                    lastHeight = newHeight
                for follower in driver.find_elements_by_xpath('//div[@class="ProfileCard-content"]//div[contains(@class, "user-actions")]'):
                    follower_list.append(int(follower.get_attribute('data-user-id')))
            elif user.followers_count > 50000:
                continue
            else:
                for page in tweepy.Cursor(api.followers_ids, screen_name=user.screen_name).pages():
                    follower_list.extend(page)
                    time.sleep(2)
        except tweepy.TweepError:
            continue
        print(follower_list)
        
        with open('data/followers', 'a') as f:
            f.write(str({user.id: follower_list}))