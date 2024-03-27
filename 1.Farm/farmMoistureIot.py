from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1',5000)
# to interact with Analog sensors like soil Moisture sensor
from counterfit_shims_grove.adc import ADC 
import time
# to control Bump by Rely and Soil Moisture Sensor
from counterfit_shims_grove.grove_relay import GroveRelay

import json
# to connect to Azure cloud
from azure.iot.device import IoTHubDeviceClient,Message,MethodResponse,X509

#connection_string = ""

#Security By Certificate
host_name = "soil-moisture-sensor-abdallah-iot.azure-devices.net"
device_id = "soil-moisture-sensor-x509"

#Create an X509 class instance using your certificate and key files by adding this code below the host_name declaration:
x509 = X509("./soil-moisture-sensor-x509-cert.pem", "./soil-moisture-sensor-x509-key.pem")

soilSensor = ADC()
relay = GroveRelay(5)

#device_client = IoTHubDeviceClient.create_from_connection_string(connection_string)
device_client = IoTHubDeviceClient.create_from_x509_certificate(x509, host_name, device_id)


print('Connecting')
device_client.connect()
print('Connected')
    

def method_request (req):
    print ('Received a direct method request',req.name)

    if req.name == 'relay_on':
        relay.on()
    elif req.name == 'relay_off':
        relay.off()
    method_res = MethodResponse.create_from_method_request(req,200)
    device_client.send_method_response(method_res)

device_client.on_method_request_received = method_request
# az iot hub invoke-device-method --device-id soil-moisture-sensor --method-name relay_off --method-payload '{}' --hub-name soil-moisture-sensor-abdallah-iot
# use this line in terminal to send a message from IoT Hub to control IoT Device

while True:
    moisture = soilSensor.read(0)
    print(f"Soil Moisture is:{moisture}")
    message = Message(json.dumps({'soilMoisture':moisture}))
    device_client.send_message(message)
    time.sleep(10)
    # if moisture > 450 :
    #     print("Soil Moisture is too low, turn bump on")
    #     relay.on()
    #     time.sleep(5)
    #     relay.off()
    #     time.sleep(20)
    # else:
    #     print("Soil Moisture is ok, turn bump off")
    #     relay.off()

# To Monitor the Readings Sent to Iot Hub use this command:
#az iot hub monitor-events --properties anno --hub-name soil-moisture-sensor-abdallah-iot
# OR
#az iot hub monitor-events --hub-name soil-moisture-sensor-abdallah-iot