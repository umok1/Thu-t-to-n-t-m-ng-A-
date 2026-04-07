import pickle
import random
from algorithms.astar import astar
from visualization.map_demo import draw_map

# load graph
with open("data/processed/graph.pkl", "rb") as f:
    graph, coords = pickle.load(f)

nodes = list(graph.keys())

# 🔥 chọn ngẫu nhiên nhưng đảm bảo có edge
start = random.choice(nodes)
end = random.choice(nodes)

print("Start:", start)
print("End:", end)

# chạy A*
path = astar(graph, coords, start, end)

# nếu không tìm được → thử lại
attempt = 0
while path is None and attempt < 10:
    start = random.choice(nodes)
    end = random.choice(nodes)
    print("🔁 Thử lại:", start, "→", end)
    path = astar(graph, coords, start, end)
    attempt += 1

if path is None:
    print("❌ Không tìm được đường sau nhiều lần thử")
    exit()

print("✅ Tìm được đường, số node:", len(path))

# chuyển sang tọa độ
path_coords = [coords[n] for n in path]

# vẽ map
draw_map(path_coords)

print("🎉 Đã tạo route.html")