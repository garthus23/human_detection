#!/usr/bin/env /home/greg/pyenv/facereco/bin/python3.9

from variables import *
from PIL import Image
import cv2
from ultralytics import YOLO
import json
import time
from datetime import datetime

# modele pour la reconnaissance a utiliser
model = YOLO("yolov8n.pt")
time.sleep(180)

cap0 = cv2.VideoCapture(0) 
cap1 = cv2.VideoCapture(2)

pict=0

while(True):


    ret0, cam0= cap0.read()
    ret1, cam1= cap1.read()
    img0 = cv2.resize(cam0,(640,480))
    img1 = cv2.resize(cam1,(640,480))
    
    results = model([img0,img1])

    for idx, r in enumerate(results):
        human=0
        data=json.loads(r.tojson())
        for i in data:
            if i['name'] == 'person':
                human+=1

        if human > 0:
            pict+=1
            print('there is a human on this picture : {}'.format(r.path))
            now = datetime.now()
            if idx == 0 :
                cv2.imwrite('{}/detection_{}.png'.format(captdir,now.strftime("%d%m%Y_%H%M%S")),img0)
            else:
                cv2.imwrite('{}/detection_{}.png'.format(captdir,now.strftime("%d%m%Y_%H%M%S")),img1)
            with open('{}'.format(trigger), 'w') as f:
                f.write('Someone Was detected !')
        else:
            print('there is no human on this picture : {}'.format(r.path))

    time.sleep(0.5)


