//
// Created by Watson, Thomas (VWoA-ERL) on 9/26/17.
//
#include <iostream>
#include <vector>
#include "catch.hpp"
#include "../src/tools.h"
#include "../src/Eigen/Dense"

using namespace std;
using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::vector;

Tools tools;

TEST_CASE("CalculateRMSE", "[TOOLS]") {

  vector<VectorXd> estimations;
  vector<VectorXd> ground_truths;

  auto estimation = VectorXd(4);
  auto ground_truth = VectorXd(4);

  estimation << 1, 1, 0.2, 0.1;
  estimations.push_back(estimation);
  estimation << 2, 2, 0.3, 0.2;
  estimations.push_back(estimation);
  estimation << 3, 3, 0.4, 0.3;
  estimations.push_back(estimation);

  ground_truth << 1.1, 1.1, 0.3, 0.2;
  ground_truths.push_back(ground_truth);
  ground_truth << 2.1, 2.1, 0.4, 0.3;
  ground_truths.push_back(ground_truth);
  ground_truth << 3.1, 3.1, 0.5, 0.4;
  ground_truths.push_back(ground_truth);

  auto expected = VectorXd(4);
  expected << .1, .1, .1, .1;

  auto actual = tools.CalculateRMSE(estimations, ground_truths);

  REQUIRE(actual.isApprox(expected));
}

TEST_CASE("CalculateJacobian", "[TOOLS]") {
  VectorXd x_predicted(4);
  x_predicted << 1, 2, 0.2, 0.4;

  MatrixXd expected(3,4);
  expected << 0.447214, 0.894427, 0, 0,
      -0.4, 0.2, 0, 0,
      0, 0, 0.447214, 0.894427;

  MatrixXd actual = tools.CalculateJacobian(x_predicted);

  auto isApprox = actual.isApprox(expected, .000001);
  REQUIRE(isApprox == true);
}