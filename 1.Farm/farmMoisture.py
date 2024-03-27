from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1',5000)
# to interact with Analog sensors like soil Moisture sensor
from counterfit_shims_grove.adc import ADC 
import time
# to control Bump by Rely and Soil Moisture Sensor
from counterfit_shims_grove.grove_relay import GroveRelay
# to control through MQTT Broker
import paho.mqtt.client as mqtt
import json
# to connect to Azure cloud
from azure.iot.device import IoTHubDeviceClient,Message,MethodResponse


#MQTT Configrations
id = 'abdallah123'
client_Name = id + '\Soil'
mqtt_client = mqtt.Client(client_Name)
mqtt_client.connect("test.mosquitto.org")

publish_topic = id + '\SoilBump'

mqtt_client.loop_start()
print("MQTT Broker Connected !!!")

def on_message (client,userdata,msg):
    moisture = json.loads(msg.payload.decode())
    print(f"Soil Moisture From Broker is:{moisture}")
        # control condtions
    if moisture > 450 :
        print("Soil Moisture is too low, turn bump on")
        mqtt_client.unsubscribe(publish_topic) 
        relay.on()
        time.sleep(5)
        relay.off()
        time.sleep(20)
        mqtt_client.subscribe(publish_topic)
    else:
        print("Soil Moisture is ok, turn bump off")
        relay.off()
    

soilSensor = ADC()
relay = GroveRelay(5)


while True:
    moisture = soilSensor.read(0)
    print(f"Soil Moisture is:{moisture}")
    mqtt_client.publish(publish_topic,json.dumps(moisture))

    time.sleep(5)
    
    mqtt_client.subscribe(publish_topic)
    mqtt_client.on_message = on_message

