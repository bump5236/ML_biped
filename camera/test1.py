from ximea import xiapi
import cv2
import time
import PIL.Image

cnt = 0
#create instance for first connected camera 
cam = xiapi.Camera()

save_F = 0
FILE_NAME = "003_HS_test.avi"
FRAME_RATE = 30

#start communication
print('Opening first camera...')
cam.open_device()

#settings
cam.set_exposure(1000)
# cam.set_acq_timing_mode('XI_ACQ_TIMING_MODE_FRAME_RATE')
# cam.set_framerate(500)

# ---------Skipping_start---------
# cam.set_downsampling_type('XI_SKIPPING')
# cam.set_downsampling('XI_DWN_2x2')
# ---------Skipping_end---------

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

try:
    print('Starting video. Press CTRL+C to exit.')
    t0 = time.time()
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
        text = 'FPS:{:5.2f}'.format(cam.get_framerate())
        # cv2.putText(
        #     data, text, (480,400), font, 1, (255, 255, 255), 2
        #     )
        cv2.imshow('XiCAM example', data)
        print(text)

        if save_F == 1:
            rec.write(data)

        k = cv2.waitKey(1)
        if k == 27:
            break

        elif k == ord('s'):
            save_F = 1

except KeyboardInterrupt:
    # cv2.destroyAllWindows()
    pass

rec.release()
cv2.destroyAllWindows()
#stop data acquisition
print('Stopping acquisition...')
cam.stop_acquisition()

#stop communication
cam.close_device()

print('Done.')
