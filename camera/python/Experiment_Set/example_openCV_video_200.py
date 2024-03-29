from ximea import xiapi
import cv2
import time
import PIL.Image
import sys
import Jetson.GPIO as GPIO


cnt = 0
#create instance for first connected camera 
cam = xiapi.Camera()

args = sys.argv
save_F = 0
FILE_NAME = "20191120_200_{}.avi".format(args[1])
FRAME_RATE = 30

#start communication
print('Opening first camera...')
cam.open_device()

#settings
cam.set_exposure(1875)

cam.set_downsampling_type('XI_SKIPPING')
cam.set_downsampling('XI_DWN_2x2')

cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FRAME_RATE')
cam.set_framerate(200)

# 1. Resize the main region - region 0.
# cam.set_region_selector(0)
# cam.set_aeag_roi_width(380) # This is the width for all regions
# cam.set_aeag_roi_height(400)
# cam.set_aeag_roi_offset_x(550) # This is the x_offset for all regions
# cam.set_aeag_roi_offset_y(200)
# 2. Configure another region.
# cam.set_region_selector(0) # Selects region 1.
# cam.set_aeag_roi_height(20) # This is the new height of region 1
# cam.set_aeag_roi_offset_y(20) # This is th Y-offset of region 1
# cam.set_region_mode(0) # Atcivate (1), or deactivate (0) the selected region.

# cam.set_width(32) #Multiple of 16
# cam.set_height(400) #Multiple of 2

rec = cv2.VideoWriter(FILE_NAME, \
                      cv2.VideoWriter_fourcc("H", "2", "6", "4"), \
                      FRAME_RATE, \
                      (cam.get_width(), cam.get_height()), \
                      False)

#create instance of Image to store image data and metadata
img = xiapi.Image()

#start data acquisition
print('Starting data acquisition...')
cam.start_acquisition()

tmp = 0
sync = 0

# Pin Definitions
input_pin = 31  # BCM pin 18, BOARD pin 12
prev_value = None
# Pin Setup:
GPIO.setmode(GPIO.BOARD)  # BCM pin-numbering scheme from Raspberry Pi
GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin
print("Waiting Sync now!")
print(GPIO.JETSON_INFO)
while sync == 0:
    value = GPIO.input(input_pin)
    if value != prev_value:
        if value == GPIO.HIGH:
            value_str = "HIGH"
        else:
            value_str = "LOW"
            sync = 1

        print("Value read from pin {} : {}".format(input_pin, value_str))
        prev_value = value
    time.sleep(1)

try:
    print('Starting video. Press CTRL+C to exit.')
    # t0 = time.time()

    while True:
        #get data and pass them from camera to img
        cam.get_image(img)

        #create numpy array with data from camera. Dimensions of the array are 
        #determined by imgdataformat
        data = img.get_image_data_numpy()

        # data = cv2.resize(data, (640, 480))
        #show acquired image with time since the beginning of acquisition
        font = cv2.FONT_HERSHEY_SIMPLEX
        # text = '{:5.2f}'.format(time.time()-t0)
        # text = 'FPS:{:5.2f}'.format(cam.get_framerate())
        # text2 = str(round(time.time()-t0,3))
        # cv2.putText(
        #     data, text2, (10,50), font, 1, (255, 255, 255), 2
        #     )
        # cv2.imshow('XiCAM example', data)
        # print(text2)

        if tmp == 0:
            print('saving')
        
        rec.write(data)
        tmp += 1

        # if save_F == 1:
        #     # print("---saving---")
        #     # print(type(data))
        #     # print(data.shape)
        #     rec.write(data)

        # k = cv2.waitKey(1)
        # if k == 27:
        #     break

        # elif k == ord('s'):
        #     save_F = 1

except KeyboardInterrupt:
    pass

rec.release()
cv2.destroyAllWindows()
GPIO.cleanup()
#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()

#stop communication
cam.close_device()

print('Done.')
