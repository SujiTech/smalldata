# -*- coding: utf-8 -*-

import re
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
import networkx as nx
import matplotlib.pyplot as plt

cookies = {}


def read_users(in_file, delimiter=" "):
    """
    Read weibo username and password from a file, put in a dictionary
    
    :param in_file: the file to read from -- username and password should be split by " " if not specified
    :param delimiter: specify delimiter used in the file
    :return: a dictionary where (key, value) is (username, password)
    """
    with open(in_file, 'r') as f:
        weibos = {}
        for line in f:
            weibo = line.strip().split(delimiter)
            # print weibo
            if len(weibo) > 1:
                weibos[weibo[0]] = weibo[1]

    return weibos


def get_uid(uid, cookies):
    """

    :param uid: uid in string, might be customized
    :param cookies: cookies
    :return: uid in int
    """
    if uid.isdigit():
        return int(uid)
    else:
        uid_driver = webdriver.PhantomJS()
        uid_driver.delete_all_cookies()

        uid_driver.get("https://weibo.cn/")
        time.sleep(1)
        for cookie in cookies:
            print(cookie)
            uid_driver.add_cookie(cookie)

        uid_driver.get("https://weibo.cn/" + str(uid))
        WebDriverWait(uid_driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ut')))

        uid_str_list = uid_driver.find_elements_by_xpath('//div[@class="ut"]//a')  # uid
        for uid_str in uid_str_list:
            uid = re.findall('/[0-9]+/', uid_str.get_attribute('href'), re.M)
            if len(uid) > 0:
                uid = int(uid[0][1:-1])
                break

        return uid


def login(username, password):
    """
    Login function for Sina Weibo, which gives a proper cookie to driver
    
    :param username: login username -- can be email, mobile phone or customized username
    :param password: corresponding password to username
    :return: login status -- can be true or false
    """
    driver = webdriver.PhantomJS()

    driver.get('https://passport.weibo.cn/signin/login')
    # time.sleep(15)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'loginName')))
    time.sleep(2)  # if met element not interactable error, change it to be longer

    print('开始登录')
    try:
        name_field = driver.find_element_by_id('loginName')
        name_field.clear()
        name_field.send_keys(username)
        password_field = driver.find_element_by_id('loginPassword')
        password_field.clear()
        password_field.send_keys(password)
    except exceptions.InvalidElementStateException:
        return False, None

    submit = driver.find_element_by_id('loginAction')
    submit.click()
    time.sleep(2)

    driver_cookies = driver.get_cookies()
    driver.get('http://weibo.cn/')
    if 'info' in driver.page_source:
        print('登录成功')
        driver.quit()
        cookies[username] = driver_cookies
        return driver_cookies
    else:
        print('登录失败')
        driver.quit()
        return False


def crawl_info(uid, to_file=False, cookies=None):
    """
    Get information of specific user including nickname, uid, number of weibos, number of followers 
    and number of followings
    
    :param id: can be customized or uid
    :param to_file: whether output result to file
    :param cookies: set cookie to driver if passed in
    :return: a dict for specific user, including nickname, uid, weibo, follwer, following
    """
    driver = webdriver.PhantomJS()

    if bool(cookies):
        driver.get('http://weibo.cn/')
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('http://weibo.cn/')
        if 'info' in driver.page_source:
            print('登录成功')
        else:
            print('登录失败')
            return

    driver.get("https://weibo.cn/" + str(uid))
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ut')))

    nickname = driver.find_element_by_xpath('//div[@class="ut"]').text.split(' ')[0]  # 昵称
    uid_str_list = driver.find_elements_by_xpath('//div[@class="ut"]//a')  # uid
    for uid_str in uid_str_list:
        uid = re.findall('/[0-9]+/', uid_str.get_attribute('href'), re.M)
        if len(uid) > 0:
            uid = int(uid[0][1:-1])
            break
    print(nickname, uid)

    pattern = '\[[0-9]+\]'
    user_info = driver.find_element_by_xpath('//div[@class="tip2"]').text.split(' ')
    num_weibo = int(re.findall(pattern, user_info[0], re.M)[0][1:-1])
    num_following = int(re.findall(pattern, user_info[1], re.M)[0][1:-1])
    num_follower = int(re.findall(pattern, user_info[2], re.M)[0][1:-1])
    print(num_weibo, num_following, num_follower)

    user_info = {
        'nickname': nickname,
        'uid': uid,
        'weibos': num_weibo,
        'follwing': num_following,
        'follower': num_follower
    }

    if to_file:
        with open(str(uid) + '_info.txt', "a+") as f:
            f.write(str(json.dumps(user_info)).encode('utf-8'))
            f.write('\n')

    return user_info


def crawl_weibo(uid, pages=None, to_file=False, cookies=None):
    """
    Get Weibo Details from specific user
    :param uid: id, preferred uid as number
    :param pages: largest pages to read, default is crawling all pages
    :param to_file: whether output result to file
    :param cookies: set cookie to driver if passed in
    :return: a list of weibo, where every element is a dict including weibo content, attitudes, reposts and comments
    """
    driver = webdriver.PhantomJS()
    if bool(cookies):
        driver.get('http://weibo.cn/')
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('http://weibo.cn/')
        if 'info' in driver.page_source:
            print('登录成功')
        else:
            print('登录失败')
            return

    uid = get_uid(uid, driver.get_cookies())
    if pages is None:
        driver.get('https://weibo.cn/' + str(uid))
        try:
            pages = int(driver.find_element_by_xpath('//input[@name="mp"]').get_attribute('value'))
        except exceptions.NoSuchElementException:
            pages = 1

    weibos = []
    for i in range(1, pages + 1):
        driver.get('https://weibo.cn/' + str(uid) + '?page=' + str(i))
        weibo_content_list = driver.find_elements_by_xpath('//div[starts-with(@id, "M_")]')
        for weibo in weibo_content_list:
            content = weibo.find_element_by_xpath('.//span[@class="ctt"]').text

            pattern = '\[[0-9]+\]'
            num_attitude =int(re.findall(pattern,
                                         weibo.find_element_by_xpath('.//a[contains(@href, "attitude")]').text,
                                         re.M)[0][1:-1])
            num_repost = int(re.findall(pattern,
                                         weibo.find_element_by_xpath('.//a[contains(@href, "repost")]').text,
                                         re.M)[0][1:-1])

            comments = weibo.find_elements_by_xpath('.//a[contains(@href, "comment")]')
            if len(comments) > 1:
                num_comment = int(re.findall(pattern, comments[1].text, re.M)[0][1:-1])
                content = "".join(weibo.text.split("  ")[:-1])
            else:
                num_comment = int(re.findall(pattern, comments[0].text, re.M)[0][1:-1])

            print(content.replace('\r\n', ' ').replace('\n', ' '))
            print(num_attitude, num_repost, num_comment)
            print()

            weibo_content = {
                'content': content,
                'attitude': num_attitude,
                'repost': num_repost,
                'comment': num_comment
            }
            weibos.append(weibo_content)

            if to_file:
                with open(str(uid) + '_weibo.txt', "a+") as f:
                    f.write(str(json.dumps(weibo_content)).encode('utf-8'))
                    f.write('\n')
    return weibos


def crawl_fans(uid, pages=None, to_file=False, cookies=None):
    """
    Get fans list for a user as a list (at most 200 fans limited by Sina)
    
    :param uid: id, preferred uid as number
    :param pages: number of pages to crawl
    :param to_file: whether output result to file
    :param cookies: set cookie to driver if passed in
    :return: a list of fans in uid
    """

    driver = webdriver.PhantomJS()
    if bool(cookies):
        driver.get('http://weibo.cn/')
        time.sleep(1)
        driver.delete_all_cookies()
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('http://weibo.cn/')
        if 'info' in driver.page_source:
            print('登录成功')
        else:
            print('登录失败')
            return None

    uid = get_uid(uid, driver.get_cookies())
    if pages is None:
        driver.get('https://weibo.cn/' + str(uid) + '/fans')
        try:
            pages = int(driver.find_element_by_xpath('//input[@name="mp"]').get_attribute('value'))
        except exceptions.NoSuchElementException:
            pages = 1

    print("获取粉丝")
    print(str(pages))
    fans_list = []
    for i in range(1, pages + 1):
        print("正在抓取第" + str(i) + "页")
        driver.get('https://weibo.cn/' + str(uid) + '/fans?page=' + str(i))
        # print driver.page_source
        user_img_list = driver.find_elements_by_xpath('//table//td[@style]//a')
        print("本页共有" + str(len(user_img_list)) + '个粉丝')

        for avatars in user_img_list:
            fans_list.append(avatars.get_attribute('href').split("/")[-1])

    print(fans_list)
    # processed_fan_list = []
    # for fan in fans_list:
    #     # print(fan)
    #     fan_uid = get_uid(fan, driver.get_cookies())
    #     # print fan_uid
    #     processed_fan_list.append(fan_uid)

    if to_file:
        with open(str(uid) + '_fans.txt', "a+") as f:
            f.write(str(fans_list))
            f.write('\n')

    driver.quit()
    return list(set(fans_list))


def crawl_repost(weibo_id, pages=None, graph=False, cookies=None, reposters={}):
    """
    Crawl repost infomation around a weibo.

    :param uid: weibo's original poster's uid
    :param weibo_id: weibo's id itself
    :param pages: pages to crawl
    :param graph: if output to a graph
    :param cookies: use cookies
    :return: a dict from reposter uid to repost content and from uid.
    """

    driver = webdriver.PhantomJS()
    if bool(cookies):
        driver.get('http://weibo.cn/')
        time.sleep(1)
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.get('http://weibo.cn/')
        if 'info' in driver.page_source:
            print('登录成功')
        else:
            print('登录失败')
            return None

    # uid = get_uid(uid, driver.get_cookies())
    if pages is None:
        driver.get('https://weibo.cn/repost/' + weibo_id)
        try:
            pages = int(driver.find_element_by_xpath('//input[@name="mp"]').get_attribute('value'))
        except exceptions.NoSuchElementException:
            pages = 1
    # print(weibo_id)
    for i in range(1, pages + 1):
        driver.get('https://weibo.cn/repost/' + weibo_id + '?page=' + str(i))
        repost_list = driver.find_elements_by_xpath('//div[@class="c"]')
        # print(len(repost_list))
        for repost in repost_list:
            if 'attitude' not in repost.get_attribute('innerHTML'):
                continue

            reposter_info = repost.find_element_by_xpath('.//a')
            reposter_nickname = reposter_info.text
            reposter_uid = reposter_info.get_attribute('href').split("/")[-1]

            reposter_content = ":".join(repost.text.split(":")[1:])
            reposter_content = reposter_content[:reposter_content.find(u'赞')].split("//@")[0]
            # print(reposter_content)

            repost_weibo_id = repost.find_element_by_partial_link_text(u'赞').get_attribute('href').split("/")[-2]
            print(repost_weibo_id)
            # if '//@' in repost.text:
            #     pattern = '\/\/<a[^@]*\>'
            #     source = re.findall(pattern, repost.get_attribute('innerHTML'), re.M)[0]
            #     source = source[source.find('\"') + 2: -2]
            #     # print(source)
            #     repost_from_uid = get_uid(source)
            #     # print(repost_from_uid)
            # else:
            #     repost_from_uid = uid
            # print(repost_from_uid)

            repost_info = {
                'from_weibo_id': weibo_id,
                'nickname': reposter_nickname,
                'uid': reposter_uid,
                'content': reposter_content,
                # 'from_uid': [repost_from_uid],
                'weibo_id': repost_weibo_id,
            }

            reposters[reposter_uid] = repost_info

    # print(reposters)

    return reposters

