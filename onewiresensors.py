import time,  onewire,  machine, pycom,  json, ubinascii
from machine import Pin
from umqtt import MQTTClient


#pir = onewire.OneWire(Pin('P12'))
pir = onewire.OneWire(Pin('P12',mode=Pin.IN, pull=Pin.PULL_UP))
#config
hold_time_sec = 10
#flags
last_trigger = -10

def settimeout(duration): pass


def t3_publication(topic, msg):
	print (topic, ';', msg)
	pycom.rgbled(0xff00)

def sendmq(msg):
    UNIQUE_ID = ubinascii.hexlify(machine.unique_id())
    MQTT_BROKER = "192.168.2.68"
    MQTT_PORT = 1883
    MQTT_TOPIC = "iot-2/type/lopy/id/" + "buhardilla" + "/evt/presence1/fmt/json"
    print(MQTT_TOPIC)
    mqtt_client = MQTTClient(UNIQUE_ID, MQTT_BROKER, port=MQTT_PORT)
    mqtt_client.settimeout = settimeout
    mqtt_client.set_callback(t3_publication)
    mqtt_client.connect()
    result = mqtt_client.publish(MQTT_TOPIC, json.dumps(msg))
    mqtt_client.disconnect()
    return result


# main loop
print("Starting main loop")
while True:
    #print(pir(), pir2())
    if pir.read_bit() == 1:
        if time.time() - last_trigger > hold_time_sec:
            last_trigger = time.time()
            print("Presence detected, sending MQTT request")
            try:
                #execfile('node.py')
                return_code = sendmq('Presencia en Buhardilla')
                if return_code == None:
                    print("Request result. OK")
                else:
                    print("Request result: %s" % return_code)
            except Exception as e:
                print("Request failed")
                print(e)
    else:
        last_trigger = 0
        print("No presence")

    time.sleep_ms(500)

print("Exited main loop")
