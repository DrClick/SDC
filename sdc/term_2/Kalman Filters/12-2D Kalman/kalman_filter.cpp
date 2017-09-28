//
// Created by Watson, Thomas (VWoA-ERL) on 9/23/17.
//

#include "kalman_filter.h"


KalmanFilter::KalmanFilter() = default;
KalmanFilter::~KalmanFilter() = default;

void KalmanFilter::Predict() {
    x_ = F_ * x_;
    MatrixXd Ft = F_.transpose();
    P_ = F_ * P_ * Ft + Q_;
}


void KalmanFilter::Update(const VectorXd &z) {
    VectorXd z_pred = H_ * x_;
    VectorXd y = z - z_pred;
    MatrixXd Ht = H_.transpose();
    MatrixXd S = H_ * P_ * Ht + R_;
    MatrixXd Si = S.inverse();
    MatrixXd PHt = P_ * Ht;
    MatrixXd K = PHt * Si;

    //new estimate
    long x_size = x_.size();
    MatrixXd I = MatrixXd::Identity(x_size, x_size);

    x_ = x_ + (K * y);
    P_ = (I - K * H_) * P_;
}