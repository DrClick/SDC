cmake_minimum_required(VERSION 3.8)
project(Kalman_Filters)

set(CMAKE_CXX_STANDARD 17)

set(SOURCE_FILES main.cpp)
add_executable(Kalman_Filters ${SOURCE_FILES})