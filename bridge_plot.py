import json
import folium

# JSONファイルを読み込む
with open("osm_bridge_ways.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 地図の中心（例：東京湾）
center_lat = (35.390583 + 35.667192) / 2
center_lon = (139.663983 + 139.981214) / 2
m = folium.Map(location=[center_lat, center_lon], zoom_start=12)

# IDをキーにノード位置を保持
node_positions = {}

# まずノードの位置情報を保存
for element in data["elements"]:
    if element["type"] == "node":
        node_positions[element["id"]] = (element["lat"], element["lon"])

# 次に、橋（node, way）を描画
for element in data["elements"]:
    tags = element.get("tags", {})
    if "bridge" not in tags:
        continue

    bridge_type = tags.get("bridge", "unknown")
    name = tags.get("name", "no name")

    if element["type"] == "node":
        lat = element.get("lat")
        lon = element.get("lon")
        folium.Marker(
            location=[lat, lon],
            popup=f"橋の名前: {name}<br>種類: {bridge_type}",
            icon=folium.Icon(color="blue", icon="road")
        ).add_to(m)

    elif element["type"] == "way":
        coords = []
        for node_id in element.get("nodes", []):
            if node_id in node_positions:
                coords.append(node_positions[node_id])
        if coords:
            folium.PolyLine(
                locations=coords,
                color="blue",
                weight=4,
                tooltip=name
            ).add_to(m)

# 地図を保存
m.save("bridges_map.html")
print("地図を保存しました: bridges_map.html")
