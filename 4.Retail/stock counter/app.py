from counterfit_connection import CounterFitConnection
CounterFitConnection.init("127.0.0.1", 5000)

import io
from counterfit_shims_picamera import PiCamera

#For Use AI Model 
from msrest.authentication import ApiKeyCredentials
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient

from PIL import Image, ImageDraw, ImageColor

#Calculate Stock
from shapely.geometry import Polygon
#percentage allowed for inersection
overlap_threshold = 0.20

#calculate overlapping
def create_polygon(prediction):
    scale_left = prediction.bounding_box.left
    scale_top = prediction.bounding_box.top
    scale_right = prediction.bounding_box.left + prediction.bounding_box.width
    scale_bottom = prediction.bounding_box.top + prediction.bounding_box.height

    return Polygon([(scale_left, scale_top), (scale_right, scale_top), (scale_right, scale_bottom), (scale_left, scale_bottom)])

prediction_url = ''
prediction_key = ''

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
results = predictor.detect_image(project_id, iteration_name, image)

threshold = 0.3

predictions = list(prediction for prediction in results.predictions if prediction.probability > threshold)

for prediction in predictions:
    #print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%')
    print(f'{prediction.tag_name}:\t{prediction.probability * 100:.2f}%\t{prediction.bounding_box}')
    print('-------------------------------')
#Finally, show the results

#The logic for removing overlapping objects involves comparing all bounding boxes 
#and if any pairs of predictions have bounding boxes that overlap more than the threshold, 
#delete one of the predictions. To compare all the predictions, 
#you compare prediction 1 with 2, 3, 4, etc., then 2 with 3, 4, etc
    
to_delete = []

for i in range(0, len(predictions)):
    polygon_1 = create_polygon(predictions[i])

    for j in range(i+1, len(predictions)):
        polygon_2 = create_polygon(predictions[j])
        overlap = polygon_1.intersection(polygon_2).area

        smallest_area = min(polygon_1.area, polygon_2.area)

        if overlap > (overlap_threshold * smallest_area):
            to_delete.append(predictions[i])
            break

for d in to_delete:
    predictions.remove(d)

print(f'Counted {len(predictions)} stock items')

with open('image.jpg', 'wb') as im:
    im.write(image.read())
    draw = ImageDraw.Draw(im)

    for prediction in predictions:
        scale_left = prediction.bounding_box.left
        scale_top = prediction.bounding_box.top
        scale_right = prediction.bounding_box.left + prediction.bounding_box.width
        scale_bottom = prediction.bounding_box.top + prediction.bounding_box.height
        
        left = scale_left * im.width
        top = scale_top * im.height
        right = scale_right * im.width
        bottom = scale_bottom * im.height

        draw.rectangle([left, top, right, bottom], outline=ImageColor.getrgb('red'), width=2)

    im.save('image.jpg')

