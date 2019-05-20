cmake_minimum_required(VERSION 3.14)
project(lab04)

set(CMAKE_CXX_STANDARD 11)
add_executable(lab04 main.cpp function.cpp function.h)
TARGET_LINK_LIBRARIES(lab04 pthread)
