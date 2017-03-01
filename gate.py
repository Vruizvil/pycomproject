import socket,  machine,  pycom
import struct,  time,  json
from network import LoRa
from umqtt import MQTTClient

# Initialize MQTT Client
def settimeout(duration): pass


def t3_publication(topic, msg):
	print (topic, ';', msg)
	pycom.rgbled(0xff00)

UNIQUE_ID = machine.unique_id()
MQTT_BROKER = "192.168.2.68"
MQTT_PORT = 1883
MQTT_TOPIC = "iot-2/type/lopy/id/lopy2/evt/evento1/fmt/json"
mqtt_client = MQTTClient(UNIQUE_ID, MQTT_BROKER, port=MQTT_PORT)
mqtt_client.settimeout = settimeout
mqtt_client.set_callback(t3_publication)
mqtt_client.connect()

_LORA_PKG_ACK_FORMAT = "BBB"
_LORA_PKG_FORMAT = "BB%ds"
lora = LoRa(mode=LoRa.LORA, rx_iq=True)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)
print("NANO GATEWAY RUNNING!!!")
while (True):
    recv_pkg = lora_sock.recv(512)
    print(recv_pkg)
    time.sleep(5)
    if (len(recv_pkg) > 2):
        recv_pkg_len = recv_pkg[1]
        device_id, pkg_len, msg = struct.unpack(_LORA_PKG_FORMAT % recv_pkg_len, recv_pkg)
        print(msg)
        #mqtt_client.publish("lopytopic", json.dumps(msg))
        mqtt_client.publish(MQTT_TOPIC, json.dumps(msg))
        
        ack_pkg = struct.pack(_LORA_PKG_ACK_FORMAT, device_id, 1, 200)
        lora_sock.send(ack_pkg)
