import socket

# Broker Configuration
# We use HiveMQ public broker as the primary connection point
nb = 1 
brokers = [str(socket.gethostbyname('vmm1.saaintertrade.com')), str(socket.gethostbyname('broker.hivemq.com'))]
ports = ['80', '1883']
usernames = ['', ''] 
passwords = ['', ''] 

broker_ip = brokers[nb]
broker_port = ports[nb]
username = usernames[nb]
password = passwords[nb]

# MQTT Topic Definitions
# Shared prefix to avoid collisions on public brokers
comm_topic = 'pr/irrigation/5976397/'
moisture_topic = comm_topic + 'moisture'
relay_topic = comm_topic + 'relay'
alarm_topic = comm_topic + 'alarm'

# System Thresholds
MOISTURE_THR = 30.0