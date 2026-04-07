import osmnx as ox
import pickle
import os

INPUT_FILE = "data/raw/map.osm"
OUTPUT_FILE = "data/processed/graph.pkl"

# Tạo thư mục nếu chưa có
os.makedirs("data/processed", exist_ok=True)

print("🔄 Đang đọc file OSM...")
if not os.path.exists(INPUT_FILE):
    print(f"❌ Không tìm thấy file: {INPUT_FILE}")
    exit()

# Load file OSM
G = ox.graph_from_xml(INPUT_FILE)

print("✔️ Load xong")
print("Nodes:", len(G.nodes))
print("Edges:", len(G.edges))

if len(G.nodes) == 0:
    print("❌ File OSM không có dữ liệu!")
    exit()

# =========================
# Build graph & coords
# =========================
graph = {}
coords = {}

# Lưu tọa độ: y là vĩ độ, x là kinh độ
for node, data in G.nodes(data=True):
    coords[node] = (data["y"], data["x"])

for u, v, data in G.edges(data=True):
    length = data.get("length", 1)
    # OSMNX đôi khi để oneway là chuỗi "yes"/"no" hoặc boolean
    oneway = data.get("oneway", False)
    if isinstance(oneway, str):
        oneway = True if oneway == 'yes' else False

    # Thêm chiều thuận u -> v
    if u not in graph: graph[u] = []
    graph[u].append((v, length))

    # Nếu không phải đường 1 chiều, thêm chiều ngược v -> u
    if not oneway:
        if v not in graph: graph[v] = []
        # Kiểm tra tránh trùng lặp cạnh u-v đã có
        if u not in [n for n, c in graph[v]]:
            graph[v].append((u, length))

print(f"✔️ Nodes: {len(coords)} | Nodes with edges: {len(graph)}")

# =========================
# Lưu file (PHẦN QUAN TRỌNG)
# =========================
print("💾 Đang lưu dữ liệu vào graph.pkl...")
try:
    with open(OUTPUT_FILE, "wb") as f:
        # Giao thức protocol=pickle.HIGHEST_PROTOCOL giúp ghi file nhanh và ổn định hơn
        pickle.dump((graph, coords), f, protocol=pickle.HIGHEST_PROTOCOL)
    
    # Kiểm tra lại dung lượng file ngay sau khi ghi
    file_size = os.path.getsize(OUTPUT_FILE)
    if file_size > 0:
        print(f"🎉 Thành công! File lưu tại: {OUTPUT_FILE} ({file_size} bytes)")
    else:
        print("⚠️ Cảnh báo: File graph.pkl được tạo ra nhưng dung lượng bằng 0!")
except Exception as e:
    print(f"❌ Lỗi khi lưu file: {e}")