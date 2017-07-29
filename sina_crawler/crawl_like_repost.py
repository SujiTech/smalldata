# -*- coding: utf-8 -*-

from sina_weibo_crawler import *
import json

weibo_accounts = read_users('weibos')
weibo_account_list = []
for user in weibo_accounts:
    weibo_account_list.append(SinaCrawler(user, weibo_accounts[user]))

i = 0
while not weibo_account_list[i].login():
    weibo_account_list.remove(weibo_account_list[i])

weibo_ids = weibo_account_list[i].crawl_weiboid('babychara', pages=2)
print(weibo_ids)
print(len(weibo_ids))

like_dict = {}
repost_dict = {}
for weibo_seed in weibo_ids:
    while not weibo_account_list[i].login():
        weibo_account_list.remove(weibo_account_list[i])
    
    like_list = weibo_account_list[i].crawl_like_id(weibo_seed)
    like_dict[weibo_seed] = like_list

    while not weibo_account_list[i].login():
        weibo_account_list.remove(weibo_account_list[i])
    
    repost_list = weibo_account_list[i].crawl_repost_id(weibo_seed)
    repost_dict[weibo_seed] = repost_list

with open('data/like_repost_1', 'w+') as f:
    json.dump((like_dict, repost_dict), f)