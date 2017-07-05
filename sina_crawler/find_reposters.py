# -*- coding: utf-8 -*-

from sina_crawler import *
import random
import networkx as nx
from concurrent.futures import ThreadPoolExecutor

weibo_accounts = read_users('weibos')

with ThreadPoolExecutor(max_workers=30) as executor:
    for user in random.sample(weibo_accounts.keys(), 80):
        if user not in cookies:
            executor.submit(login, user, weibo_accounts[user])
print(cookies)
print('登录完成')

weibo_seed = 'F983G1RRs'

G = nx.DiGraph()
crawl_list = [weibo_seed]
crawled_set = set([])
for i in range(4):  # set depth
    print(crawl_list)
    reposts = {}
    for weibo in crawl_list:
        if weibo not in crawled_set:
            with ThreadPoolExecutor(max_workers=60) as executor:
                reposts[weibo] = executor.submit(crawl_repost, weibo, None, False, cookies[random.choice(list(cookies.keys()))])
            crawled_set.add(weibo)
    crawl_list = []
    print('爬取完成')

    for repost in reposts.keys():
        # print(reposts[repost].result())
        try:
            for uid in reposts[repost].result().keys():
                # if repost[uid]['weibo_id'] not in crawled_set:
                # print(repost.result()[uid])
                crawl_list.append(reposts[repost].result()[uid]['weibo_id'])
                G.add_edge(reposts[repost].result()[uid]['from_weibo_id'], reposts[repost].result()[uid]['weibo_id'])
        except Exception as e:
            continue
    crawl_list = list(set(crawl_list))
    # print(crawl_list)

nx.draw_networkx(G)
plt.savefig(weibo_seed + ".png")

with open(weibo_seed + '.txt', "a+") as f:
    for node in G.nodes():
        f.write(node + " "  + str(G.in_degree(node)) + " " + str(G.out_degree(node)))
        f.write('\n')
