from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1',5000)
import time
import json
from counterfit_shims_seeed_python_dht import DHT
import paho.mqtt.client as mqtt

# save data at CSV file
from os import path
import csv
from datetime import datetime
#if sensor pin is 5 as humidity in counterfit the library understand that Temp on 6
sensor = DHT('11',5)

id = 'Abdallah123'
client_name = id + 'TempMeasure'
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

publish_topic = id + '/temp'
subscribe_topic = id + '/tempRecv'

mqtt_client.loop_start()
print("MQTT Broker Connected !!!")

#CSV file create ant its fields
temperature_file_name = 'temperature.csv'
fieldnames = ['date', 'temperature']

if not path.exists(temperature_file_name):
    with open(temperature_file_name, mode='w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

def handleMSG (client,userdata,msg):
    payload = json.loads(msg.payload.decode())
    print("Received Message: ",payload)
# add Received data
    with open(temperature_file_name, mode='a') as temperature_file:        
        temperature_writer = csv.DictWriter(temperature_file, fieldnames=fieldnames)
        temperature_writer.writerow({'date' : datetime.now().astimezone().replace(microsecond=0).isoformat(), 'temperature' : payload['temp']})
#conditions    
    if int(payload['temp']) >30 :
        print("it is too high temp")
    elif int(payload['temp']) < 0 :
        print("It is freezing!!!")

while True:
    #read Data
    humidity,temp = sensor.read()
    print(f"the Temperature is:{temp}")

    tempSend = json.dumps({'temp':temp})
    print(f"Massage Sent:{tempSend}")
    mqtt_client.publish(publish_topic,tempSend)
    time.sleep(5)

    mqtt_client.subscribe(publish_topic)
    mqtt_client.on_message = handleMSG