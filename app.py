import torch
import time
import cv2
import numpy as np
from flask import request
from flask import Flask
from flask import Response
import os

app = Flask(__name__)

# initial the model
# model = torch.hub.load('yolov5', 'custom', path='yolov5s.pt', source='local')
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.eval()

@app.route('/greet')
def greet():
    return("Hello")

@app.route('/count_gpu')
def countGPU():
        return str(torch.cuda.device_count())

@app.route('/detect',methods=['POST'])
def detect():
    # get the image from the multipart form
    image = request.files["image"].read()
    # convert the image into a opencv image
    image = cv2.imdecode(np.frombuffer(image, np.uint8), -1)
    # send the image to the model and get the result
    results = model(image)
    # get the bounding boxes of the detected objects
    boxes = results.xyxy[0].cpu().numpy()
    # draw the bounding boxes on the image
    for box in boxes:
        x1,y1,x2,y2 = int(box[0]),int(box[1]),int(box[2]),int(box[3])
        image = cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
        # put the confidence value and category name on the image
        image = cv2.putText(image,str(box[4]),(x1,y1),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),2)
    # convert image to a binary string
    image = cv2.imencode('.png', image)[1].tostring()
    # send the image to the client as an png image encoded as a binary string
    return Response(image, mimetype='image/png')




    