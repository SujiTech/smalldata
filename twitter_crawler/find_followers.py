# -*- coding: utf-8 -*-

import json
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.PhantomJS()
# try:
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
        print(data['user']['screen_name'])
        driver.get('https://twitter.com/' +
                   data['user']['screen_name'] + '/followers')
        print('https://twitter.com/' +
              data['user']['screen_name'] + '/followers')
        time.sleep(2)
        # print(driver.page_source)
        follower_list = []
        # follower_num = 0
        # while len(driver.find_elements_by_xpath('//div[@class="ProfileCard-content"]//b[@class="u-linkComplex-target"]')) > follower_num:
        #     follower_num = len(driver.find_elements_by_xpath(
        #         '//div[@class="ProfileCard-content"]//b[@class="u-linkComplex-target"]'))
        #     print(follower_num)
        #     print(driver.execute_script("return document.body.scrollHeight"))
        #     time.sleep(5)

        lastHeight = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            newHeight = driver.execute_script("return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight

        # print(driver.page_source)
        for follower in driver.find_elements_by_xpath('//div[@class="ProfileCard-content"]//b[@class="u-linkComplex-target"]'):
            follower_list.append(follower.text)
        print(follower_list)
        break
