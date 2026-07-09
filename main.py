from machine import Pin, I2C, ADC
import dht
import time
import ssd1306

# ---------------- SETUP ----------------
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

dht_sensor = dht.DHT22(Pin(15))
mq135 = ADC(26)
buzzer = Pin(16, Pin.OUT)

# ---------------- CALIBRATION ----------------
oled.fill(0)
oled.text("Calibrating...", 0, 20)
oled.show()

time.sleep(3)

baseline = 0
for i in range(10):
    baseline += mq135.read_u16()
    time.sleep(0.2)

baseline = baseline // 10  # average

print("Baseline:", baseline)

# ---------------- VARIABLES ----------------
last_status = ""
last_beep_time = 0
cooldown = 10

# ---------------- MAIN LOOP ----------------
while True:
    try:
        # ---- READ SENSORS ----
        dht_sensor.measure()
        temp = dht_sensor.temperature()
        hum = dht_sensor.humidity()

        gas = mq135.read_u16()
        time.sleep(0.1)
        gas = (gas + mq135.read_u16()) // 2

        # ---- DIFFERENCE FROM BASELINE ----
        diff = gas - baseline

        # ---- LOGIC (RELATIVE VALUES) ----
        if diff > 5000:
            status = "SPOILED"
        elif diff > 2000:
            status = "WARNING"
        else:
            status = "SAFE"

        # ---- BUZZER CONTROL ----
        current_time = time.time()

        if status == "SPOILED":
            if (last_status != "SPOILED") or (current_time - last_beep_time > cooldown):
                buzzer.value(1)
                time.sleep(0.3)
                buzzer.value(0)
                last_beep_time = current_time
        else:
            buzzer.value(0)

        last_status = status

        # ---- DEBUG ----
        print("Gas:", gas, "Baseline:", baseline, "Diff:", diff)
        print("Status:", status)

        # ---- DISPLAY ----
        oled.fill(0)
        oled.text("FridgeGuard", 10, 0)
        oled.text("Temp: {}C".format(temp), 0, 15)
        oled.text("Gas: {}".format(gas), 0, 30)
        oled.text("Diff: {}".format(diff), 0, 40)
        oled.text(status, 40, 55)
        oled.show()

        time.sleep(2)

    except Exception as e:
        print("Error:", e)
        buzzer.value(0)
        time.sleep(2)