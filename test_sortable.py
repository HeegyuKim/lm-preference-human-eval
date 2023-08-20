
import streamlit as st
from streamlit_sortables import sort_items

original_items = [
    {'header': '1',  'items': ['A', 'B', 'C', 'D', 'E']},
    {'header': '2', 'items': []},
    {'header': '3', 'items': []},
    {'header': '4', 'items': []},
    {'header': '5', 'items': []},
]

sorted_items = sort_items(original_items, multi_containers=True, direction="vertical")

st.write(f'original_items: {original_items}')
st.write(f'sorted_items: {sorted_items}')