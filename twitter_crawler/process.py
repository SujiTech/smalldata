# -*- encoding:utf-8 -*-

import json
import glob


keys = open('./keyword_list.txt').readlines()
keys = [x[:-1] for x in keys]

for key in keys:
    for u in glob.glob('./tweets/%s/*'%key):
        print(u)
        for f in glob.glob('%s/*'%u):
            a = json.load(open(f))
            des = a['user']['description']
            if u'画家' in des or u'アニメーター' in des or u'脚本' in des or u'ライター' in des or u'イラストレーター' in des:
                print (a['user']['name'])
                print (a['user']['description'])
                print ('------------------------------------------------')
