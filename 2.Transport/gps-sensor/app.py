from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1',5000)

import time 
import counterfit_shims_serial

#Decode result
import pynmea2

import json
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse

connection_string = "Connection String"

device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)

print('Connecting')
device_client.connect()
print('Connected')
def decodeIt(line):
    msg = pynmea2.parse(line)
    if msg.sentence_type == 'GGA':
        lat = pynmea2.dm_to_sd(msg.lat)
        lon = pynmea2.dm_to_sd(msg.lon)

        if msg.lat_dir == 'S':
            lat = lat * -1

        if msg.lon_dir == 'W':
            lon = lon * -1
        message = Message(json.dumps({
    "gps" :
    {
        "lat" : lat,
        "lon" : lon
    }
}))
        device_client.send_message(message)
        print(f'{lat},{lon} - from {msg.num_sats} satellites')
serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')

while True:
    result = serial.readline().decode('utf-8')
    print(f"the location is :{result}")
    while len(result)>0:
        decodeIt(result)

    time.sleep(20)

    