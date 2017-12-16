import csv
from pymongo import MongoClient


client = MongoClient(port=27017)
db= client.kol

with open('data/all-kol.csv', 'r') as in_file:
    kol_reader = csv.reader(in_file)
    for row in kol_reader:
        kol_data = {
            'name': row[0], 
            'screen_name': row[1], 
            'description': row[2],
            'followers_count': row[3],
            'friends_count': row[4],
            'statuses_count': row[5],
            'favourites_count': row[6]
        }
        result = db.replace_one({'screen_name': row[1]}, kol_data, True)