import requests
import json

# Overpass APIエンドポイント
url = "https://overpass-api.de/api/interpreter"

# 対象エリア（例：東京湾周辺）
south = 35.390583
west = 139.663983
north = 35.667192
east = 139.981214

# Overpass QL クエリ：wayのみ取得
query = f"""
[out:json][timeout:25];
way["bridge"]({south},{west},{north},{east});
out body;
>;
out skel qt;
"""

# APIにPOSTリクエストを送信
response = requests.post(url, data={"data": query})
data = response.json()

# 結果をファイルに保存
with open("osm_bridge_ways.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("ウェイ橋データの取得完了！🌉")

# 概要出力
print("\n--- 取得したウェイ橋の一覧 ---\n")
for element in data["elements"]:
    if element["type"] == "way" and "tags" in element and "bridge" in element["tags"]:
        bridge_type = element["tags"].get("bridge", "unknown")
        name = element["tags"].get("name", "no name")
        print(f"ID: {element['id']}, タイプ: {bridge_type}, 名前: {name}")
