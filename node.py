import os
import sys
import socket
import time
import struct
import ubinascii
import json
import machine
from network import LoRa
uart_arduino = machine.UART(1, 9600)

# A basic package header, B: 1 byte for the deviceId, B: 1 bytes for the pkg size
_LORA_PKG_FORMAT = "BB%ds"
_LORA_PKG_ACK_FORMAT = "BBB"
DEVICE_ID = 0x01

# Open a Lora Socket, use tx_iq to avoid listening to our own messages
lora = LoRa(mode=LoRa.LORA, tx_iq=True)
lora_sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
lora_sock.setblocking(False)

def GetData(data_type):
    year, month, day, hour, minute, second, ms, dayinyear = time.localtime() 
    if not data_type:
        raise Exception('Requiere data type. Values: device, lora, app')
    if (data_type == 'app'):
        serialdata=str(uart_arduino.readline())
        datas=serialdata[2:len(serialdata)-5]
        va=json.loads(json.dumps(datas))
        print("value %s" % va)
        self = {
            'tt': "Presence", 
            'nm': "LivingRoom", 
            #'va': va, 
            'uid': ubinascii.hexlify(machine.unique_id())
        }
        self=va
    elif (data_type == 'device'):
        self = {
            'vo': str(sys.version),  #system version
            #'mp': str(sys.implementation[1]), #micropython version
            'pt': str(sys.platform), #pycom platform
            'rl': str(os.uname()[2]),  #firmware release
            #'tm': str(year) + str(month) + str(day) + str(hour) + str(minute) + str(second)
        }
    elif (data_type =='lora'):
        self = {
            #'id': DEVICE_ID, 
            'rs': lora.rssi(),  
            #'fq':lora.frequency(),
            'tx': lora.tx_power(),
            #'bw':lora.bandwidth(),
            #'pr':lora.preamble(),
            #'cr':lora.coding_rate(),
            #'sf':lora.sf(),
            #'mac': ubinascii.hexlify(lora.mac())
        }
    else:
        raise Exception('Require data type. Values: device, lora, app. %s invalid value' % data_type)
    return self
 
def WaitResponse(retries, ack_code):
     # Wait for the response from the gateway.
    waiting_ack = retries
    #while(waiting_ack>0):
    while(True):
        recv_ack = lora_sock.recv(256)
        waiting_ack = waiting_ack - 1
        ack = -1 #error
        if (len(recv_ack) > 0):
            device_id, pkg_len, ack = struct.unpack(_LORA_PKG_ACK_FORMAT, recv_ack)
            if (device_id == DEVICE_ID):
                if (ack == ack_code):
                    waiting_ack = 0
                    print("ACK")
                    break
                else:
                    waiting_ack = 0
                    print("None ACK. Message Failed")   
    return ack
 
def GetPkg(data): 
    msg= "%s" % str(json.loads(json.dumps(data)))
    pkg = struct.pack(_LORA_PKG_FORMAT % len(msg), DEVICE_ID, len(msg), msg)
    #print('Sending: %s' % (str(msg)))
    #print('Lenght: %d' % (len(pkg)))
    return pkg
    
def SendData(data):
    apppkg = GetPkg(data)
    print('Sending: %s' % apppkg)
    self = lora_sock.send(apppkg)
    print('Lenght: %d ' % self)
    response = WaitResponse(300, 200)
    print(response)   
    return self

waiting_time = 100
while(waiting_time>0):
    appdata = GetData('app')
    if (appdata!='n' and appdata!=""):
        SendData(appdata)

    devicedata = GetData('device')
    #SendData(devicedata)
   
    loradata = GetData('lora')
    #SendData(loradata)

    time.sleep(5)
    waiting_time = waiting_time - 1
print("Finised!!")

