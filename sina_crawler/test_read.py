import json
import ast


with open('2718604160_fans.txt', "r") as f:
    fan_set = set([])
    for line in f:
        data = ast.literal_eval(line)
        # print(data)
        fan_set = fan_set.union(data)

    print(fan_set)
    print(len(fan_set))