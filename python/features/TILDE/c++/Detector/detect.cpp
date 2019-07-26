// test.cpp ---
//
// Filename: test.cpp
// Description:
// Author: Yannick Verdie, Kwang Moo Yi
// Maintainer: Yannick Verdie
// Created: Tue Mar  3 17:47:28 2015 (+0100)
// Version: 0.5a
// Package-Requires: ()
// Last-Updated: Tue Jun 16 17:09:04 2015 (+0200)
//           By: Kwang
//     Update #: 26
// URL:
// Doc URL:
// Keywords:
// Compatibility:
//
//

// Commentary:
//
//
//
//

// Change Log:
//
//
//
//
// Copyright (C), EPFL Computer Vision Lab.
//
//

// Code:

#include "src/libTILDE.hpp"
#include <fstream>
#include <iterator>
#include <string>
#include <limits>
#include <opencv2/opencv.hpp>
//#include <utility>      // std::pair

vector<KeyPoint> testImage(const Mat &I,const string &pathFilter, const int &nbTest = 1, const char* ext = NULL, Mat* score = NULL)
{
	using namespace std::chrono;
	using namespace cv;
 	high_resolution_clock::time_point t1, t2;
 	std::vector<KeyPoint> kps;
 	double time_spent = 0;

	// Use appoximated filters if told to do so
 	bool useApprox = false;
 	if (ext != NULL)
 		useApprox = true;

	for (int i =0;i<nbTest;i++)
	{
		// Run TILDE
	    kps = getTILDEKeyPoints(I, pathFilter, useApprox,true,-std::numeric_limits<float>::infinity(),score);

	}
	std::vector<KeyPoint> res;
	//keep only the 100 best
	std::copy(kps.begin(),kps.begin()+min<int>(kps.size(),500),back_inserter(res));

	return res;
}

vector<KeyPoint> test_fast(const Mat &I,const string &pathFilter, const int &nbTest = 1, Mat* score = NULL)
{
	using namespace std::chrono;
	using namespace cv;
 	high_resolution_clock::time_point t1, t2;
 	std::vector<KeyPoint> kps;
 	double time_spent = 0;



	// Run multiple times to measure average runtime
	for (int i =0;i<nbTest;i++)
	{
		t1 = high_resolution_clock::now();
		// Run TILDE
	    kps = getTILDEKeyPoints_fast(I, pathFilter,true,-std::numeric_limits<float>::infinity(),score);
		t2 = high_resolution_clock::now();

		time_spent += duration_cast<duration<double>>(t2 - t1).count();
	}
	// Display execution time
	cout<<"Time all: "<<time_spent/nbTest<<" s"<<endl;


	std::vector<KeyPoint> res;
	//keep only the 100 best
	std::copy(kps.begin(),kps.begin()+min<int>(kps.size(),500),back_inserter(res));

	return res;
}

void keyPointVec_To_File(std::vector<KeyPoint>& vec, const std::string file_path){
	std::ofstream output_file;
	output_file.open(file_path);
	for( size_t ii = 0; ii < vec.size(); ++ii)
		output_file << vec[ii].pt.x<< ","<<vec[ii].pt.y<< std::endl;
	output_file.close();
}

void keyPointVec_To_StdOut(std::vector<KeyPoint>& vec){
	for( size_t ii = 0; ii < vec.size(); ++ii)
		std::cout << vec[ii].pt.x<< ","<<vec[ii].pt.y<< std::endl;
}


int main(int argc,char** argv)
{
	/* commandline arguments:
		argv[1] = location of the image png
		argv[2] = location of the output kpts file.
	*/
	using namespace std::chrono;
	using namespace cv;
	string pathFilter;

	try
	{
		// Load test image
		string image = argv[1];
		Mat I = imread(image);
		if (I.data == 0) throw std::runtime_error("Image not found !");

		// Initialize the score image
		// pathFilter = "../Lib/filters/Mexico24.txt";
		pathFilter = argv[3];

 		Mat score1 = Mat::zeros(I.rows,I.cols,CV_32F);
		vector<KeyPoint> kps1 = testImage(I,pathFilter,1,"n_approx", &score1);
		keyPointVec_To_File(kps1, argv[2]);
	}
	catch (std::exception &e) {
		cout<<"ERROR: "<<e.what()<<"\n";
	}

	return 0;
}
//
// test.cpp ends here
