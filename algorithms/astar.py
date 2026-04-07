import heapq
import math

def haversine(coord1, coord2):
    """
    Tính khoảng cách đường thẳng (đường chim bay) giữa 2 tọa độ (Vĩ độ, Kinh độ).
    Sử dụng công thức Haversine để quy đổi ra đơn vị Mét (khớp với đơn vị length của OSM).
    """
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371000  # Bán kính Trái Đất (tính bằng mét)

    # Đổi từ độ sang radian
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Áp dụng công thức Haversine
    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c  # Trả về khoảng cách bằng mét

def astar(graph, coords, start, end):
    """
    Thuật toán tìm đường đi ngắn nhất A*.
    Trả về một Tuple: (path, explored_nodes)
      - path: Danh sách các ID của node từ Start đến End.
      - explored_nodes: Danh sách các điểm đã duyệt qua để vẽ lên bản đồ.
    """
    # 1. KHỞI TẠO
    # Hàng đợi ưu tiên (Priority Queue) để luôn ưu tiên xét node có f_score thấp nhất
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    # Set dùng để tra cứu nhanh xem một node có đang nằm trong open_set hay không
    open_set_hash = {start}
    
    # Từ điển dùng để truy vết lại con đường sau khi đã đến đích
    came_from = {}
    
    # g_score: Chi phí thực tế (quãng đường) đi từ Start đến node hiện tại
    g_score = {start: 0}
    
    # f_score: Chi phí dự đoán từ Start đến End (bằng g_score + heuristic)
    f_score = {start: haversine(coords[start], coords[end])}
    
    # Danh sách lưu lại toàn bộ quá trình thuật toán lan tỏa (để vẽ mây màu xanh)
    explored_nodes = []

    # 2. VÒNG LẶP DUYỆT TÌM ĐƯỜNG
    while open_set:
        # Lấy node có f_score thấp nhất ra khỏi hàng đợi để xét
        current_f, current = heapq.heappop(open_set)
        open_set_hash.remove(current)
        
        # Ghi nhận: "Tôi đã đi qua điểm này"
        explored_nodes.append(current)

        # --- NẾU ĐÃ TỚI ĐÍCH ---
        if current == end:
            path = []
            # Lần ngược lại dấu vết từ Đích về Xuất phát thông qua 'came_from'
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            
            # Đảo ngược mảng để trả về đúng thứ tự: Start -> ... -> End
            path.reverse() 
            
            return path, explored_nodes

        # --- XÉT CÁC ĐIỂM HÀNG XÓM ---
        # graph.get(current, []) lấy ra danh sách các điểm nối trực tiếp với current
        for neighbor, distance in graph.get(current, []):
            
            # Quãng đường từ Start -> current -> neighbor
            tentative_g_score = g_score[current] + distance
            
            # Nếu tìm được đường đến neighbor ngắn hơn những gì từng biết 
            # (hoặc đây là lần đầu tiên tìm thấy neighbor)
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                
                # Ghi nhớ đường đi ngắn nhất này
                came_from[neighbor] = current
                
                # Cập nhật chi phí thực tế (G)
                g_score[neighbor] = tentative_g_score
                
                # Tính lại chi phí dự tính tới đích (F = G + H)
                h_score = haversine(coords[neighbor], coords[end])
                f_score[neighbor] = tentative_g_score + h_score
                
                # Nếu neighbor chưa nằm trong danh sách chờ duyệt thì đẩy nó vào
                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)

    # 3. KẾT THÚC
    # Nếu vòng lặp chạy hết mà không chạm được tới dòng `if current == end`
    # Nghĩa là không có đường nào kết nối Start và End
    return None, explored_nodes