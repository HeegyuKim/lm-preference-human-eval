
import streamlit as st
from streamlit_elements import elements, mui, html, dashboard


with elements("dashboard"):
    layout = [
        # Parameters: element_identifier, x_pos, y_pos, width, height, [item properties...]
        dashboard.Item("first_item", 0, 0, 0.5, 1, isDraggable=True, isResizable=False),
        dashboard.Item("second_item", 1, 0, 1, 1, isDraggable=True, isResizable=False),
        dashboard.Item("third_item", 2, 0, 1, 1, isDraggable=True, isResizable=False),
    ]

    def handle_layout_change(updated_layout):
        # You can save the layout in a file, or do anything you want with it.
        # You can pass it back to dashboard.Grid() if you want to restore a saved layout.
        print(updated_layout)

    with dashboard.Grid(layout, onLayoutChange=handle_layout_change):
        mui.Paper("First item", key="first_item")
        mui.Paper("Second item (cannot drag)", key="second_item")
        mui.Paper("Third item (cannot resize)", key="third_item")