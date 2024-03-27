from counterfit_connection import CounterFitConnection
CounterFitConnection.init("127.0.0.1", 5000)

import io
from counterfit_shims_picamera import PiCamera

import requests 

camera = PiCamera()
camera.resolution = (640, 480)
camera.rotation = 0
#This code creates a PiCamera object, sets the resolution to 640x480. 
#Although higher resolutions are supported, the image classifier works on much smaller images (227x227) 
#so there is no need to capture and send larger images.The camera.rotation = 0 line sets the rotation of the image in degrees. 

image = io.BytesIO()
camera.capture(image, 'jpeg')
image.seek(0)
#This codes creates a BytesIO object to store binary data. 
#The image is read from the camera as a JPEG file and stored in this object. 
#This object has a position indicator to know where it is in the data so that more data can be written to the end if needed,
#so the image.seek(0) line moves this position back to the start so that all the data can be read later.

prediction_url = '<URL>' # Classifier URL
headers = {
        'Content-Type' : 'application/octet-stream'
    }
image.seek(0)
response = requests.post(prediction_url, headers=headers, data=image)
results = response.json()

for prediction in results['predictions']:
        print(f'{prediction["tagName"]}:\t{prediction["probability"] * 100:.2f}%')

    
with open('image.jpg', 'wb') as image_file:
    image_file.write(image.read())
