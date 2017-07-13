# -*- coding: utf-8 -*-

import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions


def read_users(in_file, delimiter=" "):
    """
    Read weibo username and password from a file, put in a dictionary
    
    :param in_file: the file to read from
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


class SinaCrawler(object):
    def __init__(self, account, password):
        """
        Initialize object's account and password
        """
        self.account = account
        self.password = password
        self.cookies = None

    def set_account(self, account, password):
        """
        Set object's account and password
        """
        self.account = account
        self.password = password

    def test_cookies(self):
        """
        Test if cookies work for a driver
        """
        if self.cookies is None:
            return False
        driver = webdriver.PhantomJS()
        driver.get('http://weibo.cn/')
        time.sleep(1)
        driver.delete_all_cookies()
        for cookie in self.cookies:
            driver.add_cookie(cookie)

        driver.get('http://weibo.cn/')
        if 'logout' in driver.page_source:
            driver.quit()
            return True
        else:
            driver.quit()
            self.cookies = None
            return False

    def login(self):
        """
        Login function for Sina Weibo, which gives a proper cookie to driver
        """
        driver = webdriver.PhantomJS()
        # driver = webdriver.Firefox()
        driver.get('https://passport.weibo.cn/signin/login')
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'loginName')))
        time.sleep(1)  # if met element not interactable error, change it to be longer

        print("======账号登录======")
        try:
            name_field = driver.find_element_by_id('loginName')
            name_field.clear()
            name_field.send_keys(self.account)
            password_field = driver.find_element_by_id('loginPassword')
            password_field.clear()
            password_field.send_keys(self.password)
        except exceptions.InvalidElementStateException:
            self.cookies = None

        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'loginAction')))
        time.sleep(2)
        submit = driver.find_element_by_id('loginAction')
        submit.click()

        self.cookies = driver.get_cookies()
        driver.quit()
        ret = self.test_cookies()
        print(ret)
        return ret

    def get_uid(self, uid):
        """
        :param uid: uid in string, might be customized
        :return: uid in int
        """
        if not self.test_cookies():
            if not self.login():
                return None

        if uid.isdigit():
            return int(uid)
        else:
            driver = webdriver.PhantomJS()
            driver.get("https://weibo.cn/")
            time.sleep(1)
            for cookie in self.cookies:
                driver.add_cookie(cookie)

            driver.get("https://weibo.cn/" + str(uid))
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ut')))
            print("======获取uid======")

            info_element = driver.find_element_by_xpath('//div[@class="ut"]')  # uid
            uid = re.findall('uid=[0-9]+', info_element.get_attribute('innerHTML'), re.M)
            print(int(uid[0][4:]))
            return int(uid[0][4:])

    def crawl_info(self, uid):
        """
        Get information of specific user including nickname, uid, number of weibos, number of followers
        and number of followings

        :param uid: can be customized or uid
        :return: a dict for specific user, including nickname, uid, weibo, follwer, following
        """
        if not self.test_cookies():
            if not self.login():
                return None

        driver = webdriver.PhantomJS()
        for cookie in self.cookies:
            driver.add_cookie(cookie)

        uid = self.get_uid(uid)

        driver.get("https://weibo.cn/" + str(uid))
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ut')))

        nickname = driver.find_element_by_xpath('//div[@class="ut"]').text.split(' ')[0]  # 昵称

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
            'follwings': num_following,
            'followers': num_follower
        }

        return user_info

    def crawl_fans(self, uid, pages=None):
        """
        Get fans list for a user as a list (at most 200 fans limited by Sina)

        :param uid: id, preferred uid as number
        :param pages: number of pages to crawl
        :return: a list of fans in uid
        """

        if not self.test_cookies():
            if not self.login():
                return None

        driver = webdriver.PhantomJS()
        for cookie in self.cookies:
            driver.add_cookie(cookie)

        uid = self.get_uid(uid)
        if pages is None:
            driver.get('https://weibo.cn/' + str(uid) + '/fans')
            time.sleep(1)
            try:
                # print(driver.page_source)
                pages = int(driver.find_element_by_xpath('//input[@name="mp"]').get_attribute('value'))
            except exceptions.NoSuchElementException:
                pages = 1

        print("======获取粉丝======")
        fans_list = []
        for i in range(1, pages + 1):
            print("正在抓取第" + str(i) + "页")
            driver.get('https://weibo.cn/' + str(uid) + '/fans?page=' + str(i))
            user_img_list = driver.find_elements_by_xpath('//table//td[@style]//a')
            # print("本页共有" + str(len(user_img_list)) + '个粉丝')
            for avatars in user_img_list:
                fans_list.append(avatars.get_attribute('href').split("/")[-1])
        # print(fans_list)
        driver.quit()
        return fans_list

    def crawl_repost(self, weiboid, pages=None):
        """
        Crawl repost information around a weibo.

        :param weiboid: weibo's id itself
        :param pages: pages to crawl
        :return: a dict from reposter uid to repost content and from uid.
        """

        if not self.test_cookies():
            if not self.login():
                return None

        driver = webdriver.PhantomJS()
        for cookie in self.cookies:
            driver.add_cookie(cookie)

        if pages is None:
            driver.get('https://weibo.cn/repost/' + weiboid)
            try:
                pages = int(driver.find_element_by_xpath('//input[@name="mp"]').get_attribute('value'))
            except exceptions.NoSuchElementException:
                pages = 1

        reposters = []
        print("======获取原微博======")
        driver.get('https://weibo.cn/repost/' + weiboid)
        nickname = driver.find_element_by_xpath('//div[@id="M_"]//a').text
        uid = driver.find_element_by_xpath('//div[@id="M_"]//a').get_attribute('href').split('/')[-1]
        content = driver.find_element_by_xpath('//div[@id="M_"]//span').text[1:]
        print(content)
        repost_info = {
            'from_weibo_id': None,
            'nickname': nickname,
            'uid': uid,
            'content': content,
            # 'from_uid': [repost_from_uid],
            'weibo_id': weiboid,
        }
        reposters.append(repost_info)

        print("======获取转发======")
        for i in range(1, pages + 1):
            driver.get('https://weibo.cn/repost/' + weiboid + '?page=' + str(i))
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
                repost_weibo_id = repost.find_element_by_partial_link_text(u'赞').get_attribute('href').split("/")[-2]
                print(repost_weibo_id, end=" ")

                repost_info = {
                    'from_weibo_id': weiboid,
                    'nickname': reposter_nickname,
                    'uid': reposter_uid,
                    'content': reposter_content,
                    # 'from_uid': [repost_from_uid],
                    'weibo_id': repost_weibo_id,
                }
                reposters.append(repost_info)
        print()
        driver.quit()
        return reposters

