#Initialize WiFi
known_nets = [('WI3T', 'Yuca2013???'), ('office_ssid', 'office_password')] # change this line to match your WiFi settings

import machine
#import os
#uart = machine.UART(0, 115200) # disable these two lines if you don't want serial access
#os.dupterm(uart)

if machine.reset_cause() != machine.SOFT_RESET: # needed to avoid losing connection after a soft reboot
    from network import WLAN
    wl = WLAN()

    # save the default ssid and auth
    original_ssid = wl.ssid()
    original_auth = wl.auth()

    wl.mode(WLAN.STA)

    available_nets = wl.scan()
    nets = frozenset([e.ssid for e in available_nets])

    known_nets_names = frozenset([e[0] for e in known_nets])
    net_to_use = list(nets & known_nets_names)

    try:
        net_to_use = net_to_use[0]
        pwd = dict(known_nets)[net_to_use]
        sec = [e.sec for e in available_nets if e.ssid == net_to_use][0]
        wl.connect(net_to_use, (sec, pwd), timeout=10000)
        print('IP address:', wl.ifconfig()[0])
    except:
        wl.init(mode=WLAN.AP, ssid=original_ssid, auth=original_auth, channel=6, antenna=WLAN.INT_ANT)
