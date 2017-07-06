# -*- coding: utf-8 -*-

from sina_crawler import *
import random
import json
import os.path
import math
import networkx as nx
from concurrent.futures import ThreadPoolExecutor

weibo_accounts = read_users('weibos')

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


weibo_seed = 'F98n9EOuP'

G = nx.DiGraph()
crawl_list = [weibo_seed]
crawled_set = set([])
for i in range(4):  # set depth
    print(crawl_list)
    reposts = {}
    for weibo in crawl_list:
        if weibo not in crawled_set:
            with ThreadPoolExecutor(max_workers=100) as executor:
                reposts[weibo] = executor.submit(crawl_repost, weibo, None, False, cookies[random.choice(list(cookies.keys()))])
            crawled_set.add(weibo)
    crawl_list = []
    print('爬取完成')

    for repost in reposts.keys():
        # print(reposts[repost].result())
        try:
            with open(weibo_seed + '.txt', "a+") as f:
                json.dump(reposts[repost].result(), f)
                f.write('\n')
            for uid in reposts[repost].result().keys():
                # if repost[uid]['weibo_id'] not in crawled_set:
                # print(repost.result()[uid])
                crawl_list.append(reposts[repost].result()[uid]['weibo_id'])
                G.add_edge(reposts[repost].result()[uid]['from_weibo_id'], reposts[repost].result()[uid]['weibo_id'])
                
        except Exception as e:
            print(e)
            continue
    crawl_list = list(set(crawl_list))
    # print(crawl_list)

nx.write_gml(G, weibo_seed + ".gml")
plt.figure(figsize=(20, 20), dpi=80)
plt.axis('off')
pos = nx.spring_layout(G)
nx.draw_networkx(G,  node_size=[math.pow(math.log((G.out_degree(v) + 1) * 10, 2), 3) for v in G.nodes()], with_labels=False)
plt.savefig(weibo_seed + ".png")

with open(weibo_seed + '_degrees.txt', "a+") as f:
    for node in G.nodes():
        f.write(node + " "  + str(G.in_degree(node)) + " " + str(G.out_degree(node)))
        f.write('\n')
