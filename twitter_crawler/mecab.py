# -*- coding: utf-8 -*-

import json
import os
import re
import sys

import MeCab

if os.path.exists('data/mecab_parse_result.txt'):
    os.remove('data/mecab_parse_result.txt')

mecab = MeCab.Tagger("")

with open('data/test.txt') as f:
    parse_result = {}
    for line in f:
        twitter = json.loads(line)
        # node = mecab.parseToNode(twitter['text'])
        # node_result = []
        sentence = re.sub('(http|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', ' ', twitter['text'])
        sentence = re.sub('RT.*:', ' ', sentence)
        sentence = re.sub('\@[A-Za-z0-9_]*', ' ', sentence)
        print(sentence)
        with open('data/mecab_parse_result.txt', 'a+') as f:
            f.write("twitter id is: " + twitter['id_str'])
            f.write("\ntwitter is: " + twitter['text'])
            f.write("\n===MeCab Result===\n")
            f.write(mecab.parse(sentence))
            f.write("\n")


        # while node:
            # node_result.append((node.surface, node.feature))
            # node = node.next
        # parse_result[twitter['id_str']] = node_result
        # print(parse_result)

    # json.dump(parse_result, f, ensure_ascii=False)
