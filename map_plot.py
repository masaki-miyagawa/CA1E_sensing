import folium
import json

# JSONファイル読み込み
with open("openseamap_buoys_lights.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 地図の中心
m = folium.Map(location=[35.55, 139.80], zoom_start=10)

# seamark:typeに応じた色を決める関数
def get_marker_color(seamark_type):
    if seamark_type == "buoy_lateral":
        return "blue"
    elif seamark_type == "buoy_cardinal":
        return "green"
    elif seamark_type == "buoy_isolated_danger":
        return "red"
    elif seamark_type == "buoy_safe_water":
        return "white"
    elif seamark_type == "buoy_special_purpose":
        return "orange"
    elif seamark_type in ["light_minor", "light_major", "light_float"]:
        return "purple"
    else:
        return "gray"

# 各データを地図にマッピング
for element in data["elements"]:
    lat = element.get("lat")
    lon = element.get("lon")
    tags = element.get("tags", {})
    seamark_type = tags.get("seamark:type", "unknown")
    name = tags.get("name", "")

    color = get_marker_color(seamark_type)
    popup_text = f"{seamark_type}<br>{name}"

    folium.Marker(
        location=[lat, lon],
        popup=popup_text,
        icon=folium.Icon(color=color, icon="info-sign")
    ).add_to(m)

# HTMLに保存
m.save("buoys_and_lights_colored_map.html")

print("色分けした地図ファイルを作成しました！🎉 → buoys_and_lights_colored_map.html")
