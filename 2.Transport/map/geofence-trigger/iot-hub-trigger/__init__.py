import json
import os
import requests

import logging

import azure.functions as func
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod
def main(event: func.EventHubEvent): 
    maps_key = os.environ['MAPS_KEY']
    geofence_udid = os.environ['GEOFENCE_UDID']

    body = json.loads(event.get_body().decode('utf-8'))
    device_id = event.iothub_metadata['connection-device-id']

    logging.info(f'Received message: {body} from {device_id}')

    for e in event :
        event_body = json.loads(e.get_body().decode('utf-8'))
        lat = event_body['gps']['lat']
        lon = event_body['gps']['lon']

        url = 'https://atlas.microsoft.com/spatial/geofence/json'

        params = {
            'api-version': 1.0,
            'deviceId': 'gps-sensor',
            'subscription-key': maps_key,
            'udid' : geofence_udid,
            'lat' : lat,
            'lon' : lon
        } 

        response = requests.get(url, params=params)
        response_body = json.loads(response.text)

        distance = response_body['geometries'][0]['distance']

        if distance == 999:
            logging.info('Point is outside geofence')
        elif distance > 0:
            logging.info(f'Point is just outside geofence by a distance of {distance}m')
        elif distance == -999:
            logging.info(f'Point is inside geofence')
        else:
            logging.info(f'Point is just inside geofence by a distance of {distance}m')
