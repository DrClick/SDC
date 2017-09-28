#include "kalman_filter.h"
#include <cmath>

using Eigen::MatrixXd;
using Eigen::VectorXd;

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in) {
  x_ = x_in; //the current state
  // TODO: Fix up for a more complete treatment of control matrix
//  u_ = u_in; //the control state (known external forces like acceleration)
//  B_ = B_in; //the control matrix
  P_ = P_in; //the current state covariance
  F_ = F_in; //prediction model
  H_ = H_in; //transform of state into measurement space
  R_ = R_in; //measurement uncertainty
  Q_ = Q_in; //process uncertainty
}

void KalmanFilter::Predict() {
  //predict the next state by applying the motion model (F) to x
  x_ = F_ * x_;
  MatrixXd Ft = F_.transpose();

  //now apply this motion model (F) to the covariance (P) and add system
  //uncertainty
  P_ = F_ * P_ * Ft + Q_;
}

void KalmanFilter::Update(const VectorXd &z) {

  //first transform the current state to the measurement space
  //in other words, we need to compare the current state to the measurement
  //and since the measurement could use different coordinate system, or
  //directly or indirectly supply parts of the state, we need to transform
  //the current state into the same "space" as the measurement in order to compare them
  VectorXd z_pred = H_ * x_;

  //y is now the delta between the observed measurement and the predicted state of the system in
  //the measurement space
  VectorXd y = z - z_pred;

  //we also need to transform the covariance to the measurement space. Here we apply the same
  //math we did in the predict step to with F and P but now we are using H and adding measurement
  //noise R instead of process noise Q
  MatrixXd Ht = H_.transpose();
  MatrixXd S = H_ * P_ * Ht + R_;

  //finally we need the kalman gain... ok, just look this up
  MatrixXd Si = S.inverse();
  MatrixXd PHt = P_ * Ht;
  MatrixXd K = PHt * Si;

  //new estimate
  x_ = x_ + (K * y);
  long x_size = x_.size();
  MatrixXd I = MatrixXd::Identity(x_size, x_size);
  P_ = (I - K * H_) * P_;
}

void KalmanFilter::UpdateEKF(const VectorXd &z) {
  //in the extended kalman filter, we need to convert the
  //state to the polar coordinates
  VectorXd z_pred(3);

  float px = x_(0);
  float py = x_(1);
  float vx = x_(2);
  float vy = x_(3);

  auto rho = sqrt(px * px + py * py);
  auto rho_dot = (px * vx + py * vy) / rho;
  auto phi = atan2(py, px);

  z_pred << rho, phi, rho_dot;


  //y is now the delta between the observed measurement and the predicted state of the system in
  //the measurement space
  VectorXd y = z - z_pred;

  while (y[1] > M_PI || y[1] < -M_PI) {
    if (y[1] < -M_PI) {
      y[1] += 2 * M_PI;
    } else {
      y[1] -= 2 * M_PI;
    }
  }

  //we also need to transform the covariance to the measurement space. Here we apply the same
  //math we did in the predict step to with F and P but now we are using H and adding measurement
  //noise R instead of process noise Q
  MatrixXd Ht = H_.transpose();
  MatrixXd S = H_ * P_ * Ht + R_;

  //finally we need the kalman gain... ok, just look this up
  MatrixXd Si = S.inverse();
  MatrixXd PHt = P_ * Ht;
  MatrixXd K = PHt * Si;

  //new estimate
  x_ = x_ + (K * y);
  long x_size = x_.size();
  MatrixXd I = MatrixXd::Identity(x_size, x_size);
  P_ = (I - K * H_) * P_;
}


