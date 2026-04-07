import streamlit as st
import folium
import streamlit.components.v1 as components
from streamlit_folium import st_folium

from algorithms.astar import astar
from utils.data_helper import load_data, get_nearest_node
from visualization.map_html import generate_animation_html

# 1. Cấu hình & Tải dữ liệu
st.set_page_config(page_title="A* Pathfinding Map", layout="wide")
st.title("🗺️ Tìm đường A* trên bản đồ")

graph, coords = load_data()
first_node = list(coords.keys())[0]
center_lat_lon = coords[first_node]

# 2. Khởi tạo Session State
if "start_point" not in st.session_state:
    st.session_state.start_point = None
if "end_point" not in st.session_state:
    st.session_state.end_point = None

if st.button("🔄 Reset"):
    st.session_state.start_point = None
    st.session_state.end_point = None
    st.rerun()

# 3. Phân luồng giao diện
if st.session_state.start_point and st.session_state.end_point:
    # KHI ĐÃ CÓ ĐỦ 2 ĐIỂM -> CHẠY THUẬT TOÁN & ANIMATION
    start_node = get_nearest_node(st.session_state.start_point[0], st.session_state.start_point[1], coords)
    end_node = get_nearest_node(st.session_state.end_point[0], st.session_state.end_point[1], coords)
    
    path, explored = astar(graph, coords, start_node, end_node)
    
    if explored:
        explored_coords = [coords[n] for n in explored]
        path_coords = [coords[n] for n in path] if path else []
        
        # Gọi hàm tạo HTML từ file map_html.py
        map_html = generate_animation_html(
            center_lat_lon[0], center_lat_lon[1],
            st.session_state.start_point[0], st.session_state.start_point[1],
            st.session_state.end_point[0], st.session_state.end_point[1],
            explored_coords, path_coords
        )
        components.html(map_html, height=500, scrolling=False)        
        if path:
            st.success(f"✅ Đã tìm thấy! (Duyệt qua {len(explored)} ngã tư, đường đi gồm {len(path)} điểm)")
        else:
            st.error("❌ Không có đường nối đến đích!")

else:
    # KHI CHƯA CHỌN ĐỦ ĐIỂM -> HIỂN THỊ BẢN ĐỒ TƯƠNG TÁC
    m = folium.Map(location=center_lat_lon, zoom_start=14)
    
    if st.session_state.start_point:
        folium.Marker(st.session_state.start_point, icon=folium.Icon(color="green", icon="play")).add_to(m)
    if st.session_state.end_point:
        folium.Marker(st.session_state.end_point, icon=folium.Icon(color="red", icon="stop")).add_to(m)

    map_data = st_folium(m, width=800, height=500, key="interactive_map")

    # Bắt sự kiện click
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
        
        if st.session_state.start_point is None:
            st.session_state.start_point = (lat, lon)
            st.rerun()
        elif st.session_state.end_point is None:
            st.session_state.end_point = (lat, lon)
            st.rerun()