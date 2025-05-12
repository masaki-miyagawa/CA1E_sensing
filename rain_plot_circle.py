import folium
import json

# --- ファイル読み込み ---
with open("rain_data.json", "r", encoding="utf-8") as f:
    rain_data = json.load(f)

# --- 地図の中心座標を計算（最初に表示される場所） ---
center_lat = sum([item["lat"] for item in rain_data]) / len(rain_data)
center_lon = sum([item["lon"] for item in rain_data]) / len(rain_data)

# --- folium地図オブジェクト作成 ---
m = folium.Map(location=[center_lat, center_lon], zoom_start=10)

# --- 雨量によってマーカー色分け ---
def get_color(rain_mm):
    if rain_mm == 0:
        return "green"
    elif rain_mm < 2:
        return "blue"
    elif rain_mm < 3:
        return "yellow"
    elif rain_mm < 5:
        return "orange"
    else:
        return "red"

# --- マーカー追加 ---
for item in rain_data:
    lat = item["lat"]
    lon = item["lon"]
    cloudiness = item.get("cloudiness_percent", 0)

    # 雲密度が80%以上なら実際の雨量を使用、そうでなければ0とみなす
    if cloudiness >= 80:
        rain_mm = item.get("rain_mm", 0)
    else:
        rain_mm = 0  # 降っていないとみなす

    color = get_color(rain_mm)

    folium.CircleMarker(
        location=[lat, lon],
        radius=8,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=(
            f"Cloudiness: {cloudiness}%<br>"
            f"Rain: {rain_mm} mm"
        )
    ).add_to(m)

# --- 地図保存 ---
m.save("rain_map.html")

print("✅ マップを rain_map.html に保存しました！ブラウザで開いて確認してね✨")
