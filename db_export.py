import json, jsonlines
import pymongo
from tqdm import tqdm

OUTPUT_FILE = "humaneval-lima-12.8b.jsonl"

client = pymongo.MongoClient("localhost", 27017)
pref_db = client.humaneval.pref

with jsonlines.open(OUTPUT_FILE, "w") as fout:
    for item in tqdm(pref_db.find()):
        print(item)
        del item["_id"]
        fout.write(item)



