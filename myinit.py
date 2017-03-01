import time
print('myinit.py is running!')
execfile('wl.py')
time.sleep(3)
execfile('onewiresensors.py')
#execfile('mq.py')
#execfile('bt.py')
time.sleep(3)
print('myinit.py is finished!')
