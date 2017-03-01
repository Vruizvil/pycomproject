from machine import  Pin,  ADC,  PWM
import time,  pycom

pycom.heartbeat(True)

pot = Pin('P19', mode=Pin.IN)
led= Pin('P9', mode=Pin.OUT)
led2=Pin('P12',  mode=Pin.OUT)
rgb=pycom.rgbled(0xFF00)
buz = Pin('P10',  mode=Pin.OUT)

adc = ADC()             # create an ADC object
apin = adc.channel(pin=pot)   # create an analog pin on P19
pwm = PWM(0, frequency=349)  # use PWM timer 0, with a frequency of 50KHz

while(True):
    val = apin()     # read an analog value
    led.value(val)
    buz.value(val)
    print(val)
    time.sleep(0.3)
    led.value(0)
    buz.value(0)
    
    
    # create pwm channel on pin P12 with a duty cycle of 50%
    time.sleep(0.5)
    pwm_c = pwm.channel(1, pin=led2, duty_cycle=0.2)
    time.sleep(0.7)
    pwm_c.duty_cycle(0.8) # change the duty cycle to 30%
    time.sleep(0.3)
    pwm_c.duty_cycle(0.0)
    time.sleep(0.5)
