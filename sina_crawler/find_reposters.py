# -*- coding: utf-8 -*-

from sina_crawler import *
import random


weibo_accounts = read_users('weibos')

login_threads = []
for user in random.sample(list(weibo_accounts.keys()), 5):
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

crawl_list = ['F9BuPfjFb']
for i in range(2):
    repost_threads = []
    reposters = [{} for _ in range(len(crawl_list))]
    for n, weibo in enumerate(crawl_list):
        t = Thread(target=crawl_repost, args=(weibo, None, False,
                                              random.choice(list(cookies.values())), reposters[n]))
        repost_threads.append(t)
    crawl_list = []
    for thr in repost_threads:
        thr.start()
    for thr in repost_threads:
        thr.join()
    print('爬取完成')

    for repost in reposters:
        for uid in repost.keys():
            crawl_list.append(repost[uid]['weibo_id'])
    print(crawl_list)





