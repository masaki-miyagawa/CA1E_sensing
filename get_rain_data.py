import requests
import json
import time

# --- パラメータ設定 ---
API_KEY = "71af64b26516f81c972af113ad60d644"  # ★自分のOpenWeatherMapのAPIキーを入れてね

# 指定する矩形エリア（左下と右上の緯度経度）
lat_min = 22.114645  # 南側（小さいほう）
lon_min = 121.840587  # 西側（小さいほう）
lat_max = 23.143890   # 北側（大きいほう）
lon_max = 123.049083  # 東側（大きいほう）

# グリッド分割数
GRID_N = 7  # 7x7に分割

# 出力先ファイル
OUTPUT_FILE = "rain_data.json"

# --- グリッド地点リスト作成 ---
lat_list = [lat_min + (lat_max - lat_min) * i / (GRID_N - 1) for i in range(GRID_N)]
lon_list = [lon_min + (lon_max - lon_min) * j / (GRID_N - 1) for j in range(GRID_N)]

# --- データ取得 ---
results = []

for lat in lat_list:
    for lon in lon_list:
        # OpenWeatherMap API呼び出し
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            rain = data.get("rain", {}).get("1h", 0)  # 1時間の降水量（mm）、なければ0
            clouds = data.get("clouds", {}).get("all", None)  # 雲密度（%）、なければNone

            weather = {
                "lat": lat,
                "lon": lon,
                "rain_mm": rain,
                "cloudiness_percent": clouds,
                "timestamp": data.get("dt")
            }
            print(weather)  # 途中経過出力
            results.append(weather)
        else:
            print(f"Error at {lat},{lon}: {response.status_code}")
        
        time.sleep(0.5)  # ちょっと待ってAPI制限回避（安全策）

# --- JSONファイル保存 ---
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"完了！データを {OUTPUT_FILE} に保存しました✨")
