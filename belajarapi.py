from datetime import datetime
import json
import os
import time
from datetime import datetime



myjson= {
    'status': 'ok',
    'count': '62',
    'devices': [
        {
            'device_id': '42',
            'hostname': '101.255.141.74',
            'sysName': 'cmg-matrik-hq',
        },
        {
            'device_id': '84',
            'hostname': '103.149.47.105',
            'sysName': '2022216jkcro1039-dewi-hsg200',
        },
        {
            'device_id': '14',
            'hostname': '116.68.172.242',
            'sysName': 'cmg-master',
        },
    ]
}

a = myjson
ad = {'a' : a['devices']}
now = datetime.now()
dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
print(dt_string)