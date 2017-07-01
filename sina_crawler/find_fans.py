# -*- coding: utf-8 -*-

from sina_crawler import *
import random
from concurrent.futures import ThreadPoolExecutor
import time

weibo_accounts = read_users('weibos')
while True:
    with ThreadPoolExecutor(max_workers=10) as executor:
        for user in random.sample(weibo_accounts.keys(), 10):
            if user not in cookies:
                executor.submit(login, user, weibo_accounts[user])

    print(cookies)
    print('登录完成')

    for user in random.sample(list(cookies.keys()), min(10, len(cookies))):
        ret = crawl_fans('2718604160', to_file=True, cookies=cookies[user])
        if ret is None:
            login(user, weibo_accounts[user])

    time.sleep(3600)