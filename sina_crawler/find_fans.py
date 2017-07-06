# -*- coding: utf-8 -*-

from sina_crawler import *
import random
import os
from concurrent.futures import ThreadPoolExecutor
import time

weibo_accounts = read_users('weibos')
user_seed = '2718604160'
while True:
    if not os.path.isfile('cookies'):
        with ThreadPoolExecutor(max_workers=30) as executor:
            for user in weibo_accounts.keys():
                if user not in cookies:
                    executor.submit(login, user, weibo_accounts[user])
        # print(cookies)
        print('登录完成')
        with open('cookies', "w") as f:
            json.dump(cookies, f)
    else:
        with open('cookies') as f:    
            cookies = json.load(f)
        print(type(cookies))

    for user in random.sample(list(cookies.keys()), min(10, len(cookies))):
        ret = crawl_fans(user_seed, cookies=cookies[user])
        if ret is None:
            login(user, weibo_accounts[user])
        else:
            with open(user_seed + '_fans.txt', "w") as f:
                json.dump(ret, f)
    time.sleep(3600)