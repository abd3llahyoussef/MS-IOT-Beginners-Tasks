from counterfit_connection import CounterFitConnection
CounterFitConnection.init("127.0.0.1", 5000)

import io
from counterfit_shims_picamera import PiCamera

#For Use AI Model 
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

prediction_url = 'url'
prediction_key = 'key'

parts = prediction_url.split('/')
endpoint = 'https://' + parts[2]
project_id = parts[6]
iteration_name = parts[9]
#The prediction URL that was provided by the Prediction URL dialog is 
#designed to be used when calling the REST endpoint directly. 
#The Python SDK uses parts of the URL in different places.
# Add the following code to break apart this URL into the parts needed

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

prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(endpoint, prediction_credentials)
#Create a predictor object to perform the prediction
#The prediction_credentials wrap the prediction key. 
#These are then used to create a prediction client object pointing at the endpoint.

image.seek(0)
results = predictor.classify_image(project_id, iteration_name, image)
#Send the image to custom vision, This rewinds the image back to the start, then sends it to the prediction client.


for prediction in results.predictions:
    print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')
    print('-------------------------------')
#Finally, show the results
    
with open('image.jpg', 'wb') as image_file:
    image_file.write(image.read())
