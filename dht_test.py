import time
import board
import adafruit_dht

dht = adafruit_dht.DHT11(board.D17)

while True:
    try:
        print(f"Temp: {dht.temperature} °C  Humidity: {dht.humidity} %")
    except RuntimeError:
        pass
    time.sleep(2)
