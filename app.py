"""
pip install streamlit redis

streamlit run --server.port 7860 --server.address 0.0.0.0 app.py
http://203.253.25.176:35010 으로 접속
"""
import streamlit as st
import pymongo, json
from streamlit_sortables import sort_items

import random
from dataclasses import dataclass


st.set_page_config(layout="wide")

def count_works(db, annotator):
    return db.count_documents({"annotator": annotator})
    # return db.estimated_document_count({"annotator": annotator})

def sample_random(db):
    print("sample")
    item = db.aggregate([
        { "$match": { "state": None } },
        { "$sample": { "size": 1 } }
    ])
    item = list(item)
    if len(item) > 0:
        item = item[0]
        db.update_one({"_id": item["_id"]}, {"$set":{"state":"annotating"}})
        return item
    else:
        return None
    

def ack_item(db, item, annotator, selection):
    db.update_one(
        {"_id": item["_id"]}, 
        {"$set": {
            "state": "finish",
            "annotator": annotator,
            "selection": selection
            }
        })

@st.cache_resource(hash_funcs={pymongo.MongoClient: id})
def connect_to_database():
    return pymongo.MongoClient("localhost", 27017)

@dataclass
class RankingOption:
    label: str
    value: str

    def __str__(self) -> str:
        return label

def prompt_binary(user, outputs):

    if isinstance(user, str):
        with st.chat_message("user"):
            st.write("Human:")
            st.write(user.strip())
    elif isinstance(user, list):
        for conv in user[:-1]:
            if conv["from"] == "human":
                icon, speaker = "user", "Human"
            else:
                icon, speaker = "assistant", "Assistant"

            with st.chat_message(icon):
                st.write(speaker + ":")
                st.markdown(conv["value"])

    random.shuffle(outputs)
    labels = ["A", "B", "C", "D", "E"]
    tabs = st.tabs(labels)

    # outputs.insert(0,)
    for tab, label, option in zip(tabs, labels, outputs):
        with tab, st.chat_message("assistant"):
            st.write(f"{label}:")
            st.markdown(option)


    original_items = [
        {'header': '1',  'items': labels},
        {'header': '2', 'items': []},
        {'header': '3', 'items': []},
        {'header': '4', 'items': []},
        {'header': '5', 'items': []},
    ]

    sorted_items = sort_items(original_items, multi_containers=True, direction="vertical")

    st.write(f'sorted_items: {sorted_items}')

    # options = [
    #     "A를 확실하게 더 선호합니다.",
    #     "A를 약간 더 선호합니다.",
    #     "둘이 비슷합니다.",
    #     "B를 약간 더 선호합니다.",
    #     "B를 확실하게 더 선호합니다.",
    #     "둘 다 별로입니다."
    #     ]
    
    # selection = st.radio(
    #     "A와 B의 답변 중 어떠한 것을 더 선호하시나요?",
    #     options,
    #     index=2
    # )

    return {
        "ranking": sorted_items,
        "options": outputs
    }

def main(annotator):
    if "item" not in st.session_state:
        st.session_state.item = sample_random(db_pref)

    item = st.session_state.item

    with st.form('hi', False):
        selection = prompt_binary(
            item["conversations"],
            [item["conversations"][-1]["value"]] + item["samples"]
        )
        submit = st.form_submit_button("제출")
    skip = st.button("skip")

    if submit:
        ack_item(db_pref, item, annotator, selection)
        st.session_state.count += 1
        print("submit")
        st.session_state.item = sample_random(db_pref)
        st.experimental_rerun()
    
    if skip:
        st.session_state.item = sample_random(db_pref)
        st.experimental_rerun()


db_client = connect_to_database()
db_pref = db_client.humaneval.pref

human_name = st.text_input("평가자명 입력")

if human_name:
    if "count" not in st.session_state:
        st.session_state.count = count_works(db_pref, human_name)
    st.write(f"{st.session_state.count}개 작업하셨습니다")
    main(human_name)
else:
    st.info("평가자명을 입력하세요.")