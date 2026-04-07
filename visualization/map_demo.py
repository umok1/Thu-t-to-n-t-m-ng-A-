import folium
import os

def draw_map(path_coords, output_file="route.html"):
    if not path_coords or len(path_coords) < 2:
        print("⚠️ Không có đủ tọa độ để vẽ bản đồ!")
        return

    # Khởi tạo bản đồ tại điểm bắt đầu
    # Lưu ý: path_coords[0] phải là (lat, lon)
    m = folium.Map(location=path_coords[0], zoom_start=15)

    # Vẽ đường đi màu đỏ nối các điểm
    folium.PolyLine(path_coords, color="red", weight=5, opacity=0.8).add_to(m)

    # Đánh dấu điểm đầu và điểm cuối
    folium.Marker(
        path_coords[0], 
        popup="Start Node", 
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)
    
    folium.Marker(
        path_coords[-1], 
        popup="End Node", 
        icon=folium.Icon(color="red", icon="stop")
    ).add_to(m)

    # Lưu file
    m.save(output_file)
    print(f"🎉 Đã tạo bản đồ thành công tại: {os.path.abspath(output_file)}")