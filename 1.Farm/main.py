from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)
#print("Hello world")
import time
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
#The import time statement imports the Python time module that will be used later in this assignment.
#The from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor statement 
#imports the GroveLightSensor from the CounterFit Grove shim Python libraries. 
#This library has code to interact with a light sensor created in the CounterFit app.
import json

import paho.mqtt.client as mqtt
# inatall "paho-mqtt" library to connect yo broker



light_sensor = GroveLightSensor(0)
led_Actuator = GroveLed(5)
#The line light_sensor = GroveLightSensor(0) creates an instance of the GroveLightSensor class 
#connecting to pin 0 - the CounterFit Grove pin that the light sensor is connected to.


id = 'Abdallah123'

client_name = id + 'nightlight_client'
#Replace <ID> with a unique ID that will be used the name of this device client, 
#and later for the topics that this device publishes and subscribes to.
# The test.mosquitto.org broker is public and used by many people, including other students working through this assignment.
# Having a unique MQTT client name and topic names ensures your code won't clash with anyone elses.
# You will also need this ID when you are creating the server code later in this assignment.

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

print("MQTT connected!")
#This code creates the client object, connects to the public MQTT broker,
# and starts a processing loop that runs in a background thread listening for messages on any subscribed topics.

def on_message(mqtt_client, userdata, msg):
    # The callback for when a PUBLISH message is received from the server.
    payload = json.loads(msg.payload.decode())
    print("Message received:", payload)

    if int(payload["light"]) >=300:
        led_Actuator.on()
    else:
        led_Actuator.off()


client_telemetry_topic = id + '/telemetry'
client_command_topic = id + '/command'
while True:
    light = light_sensor.light
    telemetry = json.dumps({'light' : light})

    print("Sending telemetry ", telemetry)

    mqtt_client.publish(client_telemetry_topic, telemetry)

    time.sleep(5)


    mqtt_client.subscribe(client_telemetry_topic)
    mqtt_client.on_message = on_message

# while True:
#     light = light_sensor.light
#     print('Light level:', light)
#     if light > 300 :
#         led_Actuator.on()
#     else:
#         led_Actuator.off()
#This will read the current light level using the light property of the GroveLightSensor class. 
#This property reads the analog value from the pin. This value is then printed to the console.
#    time.sleep(1)
#Add a small sleep of one second at the end of the while loop as the light levels don't need to be checked continuously.
# A sleep reduces the power consumption of the device.
    

