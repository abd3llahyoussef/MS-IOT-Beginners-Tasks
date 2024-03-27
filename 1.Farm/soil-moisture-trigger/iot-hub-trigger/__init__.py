# in function.json: binding is the term to connect between Azure Functions and other Azure services. This function has an input binding to an event hub - it connects to an event hub and receives data.
# The connection string cannot be stored in the function.json file, it has to be read from the settings. This is to stop you accidentally exposing your connection string.
import logging

import azure.functions as func

import json
import os
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

def main(event: func.EventHubEvent):    
    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')

    soil_moisture = body['soilMoisture']

    if soil_moisture > 450:
        direct_method = CloudToDeviceMethod(method_name='relay_on', payload='{}')
    else:
        direct_method = CloudToDeviceMethod(method_name='relay_off', payload='{}')

    logging.info(f'Sending direct method request for {direct_method.method_name} for device {device_id}')
    
    registry_manager_connection_string = os.environ['REGISTRY_MANAGER_CONNECTION_STRING']
    registry_manager = IoTHubRegistryManager(registry_manager_connection_string)

    registry_manager.invoke_device_method(device_id, direct_method)

    logging.info('Direct method request sent!')
