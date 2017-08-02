import json

with open('test.txt', "r+") as f:
    for line in f:
        data = json.loads(line)
        print data