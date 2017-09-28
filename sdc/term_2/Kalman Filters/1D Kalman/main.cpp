#include <iostream>
#include <vector>
#include "Eigen/Dense"

using namespace std;
using namespace Eigen;

//kalman filter variables
VectorXd x; //object state
MatrixXd P; //object covariance
VectorXd u; //external motion
MatrixXd F; //state transformation matrix
MatrixXd H; //measurement matrix
MatrixXd R; //measurement covariance
MatrixXd I; //identity
MatrixXd Q; //process covariance

vector<VectorXd> measurements;
void filter(VectorXd &x, MatrixXd &P);

int main() {

    //init variables
    x = VectorXd(2);
    x << 0,0;

    P = MatrixXd(2, 2);
    P << 1000, 0, 0, 1000;

    u = VectorXd(2);
    u << 0,0;

    F = MatrixXd(2,2);
    F <<    1,1,
            0,1;

    H = MatrixXd(1, 2);
    H << 1, 0;

    R = MatrixXd(1, 1);
    R << 1;

    I = MatrixXd::Identity(2, 2);

    Q = MatrixXd(2, 2);
    Q << 0, 0, 0, 0;

    //create a list of measurements
    VectorXd single_meas(1);
    single_meas << 1;
    measurements.push_back(single_meas);
    single_meas << 2;
    measurements.push_back(single_meas);
    single_meas << 3;
    measurements.push_back(single_meas);

    filter(x, P);

    cout << "x: " << x << endl;
    cout << "P: " << P << endl;
    return 0;
}

void filter(VectorXd &x, MatrixXd &P){
    for (uint n = 0; n < measurements.size(); ++n){
        cout << "evaluating measurement: " << n << endl;

        //measurement update
        VectorXd z = measurements[n];
        MatrixXd y = z - (H * x);
        MatrixXd S = H * P * H.transpose() + R;
        MatrixXd K = P * H.transpose() * S.inverse();


        x = x + (K * y);
        P = (I - (K * H)) * P;

        //prediction update
        x = (F * x) + u;
        P = F * P * F.transpose();
    }
}