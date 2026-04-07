import pickle
import streamlit as st

@st.cache_data
def load_data(filepath="data/processed/graph.pkl"):
    with open(filepath, "rb") as f:
        graph, coords = pickle.load(f)
    return graph, coords

def get_nearest_node(lat, lon, coords_dict):
    nearest_node = None
    min_dist = float('inf')
    for node_id, (n_lat, n_lon) in coords_dict.items():
        dist = (lat - n_lat)**2 + (lon - n_lon)**2
        if dist < min_dist:
            min_dist = dist
            nearest_node = node_id
    return nearest_node