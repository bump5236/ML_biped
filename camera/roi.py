import cv2
from ximea import xiapi

#create instance for first connected camera
cam = xiapi.Camera()

print('Opening first camera...')
cam.open_device()

# 1. Resize the main region - region 0.
cam.set_region_selector(0)
cam.set_width(200) # This is the width for all regions
cam.set_height(100)
cam.set_offsetX(100) # This is the x_offset for all regions
# 2. Configure another region.
cam.set_region_selector(0) # Selects region 1.
cam.set_height(200) # This is the new height of region 1
cam.set_offsetY(200) # This is th Y-offset of region 1
cam.set_region_mode(1) # Atcivate (1), or deactivate (0) the selected region.

# # 3. Start acquisition.
# cam.StartAcquisition();
# Mat cv_mat_image = cam.GetNextImageOcvMat();
# cv::imshow("Image from the camera",cv_mat_image);