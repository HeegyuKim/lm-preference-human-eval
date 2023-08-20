import json
import pymongo
from datasets import load_dataset

client = pymongo.MongoClient("localhost", 27017)
pref_db = client.humaneval.pref

updated = pref_db.update_many(
    {"state": "annotating"},
    {"$set": {"state": None}}
)
print(updated.modified_count, "items are updated")