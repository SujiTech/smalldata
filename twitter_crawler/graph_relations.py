import json

import networkx as nx
from networkx.readwrite import json_graph

G = nx.DiGraph()
data = {}
with open('data/followers.txt') as f:
    for line in f:
        data.update(eval(line))

for key in data.keys():
    for value in data[key]:
        G.add_edge(value, key)

# with open('data/twitter_relation.json', 'w') as f:
#     json.dump(json_graph.node_link_data(G), f)
