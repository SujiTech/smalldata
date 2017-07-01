# -*- coding: utf-8 -*-

from sina_crawler import *
import random
import networkx as nx
from concurrent.futures import ThreadPoolExecutor

weibo_accounts = read_users('weibos')

with ThreadPoolExecutor(max_workers=10) as executor:
    for user in random.sample(weibo_accounts.keys(), 10):
        if user not in cookies:
            executor.submit(login, user, weibo_accounts[user])

print(cookies)
print('登录完成')

G = nx.DiGraph()
crawl_list = ['FafFXpljI']
crawled_set = set(crawl_list)
for i in range(4):  # set depth
    for weibo in crawl_list:
        with ThreadPoolExecutor(max_workers=10) as executor:
            reposts = [executor.submit(crawl_repost, weibo, None, False, cookies[random.choice(cookies.keys())])
                       for weibo in crawl_list]
    crawl_list = []
    print('爬取完成')

    for repost in reposts:
        # print(len(repost.result()))
        for uid in repost.result().keys():
            # if repost[uid]['weibo_id'] not in crawled_set:
            # print(repost.result()[uid])
            crawl_list.append(repost.result()[uid]['weibo_id'])
            G.add_edge(repost.result()[uid]['from_weibo_id'], repost.result()[uid]['weibo_id'])
    crawl_list = list(set(crawl_list))
    print(crawl_list)

nx.draw_networkx(G)
plt.savefig("path.png")



