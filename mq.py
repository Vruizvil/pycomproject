# Initialize MQTT Client
from umqtt import MQTTClient
import socket
import machine, time
import pycom
def settimeout(duration): pass


def t3_publication(topic, msg):
	print (topic, ';', msg)
	pycom.rgbled(0xff00)


UNIQUE_ID = machine.unique_id()
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
mqtt_client = MQTTClient(UNIQUE_ID, MQTT_BROKER, port=MQTT_PORT)
mqtt_client.settimeout = settimeout
mqtt_client.set_callback(t3_publication)
#mqtt_client.connect()

#Publish some data
#print("Sending ON")
#mqtt_client.publish("lopytopic", "ON")
#Subcribe some topic
#mqtt_client.subscribe("lopytopic", qos=1)
#mqtt_client.check_msg()

#Publish on BLUEMIX IOT PLATFORM
mqtt_bluemix = MQTTClient("a:0k1ivs:lopy2", "0k1ivs.messaging.internetofthings.ibmcloud.com", user="a-0k1ivs-oeakppvyt2", password="MYROv2kIkEA5X*?ecH")
mqtt_bluemix.settimeout = settimeout
mqtt_bluemix.set_callback(t3_publication)
BLUEMIX_TOPIC = "iot-2/type/lopy/id/lopy2/evt/evento1/fmt/json"
#mqtt_bluemix.connect()
#mqtt_bluemix.publish(BLUEMIX_TOPIC,"Hello from Lopy")
