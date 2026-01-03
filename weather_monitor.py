import csv
import os
from datetime import datetime
import time
import collections
import board
import adafruit_dht
import Adafruit_BMP.BMP085 as BMP085

# ===== 設定 =====
INTERVAL = 60            # 秒（1分ごと）
WINDOW = 180             # 3時間 = 180分
HUMIDITY_HIGH = 75
PRESSURE_DROP_WARN = 1.0
PRESSURE_DROP_ALERT = 2.0
PRESSURE_SLOPE_WARN = 0.5    # hPa/hour
PRESSURE_SLOPE_ALERT = 1.0  # hPa/hour
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "weather_log.csv")

# ===== センサー =====
dht = adafruit_dht.DHT11(board.D17)
bmp = BMP085.BMP085(busnum=1)

# ===== データ保持 =====
os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "timestamp",
            "temperature_c",
            "humidity_percent",
            "pressure_hpa",
            "delta_pressure_hpa",
            "pressure_slope_hpa_per_hour",
            "status"
        ])

pressure_hist = collections.deque(maxlen=WINDOW)
humidity_hist = collections.deque(maxlen=WINDOW)

print("Weather monitor (practical mode) started")

while True:
    try:
        hum = dht.humidity
        pres = bmp.read_pressure() / 100.0  # hPa
        temp = bmp.read_temperature()   # °C

        if hum is None:
            raise RuntimeError

        pressure_hist.append(pres)
        humidity_hist.append(hum)

        if len(pressure_hist) < WINDOW:
            time.sleep(INTERVAL)
            continue

        # 移動平均
        p_avg = sum(pressure_hist) / len(pressure_hist)
        h_avg = sum(humidity_hist) / len(humidity_hist)

        # 気圧低下量
        dp = p_avg - pres
        p_old = pressure_hist[0]
        hours = (WINDOW * INTERVAL) / 3600.0
        slope = (p_old - pres) / hours  # hPa/hour

        # 判定
        status = "Stable"

#        if h_avg >= HUMIDITY_HIGH and dp >= PRESSURE_DROP_ALERT:
#            status = "RAIN LIKELY"
#        elif h_avg >= 70 and dp >= PRESSURE_DROP_WARN:
#            status = "Rain possible"

        if h_avg >= HUMIDITY_HIGH and slope >= PRESSURE_SLOPE_ALERT:
            status = "RAIN LIKELY"
        elif h_avg >= 70 and slope >= PRESSURE_SLOPE_WARN:
            status = "Rain possible"


        print(
            f"Temp: {temp:.1f} °C | "
            f"Humidity(avg): {h_avg:.1f}% | "
            f"Pressure: {pres:.1f} hPa | "
#            f"ΔP(avg-now): {dp:.2f} hPa | "
            f"Slope: {slope:.2f} hPa/h | "
            f"Status: {status}"
        )

        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                 round(temp, 1),          # temperature_c（BMP180）
                 round(h_avg, 1),         # 平均湿度
                 round(pres, 1),          # 現在気圧
                 round(dp, 2),            # ΔP
                 round(slope, 2),         # 気圧の傾き
                 status
            ])

    except RuntimeError:
        pass

    time.sleep(INTERVAL)
