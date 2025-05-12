import requests
import json

# Overpass APIのURL
url = "https://overpass-api.de/api/interpreter"

# 欲しいエリア（東京湾例）
south = 35.4274
west = 139.6905
north = 35.6668
east = 139.9820

# Overpass QL クエリ
query = f"""
[out:json][timeout:25];
(
  node["seamark:type"="buoy_lateral"]({south},{west},{north},{east});
  node["seamark:type"="buoy_cardinal"]({south},{west},{north},{east});
  node["seamark:type"="buoy_isolated_danger"]({south},{west},{north},{east});
  node["seamark:type"="buoy_safe_water"]({south},{west},{north},{east});
  node["seamark:type"="buoy_special_purpose"]({south},{west},{north},{east});
  node["seamark:type"="light_minor"]({south},{west},{north},{east});
  node["seamark:type"="light_major"]({south},{west},{north},{east});
  node["seamark:type"="light_float"]({south},{west},{north},{east});
);
out body;
"""

# POSTリクエスト送信
response = requests.post(url, data={"data": query})
data = response.json()

# 保存
with open("openseamap_buoys_lights.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("データ保存完了！🎉")

# 取得データをターミナルに出力
print("\n--- 取得結果 ---\n")
for element in data["elements"]:
    lat = element.get("lat")
    lon = element.get("lon")
    tags = element.get("tags", {})
    seamark_type = tags.get("seamark:type", "unknown")
    colour = tags.get("seamark:colour", "unknown")
    shape = tags.get("seamark:shape", "unknown")
    name = tags.get("name", "no name")

    print(f"種類: {seamark_type}, 緯度: {lat}, 経度: {lon}, 色: {colour}, 形状: {shape}, 名前: {name}")
