#include <stdio.h>
#include <iostream>
#include "xiApiPlusOcv.hpp" 

using namespace cv;
using namespace std;

int main (void)
{
  try
  {
    xiAPIplusCameraOcv cam;
    cout << "Opening first camera..." << endl;
    cam.OpenFirst();


	// Settings
    cam.SetExposureTime(1000); //1000 us = 1 ms
	
	cam.SetAcquisitionTimingMode(XI_ACQ_TIMING_MODE AcquisitionTimingMode);
	cam.SetFrameRate(500);
    
	cam.xiSetParamInt(handle, XI_PRM_DOWNSAMPLING_TYPE, XI_SKIPPING);
	cam.xiSetParamInt(handle, XI_PRM_DOWNSAMPLING, 2);

	cout << "Starting acquisition..." << endl;
    cam.StartAcquisition();

	cout << "First pixel value:" << endl;
	XI_IMG_FORMAT format = cam.GetImageDataFormat();

	#define EXPECTED_IMAGES 50
	for (int images=0;images < EXPECTED_IMAGES;images++)
	{
	// Read and convert a frame from the camera
		Mat cv_mat_image = cam.GetNextImageOcvMat();
		cout << +cv_mat_image.at<uchar>(0, 0) << endl;
		// imshow("Image from camera", cv_mat_image);
		float fps = cam.GetFrameRate();
		printf("FPS:%d\n", fps);
	}
		waitKey(2);
	}

    cam.StopAcquisition();
    cam.Close();
		cout << "Done" << endl;
		waitKey(1000);
  }
	catch(xiAPIplus_Exception& exp)
	{
		cout << "Error:" << endl;
		exp.PrintError();
#ifdef WIN32
		Sleep(3000);
#endif
		waitKey(3000);
		return -1;
	}
	return 0;
}
