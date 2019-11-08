// xiApiPlusOcvExample.cpp : program opens first camera, captures and displays 40 images

#include <stdio.h>
#include <iostream>
#include "xiApiPlusOcv.hpp" 

using namespace cv;
using namespace std;
int main(int argc, char* argv[])
{
    try
    {
        // Sample for XIMEA OpenCV
        xiAPIplusCameraOcv cam;

        // Retrieving a handle to the camera device
        printf("Opening first camera...\n");
        cam.OpenFirst();
        cam.DisableAutoExposureAutoGain();

        // Create an inverse LUT  (inverts image pixels - min -> max, max -> min)
        int maxIndex = cam.GetLookUpTableIndex_Maximum();
        int minIndex = cam.GetLookUpTableIndex_Minimum();
        int actualIndex = cam.GetLookUpTableIndex();
        int incrementIndex = cam.GetLookUpTableIndex_Increment();
        int minValue = cam.GetLookUpTableValue_Minimum();
        int maxValue = cam.GetLookUpTableValue_Maximum();
        int actualValue = cam.GetLookUpTableValue();
        int incrementValue = cam.GetLookUpTableValue_Increment();

        cout << "maximal LUT index:" << maxIndex << endl;
        cout << "minimal LUT index:" << minIndex << endl;
        cout << "actual LUT index:" << actualIndex << endl;
        cout << "actual LUT index increment:" << incrementIndex << endl;

        cout << "maximal LUT value:" << maxValue << endl;
        cout << "minimal LUT value:" << minValue << endl;
        cout << "actual LUT value:" << minValue << endl;
        cout << "actual LUT value increment:" << incrementValue << endl;

        for (int i = 0; i < maxIndex; i++){
            cam.SetLookUpTableIndex(i);
            cam.SetLookUpTableValue(maxValue - i);
        }
        cam.SetLookUpTableIndex(800);
        cam.SetLookUpTableValue(4);
        cam.EnableLookUpTable();
        //cam.DisableLookUpTable();
        //Set exposure
        cam.SetExposureTime(40000); //10000 us = 10 ms
        // Note: The default parameters of each camera might be different in different API versions

        printf("Starting acquisition...\n");
        cam.StartAcquisition();

        printf("First pixel value \n");
        #define EXPECTED_IMAGES 100
        for (int images=0;images < EXPECTED_IMAGES;images++)
        {
            Mat cv_mat_image = cam.GetNextImageOcvMat();
            cv::imshow("Image from camera",cv_mat_image);
            cvWaitKey(20);
            printf("\t%d\n",cv_mat_image.at<unsigned char>(0,0));

        }

        cam.StopAcquisition();
        cam.Close();
        printf("Done\n");

        cvWaitKey(500);
    }
    catch(xiAPIplus_Exception& exp){
        printf("Error:\n");
        exp.PrintError();
        cvWaitKey(2000);
    }
    return 0;
}