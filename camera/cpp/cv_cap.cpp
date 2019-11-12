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
    cout << "Set exposure" << endl;
    cam.SetExposureTime(1000); //1000 us = 1 ms
	
	// cam.SetAcquisitionTimingMode("XI_ACQ_TIMING_MODE");
//    cout << "Set framerate" << endl;
//	cam.SetFrameRate(500.0);
    
	// cam.SetDownsamplingType("XI_DOWNSAMPLING_TYPE");
    cout << "Set downsamoling" << endl;
	cam.SetDownsampling((XI_DOWNSAMPLING_VALUE)2);

	cout << "Starting acquisition..." << endl;
    cam.StartAcquisition();

	cout << "First pixel value:" << endl;
	XI_IMG_FORMAT format = cam.GetImageDataFormat();
    
    // Save
    // 作成する動画ファイルの諸設定
	int    width, height, fourcc;
	double fps;
 
	width  = (int)cam.GetWidth();	// フレーム横幅を取得
	height = (int)cam.GetHeight();	// フレーム縦幅を取得
	fps    = cam.GetFrameRate();					// フレームレートを取得
 
	// ビデオフォーマットの指定
	fourcc = cv::VideoWriter::fourcc('H', '2', '6', '4');	// H264  / ファイル拡張子 .avi
	// 動画ファイルを書き出すためのオブジェクトを宣言する
	VideoWriter writer;
	writer.open("out.avi", fourcc, fps, Size(width, height));

    Mat cv_mat_image;
	
    #define EXPECTED_IMAGES 50
	for (int images=0;images < EXPECTED_IMAGES;images++)
		{
	// Read and convert a frame from the camera
		cv_mat_image = cam.GetNextImageOcvMat();
//		cout << +cv_mat_image.at<uchar>(0, 0) << endl;
		// imshow("Image from camera", cv_mat_image);
//        cout << cv_mat_image << endl;
		float fps = cam.GetFrameRate();
		printf("FPS:%f\n", fps);
		}
    
	//動画ファイルに画像を出力。
	writer << cv_mat_image;
	waitKey(1000);

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
