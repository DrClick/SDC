//
// Created by Watson, Thomas (VWoA-ERL) on 9/23/17.
//

#ifndef KALMAN_KALMAN_FILTER_H
#define KALMAN_KALMAN_FILTER_H

#include "Eigen/Dense"

using Eigen::MatrixXd;
using Eigen::VectorXd;

class KalmanFilter {
public:

    ///* state vector
    VectorXd x_;

    ///* state covariance matrix
    MatrixXd P_;

    ///* state transition matrix (ie model of motion)
    MatrixXd F_;

    ///* process covariance matrix
    MatrixXd Q_;

    ///* measurement matrix
    MatrixXd H_;

    ///* measurement covariance matrix
    MatrixXd R_;


    /**
     * Constructor
     */
    KalmanFilter();

    /**
     * Destructor
     */
    virtual ~KalmanFilter();

    /**
     * Predicts the state and the state covariance
     * using the process model (F)
     */
    void Predict();

    /**
     * Updates the state with z
     * @param z The measurement at k+1
     */
    void Update(const VectorXd &z);
};

#endif //KALMAN_KALMAN_FILTER_H
