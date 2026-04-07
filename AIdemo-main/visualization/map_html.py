import json

def generate_animation_html(center_lat, center_lon, start_lat, start_lon, end_lat, end_lon, explored_coords, path_coords, batch_size=10):
    """Tạo mã HTML và JavaScript để render bản đồ động Leaflet"""
    
    # Chuyển đổi dữ liệu sang JSON một lần duy nhất để tránh lỗi định dạng trong JS
    explored_json = json.dumps(explored_coords)
    path_json = json.dumps(path_coords)
    
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            /* Dùng {{ }} kép để thoát khỏi f-string của Python */
            * {{ box-sizing: border-box; }}
            
            body, html {{ 
                margin: 0; 
                padding: 0; 
                height: 100%; 
                width: 100%;
                overflow: hidden; 
            }}
            
            #map {{ 
                height: 500px; 
                width: 100%; 
                border: none; 
            }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            // 1. Khởi tạo bản đồ
            var map = L.map('map').setView([{center_lat}, {center_lon}], 14);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                maxZoom: 19
            }}).addTo(map);

            // 2. Thêm Marker Start/End
            L.marker([{start_lat}, {start_lon}]).addTo(map).bindPopup("Start");
            L.marker([{end_lat}, {end_lon}]).addTo(map).bindPopup("End");

            // 3. Dữ liệu từ Python
            var explored = {explored_json};
            var path = {path_json};

            var currentIndex = 0;
            var batchSize = {batch_size};

            // 4. Hàm vẽ animation mượt mà
            function animateSearch() {{
                for (var step = 0; step < batchSize && currentIndex < explored.length; step++, currentIndex++) {{
                    L.circleMarker(explored[currentIndex], {{
                        radius: 3, 
                        color: '#89CFF0', 
                        fillOpacity: 0.6, 
                        stroke: false
                    }}).addTo(map);
                }}

                if (currentIndex < explored.length) {{
                    requestAnimationFrame(animateSearch);
                }} else {{
                    if (path.length > 0) {{
                        L.polyline(path, {{color: 'red', weight: 6, opacity: 0.8}}).addTo(map);
                    }}
                }}
            }}

            animateSearch(); 
        </script>
    </body>
    </html>
    """
    return html_code