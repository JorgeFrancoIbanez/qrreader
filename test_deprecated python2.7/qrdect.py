# import the necessary packages
import cv2
from imutils.video import VideoStream
import datetime
import argparse
import imutils
import time
import numpy as np
import zbar
from PIL import Image

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1,
	help="whether or not the Raspberry Pi camera should be used")
args = vars(ap.parse_args())


# initialize the video stream and allow the cammera sensor to warmup
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

#
#faceCascade = cv2.CascadeClassifier("~/opencv-2.4.10/data/haarcascades/haarcascade_frontalface_default.xml")
#faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 400 pixels
        frame = cv2.imread("//home/jfranco/Documents/13CCC/qrs/SKEW/15deg.jpg", 1 );
        frame = imutils.resize(frame, width=400)

        #QR code recognition
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        pil = Image.fromarray(gray)
        width, height = pil.size
        raw = pil.tobytes()
        image = zbar.Image(width, height, 'Y800', raw)
        scanner.scan(image)
	
        for symbol in image:
                print ('decoded', symbol.type, 'symbol', '"%s"' % symbol.data)

	# draw the timestamp on the frame
        timestamp = datetime.datetime.now()
        ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
        cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
                0.35, (0, 0, 255), 1)

	# show the frame
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
        if key == ord("q"):
                break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
