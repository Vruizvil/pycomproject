from network import Bluetooth
import time
bt = Bluetooth()
bt.stop_scan()
bt.start_scan(-1)

while True:
    adv = bt.get_adv()
    print(adv)
    if adv:
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_NAME_CMPL))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_NAME_SHORT))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_FLAG))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_16SRV_PART))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_T16SRV_CMPL))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_32SRV_PART))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_32SRV_CMPL))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_128SRV_PART))
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_128SRV_CMPL))
        
        print('data %s' % bt.resolve_adv_data(adv.data, bt.ADV_TX_PWR))
    time.sleep(4)
    if adv and bt.resolve_adv_data(adv.data, Bluetooth.ADV_NAME_CMPL) == 'Heart Rate':
        conn = bt.connect(adv.mac)
        services = conn.services()
        for service in services:
            time.sleep(0.050)
            if type(service.uuid()) == bytes:
                print('Reading chars from service = {}'.format(service.uuid()))
            else:
                print('Reading chars from service = %x' % service.uuid())
            chars = service.characteristics()
            for char in chars:
                if (char.properties() & Bluetooth.PROP_READ):
                    print('char {} value = {}'.format(char.uuid(), char.read()))
        conn.disconnect()
        break
    else:
        time.sleep(0.050)
