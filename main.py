#!/usr/bin/env /home/greg/pyenv/facereco/bin/python3.9

from variables import *
from PIL import Image
import cv2
from ultralytics import YOLO
import json
import os
import time

# modele pour la reconnaissance a utiliser
model = YOLO("yolov8n.pt")
#time.sleep(180)

try:
    os.system('rm -f {}*'.format(captdir))
except:
    pass

while(True):
    cwd = '{}'.format(captdir)
    files=[]
    for f in os.listdir(cwd):
        if os.path.isfile(os.path.join(cwd, f)):
            try:
                Image.open("{}/{}".format(cwd,f)) 
                files.append("{}/{}".format(cwd,f))
            except:
                pass

    if len(files) == 0:
        continue
    # image a analyser
    results = model(files)

    # resultat de l'analyse formaté en Json
    for r in results:
        human=0
         #print(r)
        data=json.loads(r.tojson())
        for i in data:
            if i['name'] == 'person':
                human+=1

        if human > 0:
            print('there is a human on this picture : {}'.format(r.path))
            os.rename('{}'.format(r.path),'{}/{}'.format(detectdir,r.path.split('/')[-1]))
            with open('{}'.format(trigger), 'w') as f:
                f.write('Someone Was detected !')
            os.system('rsync -auvz --timeout=5 -e "ssh -p {}  -i {}" {}/* {}:~/'.format(sshport,sshkey,detectdir,sshserv))
        else:
            print('there is no human on this picture : {}'.format(r.path))
            os.rename('{}'.format(r.path),'{}/{}'.format(nonedir,r.path.split('/')[-1]))

    time.sleep(2)
