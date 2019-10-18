import sys
# sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
# sys.path.remove('/home/tomato/catkin_ws/devel/lib/python2.7/dist-packages')

import cv2
print(cv2.__file__)
import numpy as np
import time
import os


save_F = 0
FILE_NAME = "video.avi"
FRAME_RATE = 30


rec = cv2.VideoWriter(FILE_NAME, \
                      cv2.VideoWriter_fourcc(*'XVID'), \
                      FRAME_RATE, \
                      (640, 480), \
                      False)

cap = cv2.VideoCapture(1)
# cap = cv2.VideoCapture("v4l2src device=/dev/video1 ! queue ! video/x-h264,width=640,height=480,framerate=30/1 ! h264parse ! avdec_h264 ! videoconvert ! appsink")
t1 = time.time()

while True:
    ret, frame = cap.read()
    # frame = cv2.resize(frame, (640, 480))
    print(type(frame))
    cv2.imshow('Raw Frame', frame)
    # print(time.time()-t1)
    if save_F == 1:
        print("---saving---")
        print(type(frame))
        print(frame.shape)
        rec.write(frame)

    k = cv2.waitKey(1)
    if k == 27:
        break

    elif k == ord('s'):
        save_F = 1

cap.release()
rec.release()
cv2.destroyAllWindows()
