# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import machine
import os
import time

uart = machine.UART(0, 115200)
os.dupterm(uart)

