import json
import pymongo
from datasets import load_dataset

client = pymongo.MongoClient("localhost", 27017)
pref_db = client.humaneval.pref

# clear
print(pref_db.delete_many({}).deleted_count, "deleted")

# dataset = load_dataset("changpt/ko-lima-vicuna", split="train")
dataset = load_dataset("json", data_files="test_input.jsonl")["train"]

print('inserting')
pref_db.insert_many(dataset)