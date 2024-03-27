# in function.json: binding is the term to connect between Azure Functions and other Azure services. This function has an input binding to an event hub - it connects to an event hub and receives data.
# The connection string cannot be stored in the function.json file, it has to be read from the settings. This is to stop you accidentally exposing your connection string.
import logging

import azure.functions as func
from typing import List
import json
import os
import uuid
from azure.storage.blob import BlobServiceClient, PublicAccess

# from azure.iot.hub import IoTHubRegistryManager
# from azure.iot.hub.models import CloudToDeviceMethod

def get_or_create_container(name):
    connection_str = os.environ['STORAGE_CONNECTION_STRING']
    blob_service_client = BlobServiceClient.from_connection_string(connection_str)

    for container in blob_service_client.list_containers():
        if container.name == name:
            return blob_service_client.get_container_client(container.name)
    
    return blob_service_client.create_container(name, public_access=PublicAccess.Container)

def main(event: func.EventHubEvent):    

        body = json.loads(event.get_body().decode('utf-8'))
        device_id = event.iothub_metadata['connection-device-id']

        logging.info(f'Received message: {body} from {device_id}')

        device_id = event.iothub_metadata['connection-device-id']
        blob_name = f'{device_id}/{str(uuid.uuid1())}.json'

        container_client = get_or_create_container('gps-data')
        blob = container_client.get_blob_client(blob_name)

        event_body = json.loads(event.get_body().decode('utf-8'))
        blob_body = {
            'device_id' : device_id,
            'timestamp' : event.iothub_metadata['enqueuedtime'],
            'gps': event_body['gps']
        }

        logging.info(f'Writing blob to {blob_name} - {blob_body}')
        blob.upload_blob(json.dumps(blob_body).encode('utf-8'))