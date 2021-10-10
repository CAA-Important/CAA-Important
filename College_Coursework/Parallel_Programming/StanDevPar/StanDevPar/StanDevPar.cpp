// StanDevPar.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"


#include <iostream>
#include <fstream>
#include <cmath>
#include <chrono>
#include <omp.h>

using namespace std;
const int MAX_SIZE = 250000;
double calculateSD(int data[], int cnt);

int main()
{
	int cnt = 0;
	int data[MAX_SIZE];
	ifstream inData;

	// read data from input file

	inData.open("numData.txt");
	if (!inData) {
		cout << "Cannot open input file" << endl;
		system("pause");
		return 1;
	}
	while (inData >> data[cnt]) {
		cnt = cnt + 1;
	}
	inData.close();

	auto started = std::chrono::high_resolution_clock::now();
	//calculate standard deviation 
	cout << "Standard Deviation = " << calculateSD(data, cnt) << endl;

	auto done = std::chrono::high_resolution_clock::now();
	cout << "Execution Time (millseconds):" << std::chrono::duration_cast<std::chrono::milliseconds>(done - started).count() << endl;
	cout << endl;
	system("pause");
	return 0;
}

double calculateSD(int data[], int cnt)
{
	double sum = 0.0, mean, standardDeviation = 0.0;

	int i;

	cout << "cnt " << cnt << endl;

#pragma omp parallel reduction (+:sum) num_threads(6)
	{
#pragma omp for
		for (i = 0; i < cnt; ++i)
		{
			sum += data[i];
		}
	}
	mean = sum / cnt;

#pragma omp parallel reduction (+:standardDeviation) num_threads(6)
	{
#pragma omp for
		for (i = 0; i < cnt; ++i) {
			standardDeviation += pow(data[i] - mean, 2);
		}
	}
	return sqrt(standardDeviation / cnt);
}

