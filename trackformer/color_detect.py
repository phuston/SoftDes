import cv2
import numpy as np
import argparse
import random

cam = cv2.VideoCapture(0)  

winName = "Color Detector"
cv2.namedWindow(winName, cv2.CV_WINDOW_AUTOSIZE)

boundaries = ([50, 30, 30], [145, 133, 128])

    
while True:
	ret, frame = cam.read()

	lower, upper = boundaries[2]
	# lower, upper = random.choice(boundaries)
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")

	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(frame, lower, upper)
	output = cv2.bitwise_and(frame, frame, mask = mask)

	# show the images
	cv2.imshow("frame", np.hstack([frame, output]))
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
    
print "Goodbye"



