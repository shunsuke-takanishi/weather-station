## System Overview

This project is a simple weather monitoring system running on a Raspberry Pi.
It detects rain precursors using **humidity** and **barometric pressure trends**.

### Components
- Raspberry Pi 4 Model B
- BMP180 Barometric Pressure Sensor (I2C)
- DHT11 Temperature & Humidity Sensor (GPIO)
- Jumper wires

---

## Architecture

- **Raspberry Pi**
  - Collects sensor data
  - Calculates moving averages
  - Evaluates rain likelihood

- **BMP180**
  - Measures barometric pressure (primary signal for rain prediction)
  - Connected via I2C

- **DHT11**
  - Measures ambient humidity (supporting signal)
  - Connected via single-wire digital GPIO

---

## Wiring Diagram (Logical)

### BMP180 (I2C)

| BMP180 Pin | Raspberry Pi Pin | Notes |
|-----------|------------------|------|
| VCC       | 3.3V (Pin 1)     | **3.3V only** |
| GND       | GND (Pin 9)      | Common ground |
| SDA       | SDA (Pin 3)      | I2C data |
| SCL       | SCL (Pin 5)      | I2C clock |

### DHT11 (Digital GPIO)

| DHT11 Pin | Raspberry Pi Pin | Notes |
|-----------|------------------|------|
| VCC       | 3.3V (Pin 17)     | Module has onboard resistor |
| DATA      | GPIO17 (Pin 11)  | Single-wire digital signal |
| GND       | GND (Pin 20)      | Common ground |

> All sensors share the same **3.3V** and **GND** rails.

---

## Physical Wiring Notes

- Use **3.3V only** (do NOT use 5V)
- Keep wires short to reduce noise
- I2C devices can share SDA/SCL lines
- DHT11 timing is sensitive; unstable readings are normal

---

## Sensor Roles

| Sensor | Used For | Notes |
|------|---------|------|
| BMP180 | Pressure trend | Primary rain predictor |
| DHT11 | Humidity | Secondary confirmation |
| Temperature | Display only | Not used in logic |

---

## Software Flow

1. Read humidity (DHT11)
2. Read pressure (BMP180)
3. Store values in rolling window
4. Compute moving averages
5. Detect pressure drop + high humidity
6. Output rain likelihood

---

## Supported Environment

- Raspberry Pi OS (Bookworm)
- Python 3.11
- I2C enabled (`raspi-config`)
