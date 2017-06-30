# -*- coding: utf-8 -*-

from sina_crawler import *
import random
import time


weibo_accounts = read_users('weibos')
while True:
    login_threads = []
    for user in random.sample(list(weibo_accounts.keys()), 30):
        if user in cookies:
            continue
        t = Thread(target=login, args=(user, weibo_accounts[user]))
        login_threads.append(t)
    for thr in login_threads:
        thr.start()
    for thr in login_threads:
        thr.join()

    print(cookies)
    print('登录完成')

    for user in random.sample(list(cookies.keys()), min(10, len(cookies))):
        ret = crawl_fans('2718604160', to_file=True, cookies=cookies[user])
        if ret is None:
            login(user, weibo_accounts[user])

    time.sleep(3600)