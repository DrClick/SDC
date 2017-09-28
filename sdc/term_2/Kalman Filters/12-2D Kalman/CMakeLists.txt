cmake_minimum_required(VERSION 3.8)
project(12_2D_Kalman)

set(CMAKE_CXX_STANDARD 17)

set(SOURCE_FILES main.cpp measurement_package.h tracking.h kalman_filter.h kalman_filter.cpp tracking.cpp)
add_executable(12_2D_Kalman ${SOURCE_FILES})