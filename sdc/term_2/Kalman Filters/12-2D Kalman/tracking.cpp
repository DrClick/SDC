//
// Created by Watson, Thomas (VWoA-ERL) on 9/23/17.
//

#include "Eigen/Dense"
#include "iostream"
#include "tracking.h"
#include <cmath>

using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::vector;

Tracking::Tracking() {
    is_initialzed_ = false;
    previous_timestamp_ = 0;

    //create a 4d vector sate
    kf_.x_ = VectorXd(4);

    //state covariance
    kf_.P_ = MatrixXd(4, 4);
    kf_.P_ <<   1, 0, 0,    0,
                0, 1, 0,    0,
                0, 0, 1000, 0,
                0, 0, 0,    1000;

    //measurement covariance
    kf_.R_ = MatrixXd(2, 2);
    kf_.R_ <<   0.0225, 0.0,
                0.0,    0.2225;

    //measurement matrix
    kf_.H_ = MatrixXd(2, 4);
    kf_.H_ <<   1, 0, 0, 0,
                0, 1, 0, 0;

    //The initial transition matrix
    kf_.F_ = MatrixXd(4, 4);
    kf_.F_ <<   1, 0, 1, 0,
                0, 1, 0, 1,
                0, 0, 1, 0,
                0, 0, 0, 1;

    noise_ax = 5;
    noise_ay = 5;
}

Tracking::~Tracking() = default;

void Tracking::ProcessMeasurement(const MeasurementPackage &measurement_pack) {
    if(!is_initialzed_){
        cout << "Kalman Filter Initizlization" << endl;

        //set the state with the initial measurement
        kf_.x_ <<   measurement_pack.raw_measurements_[0],
                    measurement_pack.raw_measurements_[1],
                    0,0;
        previous_timestamp_ = measurement_pack.timestamp_;
        is_initialzed_ = true;
    }

    //compute time elapsed since last measurement
    float dt = (measurement_pack.timestamp_ - previous_timestamp_) / 1000000.0;
    previous_timestamp_ = measurement_pack.timestamp_;

    // TODO: YOUR CODE HERE
    //1. Modify the F matrix so that the time is integrated
    kf_.F_ <<   1, 0, dt, 0,
                0, 1, 0, dt,
                0, 0, 1, 0,
                0, 0, 0, 1;
    //2. Set the process covariance matrix Q
    kf_.Q_ = MatrixXd(4,4);
    kf_.Q_ <<   pow(dt, 4)/4 * noise_ax, 0, pow(dt, 3)/2 * noise_ax, 0,
                0, pow(dt, 4)/4 * noise_ay, 0, pow(dt, 3)/2 * noise_ay,
                pow(dt, 3)/2 * noise_ax, 0, pow(dt, 2)/1 * noise_ax, 0,
                0, pow(dt, 3)/2 * noise_ay, 0, pow(dt, 2)/1 * noise_ay;


    //3. Call the Kalman Filter predict() function
    kf_.Predict();
    //4. Call the Kalman Filter update() function
    // with the most recent raw measurements_
    kf_.Update(measurement_pack.raw_measurements_);

    std::cout << "x_= " << kf_.x_ << std::endl;
    std::cout << "P_= " << kf_.P_ << std::endl;

}