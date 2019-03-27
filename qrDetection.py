from __future__ import print_function

import json

import pyzbar.pyzbar as pyzbar
import cv2
import os
import time
import requests
from datetime import datetime, timedelta

# get the webcam:  
cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)
# 160.0 x 120.0
# 176.0 x 144.0
# 320.0 x 240.0
# 352.0 x 288.0
# 640.0 x 480.0
# 1024.0 x 768.0
# 1280.0 x 1024.0
time.sleep(2)

pile = {}



def decode(im):
    decodedObjects = pyzbar.decode(im)
    for obj in decodedObjects:
        text = str(obj.data)
        if obj.type == "QRCODE" and len(obj.data) == 6:
            if not text in pile:
                pile[text] = {
                    'itime': datetime.today(),
                    'otime': datetime.today() + timedelta(hours=0, minutes=0, seconds=59),
                    'remove': 0
                }
            else:
                print(pile)
                if pile[text]['itime'] <= pile[text]["otime"] \
                            and pile[text]['otime'] > datetime.today() \
                            and pile[text]['remove'] == 0:
                        try:
                            if os.path.isfile('hashnode'):
                                with open('hashnode') as f:
                                    h = [line for line in f]
                                    test=json.dumps({"value": str(obj.data).replace("b","").replace("\'", "")})
                                    print(test)
                                    r = requests.post('http://127.0.0.1:5000/post/'+str(h[0]), data=test)
                            print(r.text)
                            pile[text]['remove'] = 1
                        except Exception as ex:
                            print(ex)
                else:
                    if pile[text]['otime'] < datetime.today():
                        del pile[text]

    return decodedObjects


font = cv2.FONT_HERSHEY_SIMPLEX

while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Our operations on the frame come here
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    decode(im)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1)
    # Ongoing save data
    if key & 0xFF == ord('q'):
        print("Exit by supervisor request")
        break
    elif key & 0xFF == ord('s'):  # wait for 's' key to save
        print("Stored")
        cv2.imwrite('Capture.png', frame)

    # When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
