# insert_devices.py
import sqlite3

conn = sqlite3.connect("database2.db")
cursor = conn.cursor()

devices = [
    ("ac_01", "AC1", "Bedroom", "AC", 2800),
    ("ac_02", "AC2", "Living Room", "AC", 2500),
    ("ac_03", "AC3", "Kitchen", "AC", 2800),
    ("mw_01", "Microwave", "Kitchen", "Microwave", 1600),
    ("rf_01", "Refrigerator", "Kitchen", "Refrigerator", 500),
    ("dw_01", "Dishwasher", "Kitchen", "Dishwasher", 2400),
    ("sp_01", "SmartPlug1", "Living Room", "Smart Plug", 180),
    ("wm_01", "WashingMachine", "Laundry Room", "Washing Machine", 2000),
    ("tv_01", "TV", "Living Room", "TV", 120),
    ("lt_01", "Light1", "Living Room", "Light", 60),
    ("lt_02", "Light2", "Kitchen", "Light", 60),
    ("lt_03", "Light3", "Bedroom", "Light", 60),
    ("lt_04", "Light4", "Bathroom", "Light", 60),
    ("lt_05", "Light5", "Office", "Light", 50),
    ("lt_06", "Light6", "Garage", "Light", 70),
]

cursor.executemany("""
INSERT OR IGNORE INTO devices (switch_id, name, location, device_type, max_power_rating)
VALUES (?, ?, ?, ?, ?)
""", devices)

conn.commit()
conn.close()
print("✅ Devices inserted successfully")
