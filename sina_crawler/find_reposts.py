# -*- coding: utf-8 -*-

from sina_weibo_crawler import *
import json
import os
import os.path
import math
import networkx as nx
from networkx.readwrite import json_graph
# from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

weibo_accounts = read_users('weibos')
weibo_account_list = []
for user in weibo_accounts:
    weibo_account_list.append(SinaCrawler(user, weibo_accounts[user]))

i = 0
while not weibo_account_list[i].login():
    weibo_account_list.remove(weibo_account_list[i])

# weibo_ids = weibo_account_list[i].crawl_weiboid('qiechihe') 
# weibo_ids = ['EAEbmxbK5', 'EAm0GbGCX', 'EAexym6Em', 'EA58gwczN', 'EzVyP4CsB', 'EzTIpcpkU', 'EzRVb2ZQg', 'EzM9zjK30', 'EzCInEaV0', 'Ezavm2M4D', 'Ez11tkeLo', 'EyRzW5MUZ', 'EyIv9dZ2J', 'EyFCw9wws', 'EyyQU6EVn', 'EydAjhFdu', 'Ey6HLC3eC', 'ExX3eu8yd', 'ExOEthuTd', 'ExFeHnmVt', 'ExDV5nO8B', 'Ex2I18qKL', 'EwKgdFjZd', 'Ewr361Wqq', 'EvYPtolMd', 'Evw9c0BYk', 'EuUEbxweq', 'EuC399aDJ', 'Eu6hVoups', 'EsDl9oqXx', 'EskCOhmPd', 'EsbkQ6ZKc', 'Es1tQjOFv', 'Es1mYdtyY', 'ErQ5g7QOF', 'ErzpR8gpF', 'Erq7ACZ5M', 'EqUYNuRQP', 'EqEyU4CEZ', 'EqmjMkJRX', 'EqlxJvLjs', 'Eqkna2N5y', 'Eqczm2Iai', 'EqbpMo2oH', 'EpK8YncsS', 'EpAf17CBj', 'Eps093Fhg', 'Epo95tvxe', 'EphRJuPV0', 'EpfPceeio', 'Ep8Eq36E5', 'EoQqNkMcF', 'EoGUxxnYp', 'EoxsOq25K', 'EouIY1wM0', 'EonMchwJO', 'EomXaqHRF', 'Eoemt29v9', 'Eo57un7mK', 'EnV47bcpX', 'EnUoVfQ16', 'EnpELb4XY', 'EniHSCVAD', 'En9RxlYTs', 'En08eeACU', 'EmSAr6T0E', 'Emzko29RK', 'Emq2f9XF1', 'Emkv1y8ir', 'EmfeCupEo', 'EmfayqB8l', 'Emdnx07Kh', 'Em5jl5BDz', 'Em3FlxxwE', 'ElNnHlvdI', 'ElF1g2u6a', 'ElvYH80xs', 'Eluq2fn2t', 'El8vasfjI', 'El2REt7jZ', 'El1Scsp7n', 'EkTFX9zFW', 'EkT2O1UrI', 'EkStF2g0P', 'EkITeE7d5', 'EkHTToCHq', 'EkhNWFBgK', 'Ekhcwt7pi', 'EkdKykpFv', 'Ek8s2mAWG', 'EjZOmfmJA', 'EjQdv0OVd', 'EjO1RfIxO', 'EjGfMeP5G', 'EjeAIybYU', 'Ej9rzy3WX', 'Ej4fEvJGT', 'Ej3A4BZWy', 'EiLXv9HFi', 'EiAROAe3k', 'Eiye0hhed', 'Eik3Cdwmp', 'Eiessup7k', 'EiantcG0M', 'Ei8R2EykC', 'EhZnDg6LL', 'EhRnFqSEI', 'EhGlOtn6P', 'EhDl3jXYr', 'Ehxbs9siM', 'EhkHelXCP', 'Eh4E2oir5', 'EgTHitMrF', 'EgJgObB4b', 'EgCNZjB9O', 'EglhasmMB', 'Egc2u6TbY', 'EfSlZCCA9', 'EfGiVyYEI', 'EfA4vCosN', 'Efy9ixarE', 'EfqnzF9qU', 'Efcn5CNLj', 'Ef7JHatvp', 'EeYpLtJph', 'EeOXnCw3L', 'EeE1uhQ6w', 'Eev9NqJRr', 'EeuupFqqB', 'EemeH1H71', 'Eelcp6INx', 'Ee3V72wmf', 'Ee3ByytP3', 'EdTnXwNDX', 'EdSQ2vL56', 'EdQnXrgXW', 'EdxAK4Esp', 'EdwSBuCx4', 'EdreHCbAb', 'EdinJ7bD3', 'Ed8hlb65W', 'Ed4SRmzkb', 'EcP4EDqdo', 'EcP1p8tYj']
weibo_ids = ['EAm0GbGCX', 'EAexym6Em', 'EA58gwczN', 'EzVyP4CsB', 'EzTIpcpkU', 'EzRVb2ZQg', 'EzM9zjK30', 'EzCInEaV0', 'Ezavm2M4D', 'Ez11tkeLo', 'EyRzW5MUZ', 'EyIv9dZ2J', 'EyFCw9wws', 'EyyQU6EVn', 'EydAjhFdu', 'Ey6HLC3eC', 'ExX3eu8yd', 'ExOEthuTd', 'ExFeHnmVt', 'ExDV5nO8B', 'Ex2I18qKL', 'EwKgdFjZd', 'Ewr361Wqq', 'EvYPtolMd', 'Evw9c0BYk', 'EuUEbxweq', 'EuC399aDJ', 'Eu6hVoups', 'EsDl9oqXx', 'EskCOhmPd', 'EsbkQ6ZKc', 'Es1tQjOFv', 'Es1mYdtyY', 'ErQ5g7QOF', 'ErzpR8gpF', 'Erq7ACZ5M', 'EqUYNuRQP', 'EqEyU4CEZ', 'EqmjMkJRX', 'EqlxJvLjs', 'Eqkna2N5y', 'Eqczm2Iai', 'EqbpMo2oH', 'EpK8YncsS', 'EpAf17CBj', 'Eps093Fhg', 'Epo95tvxe', 'EphRJuPV0', 'EpfPceeio', 'Ep8Eq36E5', 'EoQqNkMcF', 'EoGUxxnYp', 'EoxsOq25K', 'EouIY1wM0', 'EonMchwJO', 'EomXaqHRF', 'Eoemt29v9', 'Eo57un7mK', 'EnV47bcpX', 'EnUoVfQ16', 'EnpELb4XY', 'EniHSCVAD', 'En9RxlYTs', 'En08eeACU', 'EmSAr6T0E', 'Emzko29RK', 'Emq2f9XF1', 'Emkv1y8ir', 'EmfeCupEo', 'EmfayqB8l', 'Emdnx07Kh', 'Em5jl5BDz', 'Em3FlxxwE', 'ElNnHlvdI', 'ElF1g2u6a', 'ElvYH80xs', 'Eluq2fn2t', 'El8vasfjI', 'El2REt7jZ', 'El1Scsp7n', 'EkTFX9zFW', 'EkT2O1UrI', 'EkStF2g0P', 'EkITeE7d5', 'EkHTToCHq', 'EkhNWFBgK', 'Ekhcwt7pi', 'EkdKykpFv', 'Ek8s2mAWG', 'EjZOmfmJA', 'EjQdv0OVd', 'EjO1RfIxO', 'EjGfMeP5G', 'EjeAIybYU', 'Ej9rzy3WX', 'Ej4fEvJGT', 'Ej3A4BZWy', 'EiLXv9HFi', 'EiAROAe3k', 'Eiye0hhed', 'Eik3Cdwmp', 'Eiessup7k', 'EiantcG0M', 'Ei8R2EykC', 'EhZnDg6LL', 'EhRnFqSEI', 'EhGlOtn6P', 'EhDl3jXYr', 'Ehxbs9siM', 'EhkHelXCP', 'Eh4E2oir5', 'EgTHitMrF', 'EgJgObB4b', 'EgCNZjB9O', 'EglhasmMB', 'Egc2u6TbY', 'EfSlZCCA9', 'EfGiVyYEI', 'EfA4vCosN', 'Efy9ixarE', 'EfqnzF9qU', 'Efcn5CNLj', 'Ef7JHatvp', 'EeYpLtJph', 'EeOXnCw3L', 'EeE1uhQ6w', 'Eev9NqJRr', 'EeuupFqqB', 'EemeH1H71', 'Eelcp6INx', 'Ee3V72wmf', 'Ee3ByytP3', 'EdTnXwNDX', 'EdSQ2vL56', 'EdQnXrgXW', 'EdxAK4Esp', 'EdwSBuCx4', 'EdreHCbAb', 'EdinJ7bD3', 'Ed8hlb65W', 'Ed4SRmzkb', 'EcP4EDqdo', 'EcP1p8tYj']

print(weibo_ids)
print(len(weibo_ids))

for weibo_seed in weibo_ids:
    while not weibo_account_list[i].login():
        weibo_account_list.remove(weibo_account_list[i])
        if len(weibo_account_list) <= i:
            i = 0
        if len(weibo_account_list) is 0:
            weibo_accounts = read_users('weibos')
            for user in weibo_accounts:
                weibo_account_list.append(SinaCrawler(user, weibo_accounts[user]))

    if os.path.isfile('data/' + weibo_seed + '.txt'): 
        os.remove('data/' + weibo_seed + '.txt')
    if os.path.isfile(('data/' + weibo_seed + '.json')):
        os.remove('data/' + weibo_seed + '.json')

    G = nx.DiGraph()
    print('正在爬取：' + weibo_seed)
    crawl_list = [weibo_seed]
    G.add_node (weibo_seed)
    crawled_set = set([])
    results = {}
    while crawl_list: 
        print(crawl_list)
        reposts = {}
        for weibo in crawl_list:
            results[weibo] = weibo_account_list[i].crawl_repost(weibo)
            crawled_set.add(weibo)
        crawl_list = []

        for result in results:
            if results[result] is None:
                if repost['weibo_id'] is not 'weibo.cn':
                    crawl_list.append(result)
                    if result in crawled_set:
                        crawled_set.remove(result)
                    continue
                while not weibo_account_list[i].login():
                    weibo_account_list.remove(weibo_account_list[i])
                    if len(weibo_account_list) <= i:
                        i = 0
                    if len(weibo_account_list) is 0:
                        weibo_accounts = read_users('weibos')
                        for user in weibo_accounts:
                            weibo_account_list.append(SinaCrawler(user, weibo_accounts[user]))
                continue
            for repost in results[result]:
                # print(repost)
                if repost['weibo_id'] not in crawled_set:
                        crawl_list.append(repost['weibo_id'])
                if not repost['from_weibo_id']:     
                    if repost['weibo_id'] is weibo_seed:
                        G.node[repost['weibo_id']]['Content'] = repost['content']
                        G.node[repost['weibo_id']]['uid'] = repost['uid']
                        G.node[repost['weibo_id']]['nickname'] = repost['nickname']
                elif not G.has_node(repost['weibo_id']):    
                    G.add_edge(repost['from_weibo_id'], repost['weibo_id'])  
                    G.node[repost['weibo_id']]['Content'] = repost['content']
                    G.node[repost['weibo_id']]['nickname'] = repost['nickname']
                    G.node[repost['weibo_id']]['uid'] = repost['uid']


    for node in G.nodes():
        G.node[node]['size'] =  math.log((G.out_degree(node) + 1) * 10, 2) * 3
        G.node[node]['in_degree'] = G.in_degree(node)
        G.node[node]['out_degree'] = G.out_degree(node)
        if G.in_degree(node) > 1:
            min_degree = G.out_degree(G.predecessors(node)[0])
            min_node = G.predecessors(node)[0]
            for predecessor in G.predecessors(node):
                if G.out_degree(predecessors) < min_degree:
                    min_degree = G.out_degree(predecessors)
                    min_node = predecessor
            for predecessor in G.predecessors(node):
                if predecessor is min_node:
                    G[predecessor][node]['show'] = True
                else:
                    G[predecessor][node]['show'] = False
        else:
            for predecessor in G.predecessors(node):
                G[predecessor][node]['show'] = True

    with open('data/' + weibo_seed + '.json', "w") as f:
            json.dump(json_graph.node_link_data(G), f)
    with open('data/' + weibo_seed + '.txt', "w") as f:
        for node in G.nodes():
            f.write(node + " "  + str(G.in_degree(node)) + " " + str(G.out_degree(node)))
            f.write('\n')