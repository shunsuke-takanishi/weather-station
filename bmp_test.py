import Adafruit_BMP.BMP085 as BMP085

# ★ busnum=1 を明示
sensor = BMP085.BMP085(busnum=1)

print(f"Pressure: {sensor.read_pressure() / 100:.1f} hPa")
print(f"Temperature: {sensor.read_temperature():.1f} °C")
