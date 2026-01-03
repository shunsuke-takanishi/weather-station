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

# ===== センサー =====
dht = adafruit_dht.DHT11(board.D17)
bmp = BMP085.BMP085(busnum=1)

# ===== データ保持 =====
pressure_hist = collections.deque(maxlen=WINDOW)
humidity_hist = collections.deque(maxlen=WINDOW)

print("Weather monitor (practical mode) started")

while True:
    try:
        hum = dht.humidity
        pres = bmp.read_pressure() / 100.0  # hPa

        if hum is None:
            raise RuntimeError

        pressure_hist.append(pres)
        humidity_hist.append(hum)

        # 移動平均
        p_avg = sum(pressure_hist) / len(pressure_hist)
        h_avg = sum(humidity_hist) / len(humidity_hist)

        # 気圧低下量
        dp = p_avg - pres

        # 判定
        status = "Stable"

        if h_avg >= HUMIDITY_HIGH and dp >= PRESSURE_DROP_ALERT:
            status = "RAIN LIKELY"
        elif h_avg >= 70 and dp >= PRESSURE_DROP_WARN:
            status = "Rain possible"

        print(
            f"Humidity(avg): {h_avg:.1f}% | "
            f"Pressure: {pres:.1f} hPa | "
            f"ΔP(avg-now): {dp:.2f} hPa | "
            f"Status: {status}"
        )

    except RuntimeError:
        pass

    time.sleep(INTERVAL)
