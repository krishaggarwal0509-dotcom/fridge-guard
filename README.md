# fridge-guard
# 🧊 FridgeGuard – Smart Spoilage Detection

FridgeGuard is a **MicroPython-powered IoT system** that monitors food freshness inside refrigerators. Using a **MQ-135 gas sensor** and **DHT22 temperature/humidity sensor**, it detects spoilage gases and environmental changes, then alerts users through an **OLED display** and a **smart buzzer**.

---

## 🚀 Features
- Real-time monitoring of gas levels and temperature/humidity  
- Adaptive baseline calibration to reduce false alarms  
- OLED interface with live status updates  
- Smart buzzer alerts with cooldown to avoid noise spam  
- Robust error handling for sensor failures  

---

## 🛠️ Hardware Setup

| Component      | GPIO Pin | Interface   |
|----------------|----------|-------------|
| OLED SCL       | GP1      | I2C (Bus 0) |
| OLED SDA       | GP0      | I2C (Bus 0) |
| DHT22 Sensor   | GP15     | Digital In  |
| MQ-135 Sensor  | GP26     | Analog In   |
| Buzzer         | GP16     | Digital Out |

---

## ⚙️ How It Works
1. **Calibration** – Takes 10 initial readings to set a baseline for local air quality.  
2. **Monitoring** – Continuously compares live gas readings against baseline.  
3. **Decision Logic**  
   - `diff > 15,000` → **SPOILED** (critical)  
   - `diff > 8,000` → **WARNING** (check food)  
   - Else → **SAFE**  
4. **Alerts** – OLED updates every 2s; buzzer triggers only on spoilage with cooldown.  
5. **Error Handling** – System retries gracefully if sensors disconnect.  

---

---

## 📦 Applications
- Household refrigerators  
- Cold storage warehouses  
- Food logistics & supply chain monitoring  
- Smart kitchens  

---

## 🔮 Future Improvements
- Mobile app notifications  
- Cloud dashboard for remote monitoring  
- AI-based spoilage prediction  
- PCB design for commercial deployment  

---

## 👨‍💻 Built With
- **MicroPython**  
- **MQ-135 Gas Sensor**  
- **DHT22 Sensor**  
- **SSD1306 OLED Display**  

---

## 🏷️ License
This project is open-source. Feel free to fork, modify, and improve FridgeGuard.


