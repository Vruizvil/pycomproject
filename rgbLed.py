import pycom
import time

# disable the heartbeat led
pycom.heartbeat(False)
t=0.3

# turn the heartbeat LED in green color
pycom.rgbled(0xFF00)
print('green')
time.sleep(t)

# now in red
pycom.rgbled(0xFF0000)
print('red')
time.sleep(t)

pycom.rgbled(0x0000FF) #BLUE
print('blue')
time.sleep(t)

pycom.rgbled(0xCC0000) # red
time.sleep(t)
pycom.rgbled(0xFF6600) # orange
time.sleep(t)
pycom.rgbled(0xFFFF00) # yellow
time.sleep(t)
pycom.rgbled(0x99FF00) # lime
time.sleep(t)
pycom.rgbled(0x00CC00) # green
time.sleep(t)
pycom.rgbled(0x009966) # aqua
time.sleep(t)
pycom.rgbled(0x0033CC) # blue
time.sleep(t)
pycom.rgbled(0x330099) # indigo
time.sleep(t)
pycom.rgbled(0x660099) # violet
time.sleep(t)
pycom.rgbled(0xCC0099) # pink
time.sleep(t)
pycom.rgbled(0xFF0033) # magenta
time.sleep(t)

# turn off the heartbeat LED
pycom.rgbled(0)
time.sleep(t)
