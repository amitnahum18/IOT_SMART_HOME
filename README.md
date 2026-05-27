# 🌱 IoT Smart Home - Irrigation System

A comprehensive IoT-based smart irrigation system built with Python that enables automated and manual watering through real-time monitoring and MQTT communication.

## 📋 Project Overview

This project implements an intelligent irrigation management system designed to optimize water usage in home gardens and agricultural settings. It combines IoT sensors, MQTT communication, database logging, and a user-friendly web dashboard.

### Key Features

- **Real-time Monitoring**: Live soil moisture tracking with automated alerts
- **MQTT-based Communication**: Publish/Subscribe architecture for sensor-to-system communication
- **Automated Irrigation Triggers**: Automatic watering when soil moisture falls below a critical threshold
- **Manual Controls**: Desktop GUI for manual irrigation actuation
- **Data Persistence**: SQLite database for historical moisture logging
- **Web Dashboard**: Streamlit-based real-time monitoring interface with charts and analytics
- **Alert System**: Automatic alarm generation for low moisture conditions

## 🏗️ System Architecture

The system consists of three main components:

### 1. **Irrigation Node** (`irrigation_node.py`)
- PyQt5-based GUI application simulating soil moisture sensors and actuators
- Continuously publishes moisture data to MQTT broker
- Supports manual irrigation triggering via desktop interface
- Simulates natural evaporation for realistic sensor data

### 2. **Application Manager** (`app_manager.py`)
- Central data processing and logging service
- Subscribes to MQTT sensor topics
- Evaluates moisture levels against predefined thresholds
- Logs all telemetry data to SQLite database
- Publishes alarm notifications when moisture is critical

### 3. **Dashboard** (`main_dashboard.py`)
- Streamlit-based web interface for real-time monitoring
- Displays current soil moisture percentage
- Shows system status (NORMAL/CRITICAL)
- Real-time line charts showing historical moisture trends
- Expandable section for raw telemetry logs

## 🔧 Components

### Files Structure

```
IOT_SMART_HOME/
├── app_manager.py           # Central manager service
├── irrigation_node.py       # Node/Sensor emulator with GUI
├── main_dashboard.py        # Web dashboard (Streamlit)
├── mqtt_init.py             # MQTT configuration constants
├── irrigation_system.db     # SQLite database
└── README.md               # This file
```

### Configuration (`mqtt_init.py`)
Contains shared MQTT settings:
- Broker IP and port
- Topic definitions:
  - `moisture_topic`: For moisture sensor readings
  - `relay_topic`: For irrigation actuator commands
  - `alarm_topic`: For alert notifications
- Threshold constants (e.g., `MOISTURE_THR`)

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- MQTT Broker (e.g., Mosquitto)
- PyQt5
- Paho MQTT Client
- Streamlit
- Pandas
- ICEcream (for debugging)

### Installation

```bash
# Clone the repository
git clone https://github.com/amitnahum18/IOT_SMART_HOME.git
cd IOT_SMART_HOME

# Install required dependencies
pip install paho-mqtt PyQt5 streamlit pandas icecream
```

### Configuration

Edit `mqtt_init.py` to configure:

```python
broker_ip = "your_broker_ip"      # MQTT Broker address
broker_port = 1883                 # MQTT Broker port
moisture_topic = "home/sensor/moisture"
relay_topic = "home/actuator/relay"
alarm_topic = "home/alerts/alarm"
MOISTURE_THR = 40                 # Moisture threshold (%)
```

### Running the System

**Terminal 1: Start the MQTT Broker**
```bash
mosquitto -v
```

**Terminal 2: Run the Application Manager**
```bash
python app_manager.py
```

**Terminal 3: Run the Irrigation Node (GUI)**
```bash
python irrigation_node.py
```

**Terminal 4: Start the Dashboard**
```bash
streamlit run main_dashboard.py
```

Access the dashboard at `http://localhost:8501`

## 📊 How It Works

1. **Sensor Reading**: The Irrigation Node simulates soil moisture sensors and publishes readings via MQTT
2. **Data Processing**: The App Manager subscribes to sensor topics and processes incoming data
3. **Threshold Evaluation**: If moisture falls below the threshold, an alarm is triggered
4. **Logging**: All measurements are saved to the SQLite database with timestamps
5. **Visualization**: The Dashboard retrieves historical data and displays real-time metrics and charts
6. **Manual Override**: Users can manually trigger irrigation via the Node GUI

## 🔌 MQTT Topic Structure

| Topic | Direction | Content | Example |
|-------|-----------|---------|---------|
| `home/sensor/moisture` | Node → Manager | Moisture reading | `Moisture: 45.5` |
| `home/actuator/relay` | Node → Manager | Relay state | `RELAY_ON_MANUAL` |
| `home/alerts/alarm` | Manager → All | Alert notifications | `LOW_MOISTURE_ALARM` |

## 📈 Database Schema

**moisture_logs table:**
```sql
- timestamp (TEXT): Date and time of reading
- value (REAL): Moisture percentage (0-100)
- status (TEXT): Current status (NORMAL/CRITICAL)
```

## 🎯 Key Features in Detail

### Automated Thresholds
- Configurable moisture threshold triggers automatic watering
- Logging of all state changes with timestamps
- Real-time status updates to dashboard

### Manual Controls
- Desktop interface for immediate irrigation needs
- One-click button to trigger manual watering
- Visual feedback on relay status

### Data Analytics
- Historical trend visualization
- Expandable data explorer for detailed logs
- Auto-refresh dashboard every 5 seconds

## ⚙️ Configuration Tips

- **Increase Responsiveness**: Lower the timer interval in `irrigation_node.py` (line 25)
- **Adjust Thresholds**: Modify `MOISTURE_THR` in `mqtt_init.py` based on your plant needs
- **Change Evaporation Rate**: Adjust the random range in `send_telemetry()` (line 59)

## 🐛 Troubleshooting

**Dashboard shows "Waiting for data"**
- Ensure the Manager and Node services are running
- Check MQTT broker connectivity
- Verify topic names match across all files

**MQTT Connection Errors**
- Verify broker IP and port in `mqtt_init.py`
- Confirm MQTT broker is running
- Check firewall settings

**Database Errors**
- Ensure write permissions in the project directory
- Delete `irrigation_system.db` to reset (will lose historical data)

## 📝 License

This project is open source and available for educational and personal use.

## 👤 Author

**Amit Nahum** (amitnahum18)

## 🤝 Contributing

Contributions are welcome! Feel free to fork the project and submit pull requests.

---

**Last Updated**: May 27, 2026
