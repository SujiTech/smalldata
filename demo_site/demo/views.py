from django.http import HttpResponse
from django.shortcuts import render
import os
import json
import networkx as nx
from networkx.readwrite import json_graph


STATIC_PATH = '/home/yimi/smalldata/demo_site/static'

def index(request):
    WEIBO_PATH = os.path.join(STATIC_PATH ,'weibo-data')
    filelist={}
    users = [user for user in os.listdir(WEIBO_PATH) if os.path.isdir(os.path.join(WEIBO_PATH,user))]
    for user in users:
        weibo_list = []
        for weibo in os.listdir(os.path.join(WEIBO_PATH, user)):
            with open(os.path.join(WEIBO_PATH, user+'/'+weibo)) as f:
                G = json_graph.node_link_graph(json.load(f))
            weibo_list.append((weibo[:-5], G.node[weibo[:-5]]['Content'], user+'/'+weibo[:-5]))
            
        weibo_list.sort(key=lambda x: x[0].swapcase(), reverse=True)
        filelist[user] = weibo_list
    return render(request, 'weibo-demo.html', {'filelist': filelist})

def demo(request, user_id, weibo_id):
    return render(request, 'weibo-demo/demo.html', {'userid': user_id, 'weiboid': weibo_id})