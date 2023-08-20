import json
import pymongo
from datasets import load_dataset

client = pymongo.MongoClient("localhost", 27017)
pref_db = client.humaneval.pref


states = pref_db.aggregate([
    {"$group" : {"_id":"$state", "count":{"$sum":1}}}
])

print("states")
for row in states:
    print(row)


states = pref_db.aggregate([
    {"$group" : {"_id":"$annotator", "count":{"$sum":1}}}
])

print("annotator")
for row in states:
    print(row)