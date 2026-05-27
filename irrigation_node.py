import sys
import random
import paho.mqtt.client as mqtt
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mqtt_init import *

class IrrigationNode(QMainWindow):
    def __init__(self):
        super().__init__()
        # MQTT Client setup with API v1 for compatibility
        r = random.randrange(1, 1000000)
        clientname = f"Node_{r}"
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, clientname)
        self.client.connect(broker_ip, int(broker_port))
        self.client.loop_start()
        
        self.moisture_val = 55.0 
        
        # Simulation timer: sends data every 5 seconds
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.send_telemetry)
        self.timer.start(5000)

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Irrigation Unit Emulator")
        self.setMinimumSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Telemetry Display
        self.label = QLabel(f"Soil Moisture: {self.moisture_val}%")
        self.label.setFont(QFont('Arial', 14, QFont.Bold))
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        # Manual Actuator Button
        self.btn = QPushButton("Manual Irrigation (Actuator)")
        self.btn.setMinimumHeight(60)
        self.btn.setFont(QFont('Arial', 11, QFont.Bold))
        self.btn.setStyleSheet("background-color: #27ae60; color: white; border-radius: 8px;")
        self.btn.clicked.connect(self.manual_irrigation)
        layout.addWidget(self.btn)
        
        self.status_label = QLabel("Relay Status: IDLE")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def send_telemetry(self):
        """Simulates natural evaporation and publishes data."""
        self.moisture_val -= random.uniform(0.5, 2.0)
        if self.moisture_val < 0: self.moisture_val = 0
        
        self.label.setText(f"Soil Moisture: {round(self.moisture_val, 2)}%")
        msg = f"Moisture: {round(self.moisture_val, 2)}"
        self.client.publish(moisture_topic, msg)

    def manual_irrigation(self):
        """Actuator logic: Increases moisture levels manually."""
        print("Actuator Triggered: Manual Irrigation Started")
        self.client.publish(relay_topic, "RELAY_ON_MANUAL")
        self.moisture_val += 15.0
        if self.moisture_val > 100: self.moisture_val = 100
        self.status_label.setText("Relay Status: PUMPING...")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    node = IrrigationNode()
    node.show()
    sys.exit(app.exec_())