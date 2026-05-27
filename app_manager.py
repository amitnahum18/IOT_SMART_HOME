import paho.mqtt.client as mqtt
import sqlite3
from datetime import datetime
from icecream import ic
import logging
from mqtt_init import *

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Manager")

def init_db():
    """Initializes the SQLite database and creates the necessary tables."""
    conn = sqlite3.connect("irrigation_system.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS moisture_logs 
                      (timestamp TEXT, value REAL, status TEXT)''')
    conn.commit()
    conn.close()
    ic("Database initialized")

def save_to_db(value, status):
    """Saves a single telemetry record to the local database."""
    conn = sqlite3.connect("irrigation_system.db")
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO moisture_logs VALUES (?, ?, ?)", (timestamp, value, status))
    conn.commit()
    conn.close()

def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the broker."""
    payload = msg.payload.decode()
    topic = msg.topic
    ic(f"Message received from {topic}: {payload}")
    
    if topic == moisture_topic:
        try:
            # Extract numeric value from "Moisture: XX.X"
            val = float(payload.split(": ")[1])
            status = "NORMAL"
            
            # Automated Logic: Trigger Alarm if below threshold
            if val < MOISTURE_THR:
                status = "CRITICAL"
                logger.warning(f"Threshold warning! Soil is dry ({val}%). Sending ALARM.")
                client.publish(alarm_topic, "LOW_MOISTURE_ALARM")
            
            save_to_db(val, status)
        except Exception as e:
            ic(f"Error parsing moisture data: {e}")

def on_connect(client, userdata, flags, rc):
    """Callback for successful connection to the broker."""
    if rc == 0:
        ic("Connected to Broker OK")
        # Subscribe to all relevant topics
        client.subscribe(moisture_topic)
        client.subscribe(relay_topic)
    else:
        ic(f"Connection failed with code {rc}")

def main():
    init_db()
    r = datetime.now().microsecond
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, f"Manager_{r}")
    client.on_connect = on_connect
    client.on_message = on_message
    
    ic(f"Connecting to broker {broker_ip}...")
    client.connect(broker_ip, int(broker_port))
    client.loop_forever()

if __name__ == "__main__":
    main()
